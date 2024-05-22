# -*- coding: utf-8 -*-
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
#
from collections import defaultdict
from typing import Union
import numpy as np

from sympy.matrices import Matrix

from BasicTools.NumpyDefs import PBasicFloatType
from BasicTools.Containers.Filters import ElementFilter
from BasicTools.Helpers.BaseOutputObject import BaseOutputObject as BOO
from BasicTools.FE.SymWeakForm import Gradient, Divergence, GetField, GetTestField, GetScalarField, Inner, Trace
import BasicTools.FE.SymWeakForm as swf
import BasicTools.Helpers.ParserHelper as PH
from BasicTools.Helpers.BaseOutputObject import froze_it


@froze_it
class Physics(BOO):
    """Basic class to hold the information about symbolic terms"""

    def __init__(self):
        self.integrationRule = None
        self.spaces = [None]
        self.bilinearWeakFormulations = []
        self.linearWeakFormulations = []
        self.numberings = None
        self.spaceDimension = 3
        self.extraRHSTerms = []
        self.coeffs = {}

    def GetCoeff(self, var_name):
        return self.coeffs.get(var_name, GetScalarField(var_name))

    def AddToRHSTerm(self, nf, val):
        """ nf  : a NodalFilter
            val : a vector of size len(self.spaces)
        """
        self.extraRHSTerms.append((nf, val))

    def Reset(self):
        self.numberings = None

    def ExpandNames(self, data):
        if data[1] == 1:
            return data[0]
        return [data[0] + "_" + str(d) for d in range(data[1])]

    def GetBulkMassFormulation(self, alpha: Union[PBasicFloatType, str] = 1.):
        u = self.primalUnknown
        ut = self.primalTest

        a = GetScalarField(alpha)

        return u.T*ut*a

    def SetSpaceToLagrange(self, P=None, isoParam=None):
        if P is None and isoParam is None:  # pragma: no cover
            raise (ValueError("Please set the type of integration P=1,2 or isoParam=True"))

        if P is not None and isoParam is not None:  # pragma: no cover
            raise (ValueError("Please set the type of integration P=1,2 or isoParam=True"))

        if isoParam is None or isoParam == False:
            if P == 1:
                from BasicTools.FE.Spaces.FESpaces import LagrangeSpaceP1
                space = LagrangeSpaceP1
                self.integrationRule = "LagrangeP1"
            elif P == 2:
                from BasicTools.FE.Spaces.FESpaces import LagrangeSpaceP2
                space = LagrangeSpaceP2
                self.integrationRule = "LagrangeP2"
            else:  # pragma: no cover
                raise (ValueError(f" P cant be : {P} , must be 1, 2 or None"))
        else:
            from BasicTools.FE.Spaces.FESpaces import LagrangeSpaceGeo
            space = LagrangeSpaceGeo
            self.integrationRule = "LagrangeIsoParam"

        self.spaces = [space]*len(self.GetPrimalNames())

    def AddBFormulation(self, zoneOrElementFilter, data):

        if type(zoneOrElementFilter) == str:
            ef = ElementFilter(tag=zoneOrElementFilter)
        else:
            ef = zoneOrElementFilter

        self.bilinearWeakFormulations.append((ef, data))

    def AddLFormulation(self, zoneOrElementFilter, data):

        if type(zoneOrElementFilter) == str:
            ef = ElementFilter(tag=zoneOrElementFilter)
        else:
            ef = zoneOrElementFilter

        self.linearWeakFormulations.append((ef, data))

    def GetNumberOfUnkownFields(self):
        return len(self.GetPrimalNames())

    def ComputeDofNumbering(self, mesh, tagsToKeep=None, fromConnectivity=False):
        from BasicTools.FE.DofNumbering import ComputeDofNumbering
        if self.numberings is None:
            self.numberings = [None]*self.GetNumberOfUnkownFields()
        else:
            return

        from BasicTools.Containers.Filters import ElementFilter, UnionElementFilter
        allFilters = UnionElementFilter(mesh)

        ff = ElementFilter(mesh, tags=tagsToKeep)
        allFilters.filters.append(ff)
        allFilters.filters.extend([f for f, form in self.linearWeakFormulations])
        allFilters.filters.extend([f for f, form in self.bilinearWeakFormulations])

        for d in range(self.GetNumberOfUnkownFields()):
            for i in range(0, d):
                if self.spaces[d] == self.spaces[i]:
                    self.numberings[d] = self.numberings[i]
                    break
            else:
                if fromConnectivity:
                    self.numberings[d] = ComputeDofNumbering(
                        mesh, self.spaces[d], fromConnectivity=True, dofs=self.numberings[d])
                else:
                    self.numberings[d] = ComputeDofNumbering(
                        mesh, self.spaces[d], fromConnectivity=False, elementFilter=allFilters, dofs=self.numberings[d])

    def ComputeDofNumberingFromConnectivity(self, mesh):
        self.ComputeDofNumbering(mesh, fromConnectivity=True)


