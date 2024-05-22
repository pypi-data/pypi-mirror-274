# -*- coding: utf-8 -*-
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
#
import concurrent.futures
import time

import numpy as np
from scipy.sparse import coo_matrix

from BasicTools.NumpyDefs import PBasicIndexType, PBasicFloatType
from BasicTools.Helpers.CPU import GetNumberOfAvailableCpus
from BasicTools.Helpers.BaseOutputObject import froze_it
from BasicTools.Helpers.BaseOutputObject import BaseOutputObject

import BasicTools.Containers.ElementNames as EN
from BasicTools.Containers.Filters import ElementFilter, ElementCounter, FrozenFilter
from BasicTools.Containers.FiltersTools import GetListOfPartialElementFilter

from BasicTools.FE.Spaces.FESpaces import LagrangeSpaceGeo
from BasicTools.FE.Fields.FEField import FEField
from BasicTools.FE.Fields.IPField import IPField
from BasicTools.FE.DofNumbering import ComputeDofNumbering
from BasicTools.FE.FETools import PrepareFEComputation

from BasicTools.FE.SymWeakForm import GetField, GetTestField, GetNormal
import BasicTools.FE.WeakForms.NumericalWeakForm as WeakForm
from BasicTools.FE.IntegrationsRules import LagrangeIsoParam
from BasicTools.FE.IntegrationsRules import IntegrationRulesAlmanac


UseCpp = False
UseMultiThread =  True
MultiThreadThreshold = 100

def IntegrateGeneralMonoThread( mesh, wform, constants, fields, unkownFields=None, testFields=None, integrationRuleName=None,onlyEvaluation=False, elementFilter=None,userIntegrator=None, integrationRule=None):
    """Integration of a weak formulation using only one thread

    For more information about the argument please refer to IntegrationClass

    Returns
    -------
    K : coo_matrix
        the assembled matrix
    rhs : ndarray
        Array with the values of the right hand side term
    """

    intClass = IntegrationClass()
    intClass.SetIntegrator(userIntegrator)
    intClass.SetMesh(mesh)
    intClass.SetOnlyEvaluation(onlyEvaluation)
    intClass.SetElementFilter(elementFilter)
    intClass.SetConstants(constants)
    intClass.SetUnkownFields(unkownFields)
    intClass.SetTestFields(testFields)
    intClass.SetExtraFields(fields)
    intClass.SetIntegrationRule(integrationRuleName=integrationRuleName,integrationRule=integrationRule)
    intClass.SetWeakForm(wform)
    intClass.PreStartCheck()
    intClass.Allocate()
    intClass.Compute(forceMonoThread=True)
    return intClass.GetK(),intClass.GetRhs()


def IntegrateGeneral( mesh, wform, constants, fields, unkownFields=None, testFields=None,
                             integrationRuleName=None,onlyEvaluation=False, elementFilter=None,
                             userIntegrator=None, integrationRule=None):

    """Integration of a weak formulation

    For more information about the argument please refer to IntegrationClass

    Returns
    -------
    K : coo_matrix
        the assembled matrix
    rhs : ndarray
        Array with the values of the right hand side term
    """

    intClass = IntegrationClass()
    intClass.SetIntegrator(userIntegrator)
    intClass.SetMesh(mesh)
    intClass.SetOnlyEvaluation(onlyEvaluation)
    intClass.SetElementFilter(elementFilter)
    intClass.SetConstants(constants)
    intClass.SetUnkownFields(unkownFields)
    intClass.SetTestFields(testFields)
    intClass.SetExtraFields(fields)
    intClass.SetIntegrationRule(integrationRuleName=integrationRuleName,integrationRule=integrationRule)
    intClass.SetWeakForm(wform)
    intClass.PreStartCheck()
    intClass.Allocate()
    intClass.Compute()
    return intClass.GetK(),intClass.GetRhs()

