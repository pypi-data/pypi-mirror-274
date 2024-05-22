# -*- coding: utf-8 -*-
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
#

from BasicTools.Containers import Filters
import BasicTools.Containers.ElementNames as EN


__cache__ = {}
__cacheSize__ = 1
numberingAlgorithm = "CppBase"
#numberingAlgorithm = "NumpyBase"
#numberingAlgorithm = "DictBase"

def GetNumberingFromCache(mesh,space,elementFilter=None,discontinuous=False,fromConnectivity=False):
    return None
    key = (id(mesh),id(space),id(elementFilter),discontinuous,fromConnectivity)
    return __cache__.get(key,None)

def SetNumberingToCache(obj, mesh,space,elementFilter=None,discontinuous=False,fromConnectivity=False):
    if len(__cache__) >=  __cacheSize__:
        for k in __cache__:
            del __cache__[k]
            break
    key = (id(mesh),id(space),id(elementFilter),discontinuous,fromConnectivity)
    __cache__[key] = obj

def ComputeDofNumbering(mesh,Space,dofs=None,fromConnectivity=False,elementFilter=None,discontinuous=False):

    if dofs is None:
        cachedData = GetNumberingFromCache(mesh=mesh, space=Space, fromConnectivity=fromConnectivity, elementFilter=elementFilter, discontinuous=discontinuous )
    if cachedData is not None:
        return cachedData

    global numberingAlgorithm
    res = None
    if numberingAlgorithm == "CppBase":
        try:
            from BasicTools.FE.Numberings.NativeDofNumbering import NativeDofNumbering
            res = NativeDofNumbering()
        except:
           numberingAlgorithm = "NumpyBase"
           print("Warning CppBase Numbering non available (missing compilation) Using NumpyBase")

    if numberingAlgorithm == "NumpyBase":
        from BasicTools.FE.Numberings.DofNumberingNumpy import DofNumberingNumpy
        res = DofNumberingNumpy()
    elif numberingAlgorithm == "DictBase":
        from BasicTools.FE.Numberings.DofNumberingDict import DofNumberingDict
        res = DofNumberingDict()
    elif res == None:
        raise(Exception(f"Numbering algorithm of type {numberingAlgorithm} not available "))


    if fromConnectivity:
        if dofs is not None or elementFilter is not None or discontinuous:
           raise(Exception("cant take dofs, sign, discontinuous or elementFilter different from the default values"))
        from BasicTools.FE.Spaces.FESpaces import LagrangeSpaceGeo
        #check the compatibility of the spaces, this is not perfect, the user is responsible of putting the shape function in the same order
        # as the nodes of the reference element
        for k in mesh.elements.keys():
            Space[k].Create()
            if Space[k].fromConnectivityCompatible == True or Space[k].GetNumberOfShapeFunctions() == EN.numberOfNodes[k]  :
                continue
            raise Exception(f"Incompatible case! Can't use a non compatible space {(type(Space[k]))} and fromConnectivity at the same time")

        res.ComputeNumberingFromConnectivity(mesh, Space)
        SetNumberingToCache(res,mesh=mesh, space=Space, fromConnectivity=fromConnectivity, elementFilter=elementFilter, discontinuous=discontinuous )
        return res
    else:
        if dofs is not None:
            res = dofs

        res.ComputeNumberingGeneral(mesh=mesh, space=Space, elementFilter=elementFilter, discontinuous=discontinuous )
        SetNumberingToCache(res,mesh=mesh, space=Space, fromConnectivity=fromConnectivity, elementFilter=elementFilter, discontinuous=discontinuous )

        return res

def CheckIntegrity(GUI=False):
    import BasicTools.FE.DofNumbering  as DN

    from BasicTools.Containers.UnstructuredMeshCreationTools import CreateCube

    res2 = CreateCube([2,2,2],[-1.0,-1.0,-1.0],[2./46, 2./46,2./46])

    from BasicTools.FE.Spaces.FESpaces import LagrangeSpaceGeo, LagrangeSpaceP0, LagrangeSpaceP1, LagrangeSpaceP2, ConstantSpaceGlobal

    spacesToTest = { "ConstantSpaceGlobal":ConstantSpaceGlobal,"LagrangeSpaceGeo":LagrangeSpaceGeo, "LagrangeSpaceP0":LagrangeSpaceP0, "LagrangeSpaceP1":LagrangeSpaceP1, "LagrangeSpaceP2":LagrangeSpaceP2 }


    from BasicTools.FE.Spaces.IPSpaces import GenerateSpaceForIntegrationPointInterpolation
    from BasicTools.FE.IntegrationsRules import GetRule
    irule = GetRule(ruleName="LagrangeP1")
    gaussSpace = GenerateSpaceForIntegrationPointInterpolation(irule)
    spacesToTest["gaussSpace"] =gaussSpace
    import time

    def printData(numbering,st):
        for k,v in res2.elements.items():
            print(k,numbering.get(k,None))
        print(f"numbering.size = {numbering.size}")
        print(f" time : {time.time()-st}" )

    for spaceName, space in spacesToTest.items():
        print("*************************** {} {}*******************************************".format(DN.numberingAlgorithm, spaceName))
        # on a tag
        print(f"vvvvvvvvvvv {spaceName} tag vvvvvvvvvvvvvvv")
        st = time.time()
        numbering = DN.ComputeDofNumbering(res2,space,elementFilter= Filters.ElementFilter(mesh=res2,tag="X0") )
        printData(numbering,st)

        # all
        print("----------------------{} all -----------------------------".format(spaceName))
        st = time.time()
        numbering = DN.ComputeDofNumbering(res2,space)
        printData(numbering,st)

        if space is LagrangeSpaceGeo:
            # from connectivity
            print("----------------------{} from connectivity -----------------------------".format(spaceName))
            st = time.time()
            numbering = DN.ComputeDofNumbering(res2, space,fromConnectivity=True)
            printData(numbering,st)

        # 3D using filter
        print("----------------------{} 3D filter-----------------------------".format(spaceName))
        st = time.time()
        numbering = DN.ComputeDofNumbering(res2,space,elementFilter=Filters.ElementFilter(mesh=res2,dimensionality=3) )
        printData(numbering,st)
    return "ok"

def CheckIntegrityUsingAlgo(algo,GUI=False):

    import BasicTools.FE.DofNumbering  as DN
    tmpAlgo = DN.numberingAlgorithm
    DN.numberingAlgorithm = algo
    try:
        res = DN.CheckIntegrity(GUI)
        DN.numberingAlgorithm = tmpAlgo
        return res
    except:
        DN.numberingAlgorithm = tmpAlgo
        raise

if __name__ == '__main__':
    print(CheckIntegrity(True))# pragma: no cover