@froze_it
class MecaPhysics(Physics):
    """Weak forms for mechanical problems

    Parameters
    ----------
    dim : int, optional
        dimension of the unknown, by default 3
    elasticModel : str, optional
        The type of model used, by default "isotropic"
        option are : "isotropic", "orthotropic", "anisotropic"
    """

    def __init__(self, dim=3, elasticModel="isotropic"):
        super().__init__()
        self.UnFrozen()
        self.spaceDimension = dim

        self.mecaPrimalName = ("u", self.spaceDimension)
        self.SetMecaPrimalName(self.mecaPrimalName[0])

        self.mecaSpace = None

        if elasticModel not in ["isotropic", "orthotropic", "anisotropic"]:  # pragma: no cover
            raise Exception(
                f'elasticModel ({elasticModel}) not available : options are "isotropic", "orthotropic", "anisotropic" ')
        self.elasticModel = elasticModel

        self.HookeLocalOperator = None

        self.materialOrientations = np.eye(self.spaceDimension, dtype=PBasicFloatType)
        self.planeStress = True

    def SetYoung(self, val):
        self.coeffs["young"] = PH.ReadFloat(val)

    def SetPoisson(self, val):
        self.coeffs["poisson"] = PH.ReadFloat(val)

    def SetMecaPrimalName(self, name):
        self.mecaPrimalName = (name, self.spaceDimension)
        self.primalUnknown = GetField(self.mecaPrimalName[0], self.mecaPrimalName[1])
        self.primalTest = GetTestField(self.mecaPrimalName[0], self.mecaPrimalName[1])

    def GetPrimalNames(self):
        return self.ExpandNames(self.mecaPrimalName)

    def GetHookeOperator(self, young=None, poisson=None, factor=None):

        if self.elasticModel == "isotropic":
            res = self.GetHookeOperatorIsotropic(young=young, poisson=poisson, factor=factor)
        elif self.elasticModel == "orthotropic":
            res = self.GetHookeOperatorOrthotropic(factor=factor)
        elif self.elasticModel == "anisotropic":
            res = self.GetHookeOperatorAnisotropic(factor=None)

        self.HookeLocalOperator = res
        return res

    def GetHookeOperatorIsotropic(self, young=None, poisson=None, factor=None):

        from BasicTools.FE.MaterialHelp import HookeLaw

        if young is None:
            young = self.GetCoeff("young")
        if poisson is None:
            poisson = self.GetCoeff("poisson")

        young = GetScalarField(young)*GetScalarField(factor)

        op = HookeLaw()
        op.Read({"E": young, "nu": poisson})
        return op.HookeIso(dim=self.spaceDimension, planeStress=self.planeStress)

    def GetHookeOperatorOrthotropic(self, factor=None):

        if self.spaceDimension == 2:
            hookOrtho = [["C11", "C12",    0],
                         ["C12", "C22",    0],
                         [0,     0, "C33"]]
        elif self.spaceDimension == 3:
            hookOrtho = [["C11", "C12", "C13",     0,     0,    0],
                         ["C12", "C22", "C23",     0,     0,    0],
                         ["C13", "C23", "C33",     0,     0,    0],
                         [0,     0,     0, "C44",     0,    0],
                         [0,     0,     0,     0, "C55",    0],
                         [0,     0,     0,     0,     0, "C66"]]
        else:  # pragma: no cover
            raise Exception("Orthotropic material no available for dimension : {self.spaceDimension}")

        return np.array([[self.GetCoeff(c) for c in line] for line in hookOrtho]) * GetScalarField(factor)

    def GetHookeOperatorAnisotropic(self, factor=None):
        if self.spaceDimension != 3:  # pragma: no cover
            raise Exception("Anisotropic material no available for dimension : {self.spaceDimension}")

        hookAnisotropic = [["C1111", "C1122", "C1133", "C1123", "C1131", "C1112"],
                           ["C2211", "C2222", "C2233", "C2223", "C2231", "C2212"],
                           ["C3311", "C3322", "C3333", "C3323", "C3331", "C3312"],
                           ["C2311", "C2322", "C2333", "C2323", "C2331", "C2312"],
                           ["C3111", "C3122", "C3133", "C3123", "C3131", "C3112"],
                           ["C1211", "C1222", "C1233", "C1223", "C1231", "C1212"]]

        return np.array([[self.GetCoeff(c) for c in line] for line in hookAnisotropic]) * GetScalarField(factor)

    def GetStressVoigt(self, utGlobal, HookeLocalOperator=None):
        from BasicTools.FE.SymWeakForm import ToVoigtEpsilon, Strain
        if HookeLocalOperator is None:
            HookeLocalOperator = self.HookeLocalOperator

        uLocal = Inner(self.materialOrientations, utGlobal)
        return swf.Inner(ToVoigtEpsilon(Strain(uLocal, self.spaceDimension)).T, HookeLocalOperator)

    def GetBulkFormulation(self, young=None, poisson=None, alpha=None):
        from BasicTools.FE.SymWeakForm import ToVoigtEpsilon, Strain
        uGlobal = self.primalUnknown
        utGlobal = self.primalTest

        utLocal = Inner(self.materialOrientations, utGlobal)

        HookeLocalOperator = self.GetHookeOperator(young, poisson, alpha)
        stress = self.GetStressVoigt(uGlobal, HookeLocalOperator)

        return stress*ToVoigtEpsilon(Strain(utLocal, self.spaceDimension))

    def GetPressureFormulation(self, pressure):
        ut = self.primalTest

        p = GetScalarField(pressure)

        from BasicTools.FE.SymWeakForm import GetNormal
        Normal = GetNormal(self.spaceDimension)

        return p*Normal.T*ut

    def GetForceFormulation(self, direction, flux="f"):
        ut = self.primalTest
        f = GetScalarField(flux)

        if not isinstance(direction, Matrix):
            direction = Matrix([direction]).T
        return f*direction.T*ut

    def GetDistributedForceFormulation(self, direction):
        ut = self.primalTest
        force = Matrix([GetScalarField(f) for f in direction])

        return Inner(force.T, ut)

    def GetAccelerationFormulation(self, direction, density=None):

        if density is None:
            density = self.GetCoeff("density")

        ut = self.primalTest
        density = GetScalarField(density)

        if not isinstance(direction, Matrix):
            direction = [GetScalarField(d) for d in direction]
            direction = Matrix([direction]).T

        return density*direction.T*ut

    def GetCentrifugalTerm(self, axe=[0, 0, 1], pointOnAxe=[0, 0, 0], angularSpeed=1, density=None):
        ut = self.primalTest

        if density is None:
            density = self.GetCoeff("density")

        density = GetScalarField(density)

        if not isinstance(axe, Matrix):
            axe = [GetScalarField(d) for d in axe]
            axe = Matrix([axe]).T

        if not isinstance(pointOnAxe, Matrix):
            pointOnAxe = [GetScalarField(d) for d in pointOnAxe]
            pointOnAxe = Matrix([pointOnAxe]).T

        pos = GetField("Pos", self.spaceDimension) - pointOnAxe
        r = pos - pos.dot(axe)*pos

        return -density*angularSpeed**2*r.T*ut

    def PostTreatmentFormulations(self):
        """For the moment this work only if GetBulkFormulation is called only once per instance
        the problem is the use of self.Hook"""
        import BasicTools.FE.SymWeakForm as wf
        uGlobal = self.primalUnknown
        utLocal = Inner(self.materialOrientations, uGlobal)

        nodalEnergyT = GetTestField("elastic_energy", 1)
        symEnergy = 0.5*wf.ToVoigtEpsilon(wf.Strain(utLocal)).T*self.HookeLocalOperator * \
            wf.ToVoigtEpsilon(wf.Strain(utLocal))*nodalEnergyT

        trStrainT = GetTestField("tr_strain_", 1)
        symTrStrain = wf.Trace(wf.Strain(uGlobal))*trStrainT

        trStressT = GetTestField("tr_stress_", 1)
        symTrStress = wf.Trace(wf.FromVoigtSigma(wf.ToVoigtEpsilon(
            wf.Strain(utLocal)).T*self.HookeLocalOperator))*trStressT

        postQuantities = {"elastic_energy": symEnergy,
                          "tr_strain_": symTrStrain,
                          "tr_stress_": symTrStress}

        return postQuantities