@froze_it
class IntegrationClass(BaseOutputObject):
    """ Class to define and execute an integration of a weak form

    """
    def __init__(self, other=None):
        super(IntegrationClass,self).__init__()
        if other is None:
            #inputs
            self.mesh = None
            self.elementFilter = None
            self.weakForm = None
            self.numericalWeakForm = None
            self.integrator = None
            self.integrationRule = None
            self.extraFields = []
            self.posFields = []
            self.unkownFields = None
            self.testFields = None
            self.nbCPUs = GetNumberOfAvailableCpus()
            self.onlyEvaluation = False
            self.constants = {}
            #----
            self.vK = None
            self.iK = None
            self.jK = None
            self.numberOfUsedvij = 0
            self.rhs = None

            #----

            self.SetIntegrator()
        else:
            """this is a internal use to prepare a class instance for multithread integration """
            import BasicTools.FE.Integrators.NativeIntegration as NI
            self.integrator = NI.PyMonoElementsIntegralCpp()
            self.nbCPUs = 1
            self.mesh = other.mesh
            self.mesh = other.mesh
            self.onlyEvaluation = other.onlyEvaluation
            self.integrator.SetOnlyEvaluation(other.onlyEvaluation)
            self.constants = other.constants
            self.integrator.SetConstants(other.constants)
            self.SetUnkownFields(other.unkownFields)
            self.SetTestFields(other.testFields)
            self.extraFields = other.extraFields
            self.integrator.SetExtraFields(other.extraFields + other.posFields )
            self.integrationRule = other.integrationRule
            self.integrator.SetIntegrationRule(other.integrationRule)
            self.numericalWeakForm = other.numericalWeakForm
            self.posFields = other.posFields


    def Reset(self):
        self.integrator.Reset()

    def SetConstants(self, constants):
        """Set the contacts to be used in the weak form

        Parameters
        ----------

        constant : dict
            dictionary with the constants key : string , value: float
        """
        self.constants = constants
        self.integrator.SetConstants(constants)

    def SetOnlyEvaluation(self, onlyEvaluation):
        """Set the onlyEvaluation option. If true the contribution of the determinant of the
        transformation and the weight of the integration points is ignored. the user is
        responsible of dividing by the mass matrix (if necessary) to get the correct values.

        Parameters
        ----------
        onlyEvaluation : bool
            True to activate this option

        """
        self.onlyEvaluation = onlyEvaluation
        self.integrator.SetOnlyEvaluation(onlyEvaluation)

    def SetUnkownFields(self, unkownFields):
        """Set the fields used for the unknown space

        Parameters
        ----------
        unkownFields : list(FEField) list of fields
        """
        if unkownFields is None:
            unkownFields = []
        self.unkownFields = unkownFields
        self.integrator.SetUnkownFields(unkownFields)

    def SetTestFields(self, testFields):
        """Set the fields used for the test space

        Parameters
        ----------
        tfs : list(FEField) list of fields
            if tfs is none then the unknown fields are used (Galerkin projection)
        """
        self.testFields = testFields
        self.integrator.SetTestFields(testFields)

    def SetExtraFields(self, fields ):
        """Set the extra fields used in the weak formulation

        Parameters
        ----------
        efs : list(FEField or IPField) list of fields
        """
        self.extraFields = fields
        self.integrator.SetExtraFields(fields + self.posFields )

    def SetIntegrationRule(self,integrationRuleName=None, integrationRule=None ):
        """Set the Integration rule to be used during integration

        Parameters
        ----------
        integrationRuleName : str, optional
            name of the integrationRule

        integrationRule : dict, optional
            integration rule for every element type key->str: value: tuple(intPoints ndarray, intWeights )
        """
        if integrationRuleName is None:
            if integrationRule is None:
                self.integrationRule = LagrangeIsoParam
            else:
                self.integrationRule = integrationRule
        else:
            if integrationRule is None:
                self.integrationRule = IntegrationRulesAlmanac[integrationRuleName]
            else:
                raise Exception("must give integrationRuleName or integrationRule not both")
        self.integrator.SetIntegrationRule(self.integrationRule)

    def SetIntegrator(self, userIntegrator=None):
        """Set the internal integrator (only for advance users) """
        if userIntegrator is None:
            import BasicTools.FE.Integrators.PythonIntegration as PI
            self.integrator = PI.MonoElementsIntegral()
        else:
            self.integrator = userIntegrator

    def SetMesh(self,mesh):
        """Set the mesh defining the integration domain
        Parameters
        ----------
        mesh : UnstructuredMesh
            mesh containing the geometry
        """
        self.mesh = mesh

        fields = list()
        LSGNum = ComputeDofNumbering(self.mesh, Space=LagrangeSpaceGeo, fromConnectivity=True)
        for i in range(self.mesh.GetPointsDimensionality()):
            fields.append(FEField(f"Pos_{i}", mesh=self.mesh, space=LagrangeSpaceGeo,numbering=LSGNum, data=np.ascontiguousarray(self.mesh.nodes[:,i]) ))
        self.posFields = fields

    def SetElementFilter(self, elementFilter=None):
        """Set the element filter to select the elements of the integration
        """
        if elementFilter is None:
            if self.mesh is None:
                raise Exception("Need a mesh")
            else:
                self.elementFilter = ElementFilter( dimensionality=self.mesh.GetElementsDimensionality()).GetFrozenFilter(mesh=self.mesh)
        else:
            if type(elementFilter) == FrozenFilter:
                self.elementFilter = elementFilter
            else:
                self.elementFilter = elementFilter.GetFrozenFilter(mesh=self.mesh)

    def SetWeakForm(self,weakForm):
        """Set the weak form to be integrated
        Parameters
        ----------

        weakForm :  NativeNumericalWeakForm or PyWeakForm
            Weak form to be integrated
        """

        if weakForm is None :
            raise Exception("Weak form can't be None")
        self.weakForm = weakForm

        ttest = [WeakForm.PyWeakForm]
        try:
            import BasicTools.FE.WearForms.NativeNumericalWeakForm as NativeNumericalWeakForm
            ttest.append(NativeNumericalWeakForm.PyWeakForm)
        except ImportError :
            pass

        if not isinstance(self.weakForm, tuple(ttest) ):
            from BasicTools.FE.WeakForms.NumericalWeakForm import SymWeakToNumWeak
            self.numericalWeakForm = SymWeakToNumWeak(self.weakForm)
        else:
            self.numericalWeakForm = self.weakForm

    def PreStartCheck(self):
        """ verification of the integration rule for the ip fields:
        """
        for f in self.extraFields:
            if isinstance(f,IPField):
                if f.rule != self.integrationRule:
                    print("f.rule")
                    print(f.rule)
                    print("integrationRule")
                    print(self.integrationRule)
                    raise Exception(f"Integration rule of field {f.GetName()} not compatible with the integration" )

        from BasicTools.Containers.UnstructuredMesh import UnstructuredMesh
        if not isinstance(self.mesh, UnstructuredMesh):
            self.mesh.GetPosOfNodes()

    def SetOutputObjects(self, vK, iK, jK, rhs):
        """ This is an advace feature, the user must put objects of the correct size"""
        self.vK = vK
        self.iK = iK
        self.jK = jK

        self.rhs = rhs

    def Allocate(self):
        """ Function to allocate the memory to do the integration
        This function must be called right before the integration

        """
        numberOfVIJ = self.integrator.ComputeNumberOfVIJ(self.mesh,self.elementFilter)
        if numberOfVIJ == 0 and ( self.testFields is not None and len(self.testFields)*len(self.unkownFields) ) > 0:
            print("Warning!!! System with zero dofs")
            raise Exception("Error!!! System with zero dofs")

        # be sure to have valid pointer so we allocate at least one element
        if numberOfVIJ==0:
            numberOfVIJ = 1


        vK = np.zeros(numberOfVIJ,dtype=PBasicFloatType)
        iK = np.zeros(numberOfVIJ,dtype=PBasicIndexType)
        jK = np.zeros(numberOfVIJ,dtype=PBasicIndexType)

        rhs = np.zeros(self.integrator.GetTotalTestDofs(),dtype=PBasicFloatType)

        self.SetOutputObjects( vK, iK, jK, rhs)

    def Compute(self, forceMonoThread=False):
        """Execute the integration in multithread

        Parameters
        ----------
        forceMonoThread : bool
            true to force the use of only one thread

        """
        numberOfElementToTreat = self.elementFilter.ApplyOnElements(ElementCounter()).cpt
        if numberOfElementToTreat == 0:
            print("Warning no elements selected for integration. Please Check your Element Filter")
            return
        elif not self.integrator.IsMultiThread() or forceMonoThread or self.nbCPUs == 1:
            self.PrintDebug(f"Integration forceMonoThread={forceMonoThread}, nbCPUs={self.nbCPUs}")
            return self.ComputeMonoThread()
        elif numberOfElementToTreat < MultiThreadThreshold:
            return self.ComputeMonoThread()

        def InitSpaces(fields):
            for f in fields:
                if isinstance(f,IPField):
                    continue
                for space in f.space.values():
                    space.Create()

        for space in LagrangeSpaceGeo.values():
            space.Create()

        if self.unkownFields is not None:
            InitSpaces(self.unkownFields)
        InitSpaces(self.extraFields)
        if self.testFields is not None:
            InitSpaces(self.testFields)

        allWorkload = GetListOfPartialElementFilter(self.elementFilter, self.nbCPUs)
        workload = []

        cpt = 0
        totalTestDofs = self.integrator.GetTotalTestDofs()
        for f in allWorkload:
            if f.ApplyOnElements(ElementCounter()).cpt > 0:
                numberOfVIJ = self.integrator.ComputeNumberOfVIJ(self.mesh,f)
                workload.append((f,self.vK[cpt:numberOfVIJ+cpt],self.iK[cpt:numberOfVIJ+cpt],self.jK[cpt:numberOfVIJ+cpt], totalTestDofs) )
                cpt += numberOfVIJ

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.nbCPUs) as executor:
            results =  executor.map(self._InternalComputeMonoThreadSafe, workload)
            for rhs in results:
                self.rhs += rhs
        self.numberOfUsedvij = cpt

    def _InternalComputeMonoThreadSafe(self, elementFilter_vK_iK_jK):
        elementFilter,vK,iK,jK, totalTestDofs = elementFilter_vK_iK_jK
        res = IntegrationClass(self)
        res.SetElementFilter(elementFilter)
        res.SetOutputObjects(vK, iK, jK, np.zeros(totalTestDofs, dtype=PBasicFloatType))
        res.ComputeMonoThread()
        return res.GetRhs()

    def ComputeMonoThread(self, elementFilter=None):
        """Execute the integration using only one tread (this function is no thread safe)
        """

        self.integrator.PrepareFastIntegration(self.mesh,self.numericalWeakForm,self.vK,self.iK,self.jK,0,self.rhs)

        if elementFilter is None:
            elementFilter = self.elementFilter

        for _name, data, idsToTreat in elementFilter:
            if len(idsToTreat) == 0:
                continue
            self.integrator.ActivateElementType(data)
            self.integrator.Integrate(self.numericalWeakForm, np.asarray(idsToTreat, dtype=PBasicIndexType))

        self.numberOfUsedvij = self.integrator.GetNumberOfUsedIvij()

    def GetKvij(self):
        """Get the values to build the operator

        Returns
        -------
            values : ndarray
                values of the operator
            tuple : (ndarray,ndarray)
                indices (i,j)

        """
        data = (self.vK[0:self.numberOfUsedvij], (self.iK[0:self.numberOfUsedvij],self.jK[0:self.numberOfUsedvij]))
        return data

    def GetLinearSystemSize(self):
        """Get the size of the Linear System

        Returns
        -------
        nbrows : int
            Number of rows of the linear system
        nbcols : int
            Number of columns of the linear system
        """
        return (self.integrator.GetTotalTestDofs(), self.integrator.GetTotalUnkownDofs())

    def GetK(self):
        """ Get K as a scipy.sparse.coo_matrix

        Returns
        -------
        K : coo_matrix
            the asembled matrix
        """
        return coo_matrix(self.GetKvij(), shape=self.GetLinearSystemSize())

    def GetRhs(self):
        """ Get the right hand side term

        Returns
        -------
        rhs : ndarray
            Array with the values of the right hand side term
        """
        return self.rhs


def CheckIntegrityNormalFlux(GUI=False):
    from BasicTools.Containers.UnstructuredMeshCreationTools import CreateMeshOf

    points = [[0,0,0],[1,0,1],[0,1,1] ]
    mesh = CreateMeshOf(points,[[0,1,2]],EN.Triangle_3)
    mesh.ConvertDataForNativeTreatment()

    sdim = 3

    space = LagrangeSpaceGeo
    numbering = ComputeDofNumbering(mesh,space)
    dofs= ["u_" + str(i) for i in range(sdim)]
    spaces = [space]*sdim
    numberings = [numbering]*sdim

    ut = GetTestField("u",sdim)
    p = GetField("p",1)

    normal = GetNormal(3)

    wformflux = p*normal.T*ut

    constants = {"alpha":1.0}

    pressField = FEField("p",mesh,space,numbering)
    pressField.Allocate(1)

    print(mesh)
    elemfilt = ElementFilter(mesh=mesh) # all elements
    unkownFields = [FEField(dofs[n],mesh=mesh,space=spaces[n],numbering=numberings[n]) for n in range(len(dofs)) ]
    _matrix,F = IntegrateGeneral(mesh=mesh,wform=wformflux, constants=constants, fields=[pressField],
                    unkownFields = unkownFields,
                    elementFilter=elemfilt )
    if GUI :
        from BasicTools.Actions.OpenInParaView import OpenInParaView
        F.shape = (3,3)
        F = F.T
        mesh.nodeFields["normalflux"] =  F
        OpenInParaView(mesh)

    return "ok"