class MecaPhysicsAxi(MecaPhysics):
    def __init__(self):
        super().__init__(dim=2)

    def GetFieldR(self):
        return GetScalarField("r")

    def GetBulkFormulation(self, young=None, poisson=None, alpha=None):
        from BasicTools.FE.MaterialHelp import HookeLaw

        u = self.primalUnknown
        ut = self.primalTest

        if young is None:
            young = self.GetCoeff("young")
        if poisson is None:
            poisson = self.GetCoeff("poisson")

        young = GetScalarField(young)*GetScalarField(alpha)

        op = HookeLaw()
        op.Read({"E": young, "nu": poisson})
        self.HookeLocalOperator = op.HookeIso(dim=self.spaceDimension, planeStress=self.planeStress, axisymetric=True)
        print(self.HookeLocalOperator)

        r = self.GetFieldR()

        from BasicTools.FE.SymWeakForm import StrainAxyCol
        epsilon_u = StrainAxyCol(u, r)
        epsilon_ut = StrainAxyCol(ut, r)
        return 2*np.pi*epsilon_u.T*self.HookeLocalOperator*epsilon_ut*r

    def GetPressureFormulation(self, pressure):
        return super().GetPressureFormulation(pressure)*self.GetFieldR()

    def GetForceFormulation(self, direction, flux="f"):
        return super().GetForceFormulation(direction, flux)*self.GetFieldR()

    def GetAccelerationFormulation(self, direction, density=None):
        return super().GetForceFormulation(direction, density)*self.GetFieldR()

    def PostTreatmentFormulations(self):

        import BasicTools.FE.SymWeakForm as wf
        symDep = self.primalUnknown

        r = self.GetFieldR()
        pir2 = 2*np.pi*r

        nodalEnergyT = GetTestField("strain_energy", 1)

        symEnergy = pir2*0.5*wf.StrainAxyCol(symDep, r).T*self.HookeLocalOperator * \
            wf.StrainAxyCol(symDep, r)*nodalEnergyT

        from sympy import prod

        trStrainT = GetTestField("tr(strain)", 1)
        strain = wf.StrainAxyCol(symDep, r)
        symTrStrain = prod(strain[0:3])*trStrainT

        trStressT = GetTestField("tr(stress)", 1)
        stress = strain.T*self.HookeLocalOperator
        symTrStress = prod(stress[0:3])*trStressT

        postQuantities = {"strain_energy": symEnergy,
                          "tr(strain)": symTrStrain,
                          "tr(stress)": symTrStress}

        return postQuantities