def CheckIntegrityKF(edim, sdim,testCase):
    from BasicTools.Containers.UnstructuredMeshCreationTools import CreateMeshOfTriangles, CreateMeshOf
    from BasicTools.FE.MaterialHelp import HookeIso

    if edim == 1:
        nu = 0.25
        #https://www.colorado.edu/engineering/CAS/courses.d/IFEM.d/IFEM.Ch20.d/IFEM.Ch20.pdf
        if sdim == 1:
            E = 1
            A = 1
            points = np.array([[0,],[2,],])
            L = np.sqrt(np.sum((points[1,:] - points[0,:])**2))
            K = np.array([[E],])

            KValidation = (E*A/L)*np.array([[1, -1],[-1, 1]])
            permut = None

        elif sdim == 2:
            E = 1000.
            A = 5.
            points = np.array([[0,0],[30,40], ])
            L = np.sqrt(np.sum((points[1,:] - points[0,:])**2))
            K = A*E*np.array([[1 ,1,0],[1,1 ,0],[0 ,0,0]])
            KValidation = np.array([[36,48,-36,-48],
                                 [48,64,-48,-64],
                                 [-36,-48,36,48],
                                 [-48,-64,48,64]])
            permut = [0,2,1,3]
            KValidation = KValidation[permut,:][:,permut]

        elif sdim == 3:
            points = np.array([[0,0,0],[2.,3.,6.], ])
            L = np.sqrt(np.sum((points[1,:] - points[0,:])**2))
            E = 343.
            A = 10.
            K = A*E*np.array([[1,1,1,0,0,0],
                               [1,1,1,0,0,0],
                               [1,1,1,0,0,0],
                               [0,0,0,0,0,0],
                               [0,0,0,0,0,0],
                               [0,0,0,0,0,0],])

            permut = [0,3,1,4,2,5]
            KValidation = np.array([[40,60,120,-40,-60,-120],
                                 [60,90,180,-60,-90,-180],
                                 [120,180,360,-120,-180,-360],
                                 [-40,-60,-120,40,60,120],
                                 [-60,-90,-180,60,90,180],
                                 [-120,-180,-360,120,180,360]])

            KValidation = KValidation[permut,:][:,permut]

        mesh = CreateMeshOf(points,[[0,1],],EN.Bar_2 )

    elif edim == 2:
        if sdim == 2:
            if testCase[0] =="A" :

                #http://www.unm.edu/~bgreen/ME360/2D%20Triangular%20Elements.pdf

                points = [[3,0],[3,2],[0,0],[0,2] ]
                #,[3,2,1][0,1,2]
                mesh = CreateMeshOfTriangles(points,[[0,1,2],[3,2,1]])


                E = 3.0/2
                nu = 0.25
                K = HookeIso(E,nu,dim=2)


                permut = [0,2,6,4,1,3,7,5]
                KValidation = np.array([[0.9833333333333333333,-0.5, -.45, .2, 0 ,0,-0.5333333333333333333, 0.3],
                                [-0.5,1.4,.3,-1.2,0,0,.2,-.2],
                                [-0.45,.3,0.9833333333333333333,0,-0.5333333333333333333,0.2,0,-0.5],
                                [.2,-1.2,0,1.4,.3,-.2,-0.5,0],
                                [0,0,-0.5333333333333333333,.3,0.983333333333333333,-0.5,-0.45,.2],
                                [0,0,0.2,-0.2,-0.5,1.4,.3,-1.2],
                                [-0.5333333333333333333,0.2,0.0,-0.5,-0.45,0.3,0.9833333333333333333,0],
                                [0.3,-0.2,-0.5,0,0.2,-1.2,0,1.4]       ])
                #                     ^^^
                #attention il y a un erreur dans le pdf  (ce termet est possitive dans le pdf)
                KValidation = KValidation[permut,:][:,permut]


            elif  testCase[0] == "B" :
                #https://www.colorado.edu/engineering/CAS/courses.d/IFEM.d/IFEM.Ch15.d/IFEM.Ch15.pdf
                #pages 15-11
                points = [[0,0],[3,1],[2,2]]
                mesh = CreateMeshOfTriangles(points,[[0,1,2],])
                #mesh.GetElementsOfType(EN.Triangle_3).tags.CreateTag("2D").SetIds(np.arange(mesh.GetElementsOfType(EN.Triangle_3).GetNumberOfElements() ) )

                K = np.array([[8,2,0],[2,8,0],[0,0,3]])*8
                permut = [0,2,4,1,3,5]

                KValidation = np.array([[11,5,-10,-2,-1,-3],
                                 [5,11,2,10,-7,-21],
                                 [-10,2,44,-20,-34,18],
                                 [-2,10,-20,44,22,-54],
                                 [-1,-7,-34,22,35,-15],
                                 [-3,-21,18,-54,-15,75]])
                KValidation = KValidation[permut,:][:,permut]

            else:
                raise RuntimeError


        elif sdim == 3:
            if testCase[0] == "A" :
                points = [[0,0,0],[6,-8,5],[6,2,3],[0,5,2] ]
                mesh = CreateMeshOf(points,[[0,1,2,3]],EN.Quadrangle_4)
                E = 3.0/2
                nu = 0.25
                K = HookeIso(E,nu,dim=sdim)
                mesh.GetElementsOfType(EN.Quadrangle_4).tags.CreateTag("2D").SetIds(np.arange(mesh.GetElementsOfType(EN.Quadrangle_4).GetNumberOfElements() ) )
                permut = [0,3,6,1,4,7,2,5,8]

            else:
                raise RuntimeError

    elif edim == 3:
        ## https://www.colorado.edu/engineering/CAS/courses.d/AFEM.d/AFEM.Ch09.d/AFEM.Ch09.pdf
        ## page  9-17
        points = [[2.,3.,4],[6,3,2],[2,5,1],[4,3,6]]
        mesh = CreateMeshOf(points,[[0,1,2,3]],EN.Tetrahedron_4)
        E = 480
        nu = 1./3.

        K = HookeIso(E,nu,dim=sdim)
        #mesh.GetElementsOfType(EN.Tetrahedron_4).tags.CreateTag("3D").SetIds(np.arange(mesh.GetElementsOfType(EN.Tetrahedron_4).GetNumberOfElements() ) )

        permut = [0, 3, 6, 9, 1, 4, 7,10,  2, 5, 8, 11]
        KValidation = np.array( [[745, 540, 120, -5, 30, 60, -270, -240, 0, -470, -330, -180],
                                 [540, 1720, 270, -120, 520, 210, -120, -1080, -60, -300, -1160, -420],
                                 [120, 270, 565, 0, 150, 175, 0, -120, -270, -120, -300, -470],
                                 [-5, -120, 0, 145, -90, -60, -90, 120, 0, -50, 90, 60],
                                 [30, 520, 150, -90, 220, 90, 60, -360, -60, 0, -380, -180],
                                 [60, 210, 175, -60, 90, 145, 0, -120, -90, 0, -180, -230],
                                 [-270, -120, 0, -90, 60, 0, 180, 0, 0, 180, 60, 0],
                                 [-240, -1080, -120, 120, -360, -120, 0, 720, 0, 120, 720, 240],
                                 [0, -60, -270, 0, -60, -90, 0, 0, 180, 0, 120, 180],
                                 [-470, -300, -120, -50, 0, 0, 180, 120, 0, 340, 180, 120],
                                 [-330, -1160, -300, 90, -380, -180, 60, 720, 120, 180, 820, 360],
                                 [-180, -420, -470, 60, -180, -230, 0, 240, 180, 120, 360, 520]])
        KValidation = KValidation[permut,:][:,permut]


    else :
        raise RuntimeError


    #CompureVolume(mesh)
    mesh.ConvertDataForNativeTreatment()
    space = LagrangeSpaceGeo
    numbering = ComputeDofNumbering(mesh,space)

    if sdim == 1:
        dofs = ["u"]
    else:
        dofs= ["u_" + str(i) for i in range(sdim)]

    spaces = [space]*sdim
    numberings = [numbering]*sdim

    from BasicTools.FE.SymWeakForm import Strain
    from BasicTools.FE.SymWeakForm import ToVoigtEpsilon
    from BasicTools.FE.WeakForms.NumericalWeakForm import SymWeakToNumWeak

    u = GetField("u",sdim)
    ut = GetTestField("u",sdim)

    weak = ToVoigtEpsilon(Strain(u,sdim)).T@K@ToVoigtEpsilon(Strain(ut,sdim))

    numericakWeakForm = SymWeakToNumWeak(weak)

    _rwf = numericakWeakForm.GetRightPart(dofs)

    lwf = numericakWeakForm.GetLeftPart(dofs)

    constants = {}
    fields  = []

    startt = time.time()

    elemFilt = ElementFilter(mesh,tag=(str(edim)+"D"))

    unkownFields = [FEField(dofs[n],mesh=mesh,space=spaces[n],numbering=numberings[n]) for n in range(len(dofs)) ]
    kInteg, _rhs = IntegrateGeneral(mesh=mesh,wform=lwf, constants=constants, fields=fields,
                    unkownFields = unkownFields,
                    elementFilter=elemFilt )

    stopt = time.time() - startt
    print(stopt)

    kDense = kInteg.todense()

    permut = []
    offset = 0
    for f in unkownFields:
        for p in range(mesh.GetNumberOfNodes()):
            permut.append(f.numbering.GetDofOfPoint(p)+offset)
        offset += f.numbering.size
    if permut is not None:
        kDense = kDense[:,permut][permut,:]

    error = np.sum(abs(kDense-KValidation))/(np.sum(abs(KValidation))  )

    if error > 1e-14 or error is np.nan:

        print((edim,sdim,testCase))
        print("K Validation")
        print(KValidation)
        print("K Calcul")
        print(kDense)

        print("ERROR : ")
        print(error)

        print(kDense-KValidation)
        print(numbering)

        return "KO"

    return "ok"