@froze_it
class BasicPhysics(Physics):
    def __init__(self):
        super().__init__()
        self.UnFrozen()
        self.PrimalNameTrial = ("u", 1)
        self.PrimalNameTest = ("u", 1)
        self.Space = None
        self.SetPrimalName(self.PrimalNameTrial[0])

    def SetPrimalName(self, unknownName, testName=None, unknownDim=1, testDim=1):
        self.PrimalNameTrial = (unknownName, unknownDim)
        if testName is None:
            testName = unknownName
        self.PrimalNameTest = (testName, testDim)
        self.primalUnknown = GetField(self.PrimalNameTrial[0], self.PrimalNameTrial[1], sdim=self.spaceDimension)
        self.primalTest = GetTestField(self.PrimalNameTest[0], self.PrimalNameTest[1], sdim=self.spaceDimension)

    def GetPrimalNames(self):
        return [self.PrimalNameTrial[0]]

    def GetPrimalDims(self):
        return [self.PrimalNameTrial[1]]

    def GetBulkFormulation_dudi_dtdj(self, u=0, t=0, i=0, j=0, alpha=1.):

        a = GetScalarField(alpha)

        unk = self.primalUnknown

        if self.PrimalNameTrial[1] > 1:
            DTestDj = Gradient(unk, self.spaceDimension)[i, u]
        else:
            DTestDj = Gradient(unk, self.spaceDimension)[i]

        ut = self.primalTest
        if self.PrimalNameTest[1] > 1:
            DTrialDi = Gradient(ut, self.spaceDimension)[j, t]
        else:
            DTrialDi = Gradient(ut, self.spaceDimension)[j]

        return DTrialDi*(a)*DTestDj

    def GetBulkLaplacian(self, alpha=1.):
        from BasicTools.FE.SymWeakForm import Gradient
        a = GetScalarField(alpha)
        u = self.primalUnknown
        ut = self.primalTest
        return Gradient(u, self.spaceDimension).T*(a)*Gradient(ut, self.spaceDimension)

    def GetFlux(self, flux="f"):
        tt = self.primalTest
        f = GetScalarField(flux)

        return f*tt