def CheckIntegrityComputeVolume(mesh):

    numbering = ComputeDofNumbering(mesh,LagrangeSpaceGeo)

    dofs= ["T"]
    spaces = [LagrangeSpaceGeo]
    numberings = [numbering]

    tField = GetField("T",1)
    F = GetField("F",1)
    tFieldTest = GetTestField("T",1)

    weakForm = tField.T*tFieldTest + F.T*tFieldTest

    constants = {}
    fields  = {}
    f = FEField("F",mesh,LagrangeSpaceGeo,numbering)
    f.Allocate(1)
    fields["F"] = f

    startt = time.time()
    unkownFields = [FEField(dofs[n],mesh=mesh,space=spaces[n],numbering=numberings[n]) for n in range(len(dofs)) ]
    K,F = IntegrateGeneral(mesh=mesh,wform=weakForm, constants=constants, fields=fields,
                    unkownFields = unkownFields, elementFilter=ElementFilter() )
    _stopt = time.time() - startt
    volk = np.sum(K)
    print("volume (k): " + str(volk))
    volf = np.sum(F)
    print("volume (f): " + str(volf))
    if abs(volk - volf) > 1e-15 :
        print(volk-volf)
        raise RuntimeError

def CheckIntegrityIntegrationWithIntegrationPointField(GUI=False):
    from BasicTools.FE.IntegrationsRules import LagrangeP1

    from BasicTools.Containers.UnstructuredMeshCreationTools import CreateCube
    mesh = CreateCube([2.,3.,4.],[-1.0,-1.0,-1.0],[2./10, 2./10,2./10])
    mesh.ConvertDataForNativeTreatment()
    space, numberings, _offset, _NGauss = PrepareFEComputation(mesh,numberOfComponents=1)

    rhoField = IPField("rho",mesh=mesh,rule=LagrangeP1)
    factor = .1
    rhoField.Allocate(factor)

    tField = GetField("T",1)
    rho = GetField("rho",1)
    tFieldTest = GetTestField("T",1)

    weakForm = tField.T*tFieldTest + rho.T*tFieldTest

    constants = {}
    fields = [ rhoField]
    unkownFields = [FEField("T",mesh=mesh,space=space,numbering=numberings[0]) ]

    startt = time.time()
    elemFilt = ElementFilter(mesh,tag="3D")
    K,F = IntegrateGeneral(mesh=mesh,
                    wform=weakForm,
                    constants=constants,
                    fields=fields,
                    unkownFields=unkownFields,
                    integrationRuleName="LagrangeP1",
                    elementFilter=elemFilt)

    intClass = IntegrationClass()
    intClass.SetMesh(mesh)
    intClass.SetOnlyEvaluation(False)
    intClass.SetElementFilter(elemFilt)
    intClass.SetConstants(constants)
    intClass.SetUnkownFields(unkownFields)
    intClass.SetTestFields(None)
    intClass.SetExtraFields(fields)
    intClass.SetIntegrationRule(integrationRuleName="LagrangeP1")
    intClass.SetWeakForm(weakForm)
    intClass.PreStartCheck()
    intClass.Allocate()
    intClass.Compute()
    matrixKII = intClass.GetK()
    vectorFII = intClass.GetRhs()

    _stopt = time.time() - startt
    volk = np.sum(K)
    print("volume (k): " + str(volk))
    print("volume class (k): " + str(np.sum(matrixKII)))
    volf = np.sum(F)
    print("volume (f): " + str(volf))
    print("volume class (f): " + str(np.sum(vectorFII)))

    if abs(volk*factor - volf) >=  volf/100000000:
        return "KO"

    volkII = np.sum(intClass.GetK())
    volfII = np.sum(intClass.GetRhs())

    if abs(volkII*factor - volfII) >=  volfII/100000000:
        return "KO"

    return "ok"