@froze_it
class ThermalPhysics(Physics):
    def __init__(self):
        super().__init__()
        self.UnFrozen()
        self.thermalPrimalName = ("t", 1)
        self.SetPrimalNames(self.thermalPrimalName)
        self.thermalSpace = None

    def GetPrimalNames(self):
        return [self.thermalPrimalName[0]]

    def SetPrimalNames(self, data):
        self.thermalPrimalName = data
        self.primalUnknown = GetField(self.thermalPrimalName[0], 1)
        self.primalTest = GetTestField(self.thermalPrimalName[0], 1)

    def SetThermalPrimalName(self, name):
        self.thermalPrimalName = name

    def GetBulkFormulation(self, alpha=1.):
        t = self.primalUnknown
        tt = self.primalTest

        if hasattr(alpha, '__iter__') and not isinstance(alpha, str):
            from sympy import diag
            K = diag(*alpha)
            return Gradient(t, self.spaceDimension).T*K*Gradient(tt, self.spaceDimension)
        else:
            alpha = GetScalarField(alpha)
            return Gradient(t, self.spaceDimension).T*(alpha)*Gradient(tt, self.spaceDimension)

    def GetMassOperator(self, rho=1, cp=1):
        t = self.primalUnknown
        tt = self.primalTest

        rho = GetScalarField(rho)
        cp = GetScalarField(cp)

        return rho*cp*(t)*tt

    def GetNormalFlux(self, flux="f"):

        tt = self.primalTest
        f = GetScalarField(flux)

        return f*tt

    def GetRobinFlux(self, beta=None, Tinf=None):
        t = self.primalUnknown[0, 0]
        tt = self.primalTest[0, 0]

        beta = GetScalarField(beta)
        Tinf = GetScalarField(Tinf)
        return beta*(t - Tinf)*tt


@froze_it
class StokesPhysics(Physics):
    def __init__(self):
        super().__init__()
        self.UnFrozen()
        self.SetPrimalNames("v", "p")

    def GetPrimalNames(self):
        res = [self.velocityPrimalName[0] + "_" + str(c) for c in range(self.velocityPrimalName[1])]
        res.append(self.pressurePrimalName)
        return res

    def SetPrimalNames(self, vName, pName):
        self.velocityPrimalName = (vName, self.spaceDimension)
        self.pressurePrimalName = (pName, 1)
        self.primalUnknownV = GetField(self.velocityPrimalName[0], self.velocityPrimalName[1])
        self.primalUnknownP = GetField(self.pressurePrimalName[0], self.pressurePrimalName[1])
        self.primalTestV = GetTestField(self.velocityPrimalName[0], self.velocityPrimalName[1])
        self.primalTestP = GetTestField(self.pressurePrimalName[0], self.pressurePrimalName[1])

    def SetSpaceToLagrange(self, P=None, isoParam=None):
        from BasicTools.FE.Spaces.FESpaces import LagrangeSpaceP1
        from BasicTools.FE.Spaces.FESpaces import LagrangeSpaceP2

        self.spaces = [LagrangeSpaceP2]*self.spaceDimension
        self.spaces.append(LagrangeSpaceP1)
        self.integrationRule = "LagrangeP2"

    def GetBulkFormulation(self, mu=1.):

        mu = GetScalarField(mu)
        v = self.primalUnknownV
        vt = self.primalTestV
        p = self.primalUnknownP[0, 0]
        pt = self.primalTestP[0, 0]
        a = Trace(Gradient(v, self.spaceDimension)*mu*Gradient(vt, self.spaceDimension))
        b = Divergence(vt, self.spaceDimension)*p
        c = pt*Divergence(v, self.spaceDimension)
        return a - b + c


@froze_it
class ThermoMecaPhysics(Physics):
    def __init__(self):
        super().__init__()
        self.UnFrozen()
        self.mecaPhys = MecaPhysics()
        self.thermalPhys = ThermalPhysics()

    def GetPrimalNames(self):
        res = self.mecaPhys.GetPrimalNames()
        res.extend(self.thermalPhys.GetPrimalNames())
        return res

    def GetBulkFormulation(self, young=1., poisson=0.3, alpha=1.):
        res = self.mecaPhys.GetBulkFormulation(young=young, poisson=poisson, alpha=alpha)
        res += self.thermalPhys.GetBulkFormulation(alpha=alpha)

        # need to add the coupling terms

        # res += self.HookeLocalOperator

        return res


def CheckIntegrity(GUI=False):

    bp = BasicPhysics()
    bp.Reset()
    bp.GetBulkMassFormulation()
    bp.SetSpaceToLagrange(1)
    bp.SetSpaceToLagrange(2)
    bp.SetSpaceToLagrange(isoParam=True)
    bp.AddBFormulation("tagname", bp.GetBulkMassFormulation())

    from BasicTools.Containers.Filters import ElementFilter
    bp.AddBFormulation(ElementFilter(), bp.GetBulkMassFormulation())
    bp.AddLFormulation('ElementTagName', bp.GetBulkMassFormulation())
    bp.AddLFormulation(ElementFilter(), bp.GetBulkMassFormulation())
    print(bp.GetNumberOfUnkownFields())

    assert (bp.ExpandNames(("t", 1)) == "t")

    bp.spaceDimension = 3
    bp.SetPrimalName("U", "V", 3, 3)
    print(bp.primalUnknown)
    print(bp.primalTest)
    print(bp.GetBulkFormulation_dudi_dtdj(u=0, i=1, t=1, j=2))
    print(bp.GetBulkFormulation_dudi_dtdj())
    print(bp.GetBulkLaplacian())
    print(bp.GetFlux())

    ###############################################################
    res = ThermoMecaPhysics()
    print(res.GetBulkFormulation())
    print(res.GetPrimalNames())

    ###############################################################
    M2D = MecaPhysics(dim=2)
    M2D.SetYoung(1)
    M2D.SetPoisson(0)
    np.testing.assert_allclose(np.array(M2D.GetHookeOperator()), [[1, 0, 0], [0, 1, 0], [0, 0, 0.5]])
    ###############################################################

    M2D = MecaPhysics(dim=2, elasticModel="orthotropic")
    print(np.array(M2D.GetHookeOperator()))

    ###############################################################

    M3DI = MecaPhysics(dim=3)
    from itertools import product
    print(M3DI.GetHookeOperator())

    M3DO = MecaPhysics(dim=3, elasticModel="orthotropic")
    iter = range(1, 7)
    M3DO.coeffs.update({"C"+str(a)+str(b): (a)*10+(b) for a, b in product(iter, iter)})
    print(M3DI.coeffs)

    print(M3DO.GetHookeOperator())
    M3DA = MecaPhysics(dim=3, elasticModel="anisotropic")
    iter = range(1, 4)
    M3DA.coeffs.update({"C" + "".join(map(str, a)): int("".join(map(str, a))) for a in product(iter, iter, iter, iter)})
    print(M3DA.GetHookeOperator())
    print(M3DA.GetPressureFormulation(1))
    print(M3DA.GetAccelerationFormulation([1, 0, 0]))
    print(M3DA.GetDistributedForceFormulation([1, 0, 0]))
    print(M3DA.GetForceFormulation([1, 0, 0]))
    print(M3DA.GetCentrifugalTerm())

    print(M3DA.PostTreatmentFormulations())

    ###############################################################
    MPA = MecaPhysicsAxi()
    MPA.GetBulkFormulation()
    MPA.GetPressureFormulation(1)
    MPA.GetForceFormulation([1, 0], 1)
    MPA.GetAccelerationFormulation([1, 0], 1)
    MPA.PostTreatmentFormulations()
    ###############################################################

    TP = ThermalPhysics()
    TP.SetThermalPrimalName("u")
    TP.GetBulkFormulation([1, 0, 0])
    TP.GetMassOperator()
    TP.GetNormalFlux()
    TP.GetRobinFlux(beta=1, Tinf=24)
    ###############################################################

    SP = StokesPhysics()
    SP.GetPrimalNames()
    SP.SetSpaceToLagrange()
    SP.GetBulkFormulation()
    return "ok"


if __name__ == '__main__':
    print(CheckIntegrity(GUI=True))  # pragma: no cover