def CheckIntegrity(GUI=False):
    import BasicTools.FE.Integration as BTFEI
    if CheckIntegrityNormalFlux(GUI).lower() != "ok":
        return "Not ok in the Normal Calculation"
    if CheckIntegrityIntegrationWithIntegrationPointField() != "ok":
        return "Not ok in the integration with IPField"

    print("Normal Calculation OK")


    print("Integration with IPField OK")

    problems = [ (1,1,"A bars 1D"),
                 (1,2,"A bars 2D"),
                 (1,3,"A bars 3D"),
                 (2,2,"A Triangles in 2D"),
                 (2,2,"B Triangle in 2D"),
                 #(2,3,"A Triangle in 3D"),
                 (3,3,"A tet in 3D"),

                ]
    startt = time.time()

    for edim,sdim,testCase in problems:
        print("*-"*80)
        print("*-"*80)
        print((edim,sdim,testCase))

        print(" --- python  integration --")
        if CheckIntegrityKF(edim=edim,sdim = sdim,testCase=testCase).lower() !=  "ok":
            return "not ok python "
        else :
            print(" --- python  integration -- OK ")

    stopt = time.time() - startt
    print("Total time : ")
    print(stopt)
    print("ALL ok")
    return "ok"

if __name__ == '__main__':
    #print("Start")# pragma: no cover
    print(CheckIntegrity(False))# pragma: no cover
    #print("Stop")# pragma: no cover
    #print(CheckIntegrityConstantRectilinearIntegrationII())
