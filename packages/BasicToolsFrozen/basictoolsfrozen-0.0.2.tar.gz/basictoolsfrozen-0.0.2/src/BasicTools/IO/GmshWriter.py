# -*- coding: utf-8 -*-
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
#

"""Gmsh  File Writer (gmesh mesh files)
"""
from itertools import combinations

import numpy as np
import BasicTools.Containers.ElementNames as EN

from BasicTools.Containers.MeshBase import Tag as Tag
from BasicTools.IO.WriterBase import WriterBase as WriterBase
from BasicTools.NumpyDefs import PBasicFloatType, PBasicIndexType
from BasicTools.IO.GmshTools import gmshName,PermutationGmshToBasicTools
PermutationBasicToolsToGmsh = {key:np.argsort(value) for key, value in PermutationGmshToBasicTools.items() }

class OverlappingTagException(Exception):
    pass

def WriteMeshToGmsh(filename, mesh, useOriginalId = False, tagMapping = None):
    """Function API for writing data into a gmsh file

    Parameters
    ----------
    fileName : str
        name of the file to be written
    mesh : UnstructuredMesh
        the mesh to be written
    useOriginalId : bool, optional
        If True, Original Id for the number of nodes and elements are used
        (the user is responsible of the consistency of this data), by default False
    tagMapping : dict, optional
        tags of geometric objects defined in the mesh, by default None
    """
    OW = GmshWriter()
    if tagMapping is not None:
        OW.tagMapping=tagMapping
    OW.Open(filename)
    OW.Write(mesh, useOriginalId = useOriginalId)
    OW.Close()

class GmshWriter(WriterBase):
    """Class to writes a gmsh file on disk
    """
    def __init__(self):
        super(GmshWriter,self).__init__()
        self.SetBinary(False)
        self.canHandleBinaryChange = False
        self.tagMapping=dict()
        self.userRequiredTags=[]

    def __str__(self):
        res  = 'GmshWriter : \n'
        res += '   FileName : '+str(self.fileName)+'\n'
        return res

    def SetFileName(self, fileName):
        """Sets the fileName parameter of the class

        Parameters
        ----------
        string : str
            fileName to set
        """
        self.fileName = fileName

    def Write(self,meshObject,useOriginalId=False,PointFieldsNames=None,PointFields=None,CellFieldsNames=None,CellFields=None):
        """Function to writes a gmsh file on disk

        Parameters
        ----------
        meshObject : UnstructuredMesh
            support of the data to be written
        useOriginalId : bool, optional
            If True original ids of vertices and elements, by default False
        PointFieldsNames : _type_, optional
            Not Used, by default None
        PointFields : _type_, optional
            Not Used, by default None
        CellFieldsNames : _type_, optional
            Not Used, by default None
        CellFields : _type_, optional
            Not Used, by default None

        Raises
        ------
        OverlappingTagException
            when at least 2 tags are overlapping
        """


        self.filePointer.write("$MeshFormat\n")
        self.filePointer.write("2.2 0 8\n")
        self.filePointer.write("$EndMeshFormat\n")
        self.filePointer.write("$Nodes\n")
        numberofpoints = meshObject.GetNumberOfNodes()
        self.filePointer.write(f"{numberofpoints}\n")

        posn = meshObject.GetPosOfNodes()
        if useOriginalId:
            for n in range(numberofpoints):
                self.filePointer.write("{} ".format(int(meshObject.originalIDNodes[n])))
                posn[np.newaxis,n,:].tofile(self.filePointer, sep=" ")
                self.filePointer.write("\n")
        else:
            for n in range(numberofpoints):
                self.filePointer.write(f"{n+1} ")
                posn[np.newaxis,n,:].tofile(self.filePointer, sep=" ")
                self.filePointer.write("\n")
        self.filePointer.write("$EndNodes\n")
        self.filePointer.write("$Elements\n")
        self.filePointer.write(f"{meshObject.GetNumberOfElements()}\n")

        cpt = 1

        celltags = meshObject.GetNamesOfElemTags()
        elements = meshObject.elements
        if self.tagMapping:
            self.userRequiredTags=self.tagMapping.keys()
            minTagVal=max(self.tagMapping.values())+1
            notMappedTagNames=sorted(list(set(celltags)-set(self.tagMapping.keys())))
            notMappedTagsValue=np.arange(minTagVal,minTagVal+len(notMappedTagNames),dtype=int)
            notMappedTagsMapping=dict(zip(notMappedTagNames, notMappedTagsValue))
            self.tagMapping={**notMappedTagsMapping,**self.tagMapping}

        # tagcounter = 2
        #for tagname in celtags:
        for elementContainer in elements:
            elemtype = gmshName[elementContainer]
            #try:
            data = meshObject.elements[elementContainer]
            phyGeoTags=np.ones(data.GetNumberOfElements(), PBasicIndexType)

            elemIdsInTags={tagName:data.tags[tagName].GetIds() for tagName in self.userRequiredTags if tagName in data.tags}

            if elemIdsInTags.keys():
                tagPairs=list(combinations(elemIdsInTags.keys(), 2))
                for tag1,tag2 in tagPairs:
                    idsTag1,idsTag2=elemIdsInTags[tag1],elemIdsInTags[tag2]
                    commonIds=np.intersect1d(idsTag1,idsTag2)
                    if commonIds.size > 0:
                        print("Common element ids for pair "+str(tag1)+","+str(tag2)+" are: ",str(commonIds))
                        raise OverlappingTagException("At least 2 tags are overlapping, cannot be handled properly naturally in .msh 2.2 format")

            for tagName in self.tagMapping.keys():
                if tagName in data.tags:
                    elemIds = data.tags[tagName].GetIds()
                    phyGeoTags[elemIds] = self.tagMapping[tagName]
            if useOriginalId:
                for i in range(data.GetNumberOfElements() ):
                    self.filePointer.write(f"{data.originalIds[i]} {elemtype} 2 {phyGeoTags[i]} {phyGeoTags[i]} ")
                    self.filePointer.write(" ".join([str(meshObject.originalIDNodes[x]) for x in data.connectivity[i,:].ravel()]))
                    cpt += 1
                    self.filePointer.write("\n")
            else:
                #for connectivity in meshObject.elements[elementContainer].connectivity[meshObject.elements[elementContainer].tags[tagname].id-1]:
                for i in range(data.GetNumberOfElements() ):
                    connectivity = data.connectivity[i,:]
                    if elementContainer in PermutationBasicToolsToGmsh:
                        connectivity = [connectivity[x] for x in PermutationBasicToolsToGmsh[elementContainer]]
                    self.filePointer.write(f"{cpt} {elemtype} 2 {phyGeoTags[i]} {phyGeoTags[i]} ")
                    self.filePointer.write(" ".join([str(x+1) for x in connectivity]))
                    cpt += 1
                    self.filePointer.write("\n")
            #except KeyError:
            #  continue
            #tagcounter += 1

        self.filePointer.write("$EndElements\n")

from BasicTools.IO.IOFactory import RegisterWriterClass
RegisterWriterClass(".msh",GmshWriter)

def CheckIntegrity_OriginalIdsForTags():

    import os
    from BasicTools.Helpers.Tests import TestTempDir
    tempdir = TestTempDir.GetTempPath()

    from BasicTools.Containers.UnstructuredMeshCreationTools import CreateMeshOfTriangles
    import BasicTools.Containers.UnstructuredMesh as UM

    mymesh = UM.UnstructuredMesh()
    mymesh.nodes = np.array([[0.00000000001,0,0],[1,0,0],[0,1,0],[1,1,0]],dtype=PBasicFloatType)
    mymesh.originalIDNodes = np.array([1, 3, 4, 5],dtype=PBasicIndexType)


    mymesh.nodesTags.CreateTag("coucou").AddToTag(0)

    tris = mymesh.GetElementsOfType('tri3')
    tris.AddNewElement([0,1,2],0)
    tris.AddNewElement([2,1,3],3)
    tris.originalIds = np.array([3, 5],dtype=PBasicIndexType)

    mymesh.AddElementToTagUsingOriginalId(3,"Tag1")
    mymesh.AddElementToTagUsingOriginalId(5,"Tag3")

    OW = GmshWriter()
    tagMapping=dict(zip(["Tag1","Tag3"], [10,30]))
    OW.tagMapping=tagMapping

    print(OW)
    OW.Open(tempdir+os.sep+"Test_GmshWriter.geof")
    OW.Write(mymesh, useOriginalId=False)
    OW.Close()


    print(mymesh)
    WriteMeshToGmsh(tempdir+os.sep+"Test_GmshWriter_II.geof", mymesh,useOriginalId=True,tagMapping=tagMapping)

    return "ok"

def CheckIntegrity_SeparatedTags():

    import os
    from BasicTools.Helpers.Tests import TestTempDir
    tempdir = TestTempDir.GetTempPath()
    from BasicTools.Containers.UnstructuredMeshCreationTools import CreateMeshOfTriangles

    nodes = np.array([[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0.5,0.5,0]],dtype=PBasicFloatType)
    elements = np.array([[0,1,4],[1,2,4],[2,3,4],[3,4,0]])
    mesh= CreateMeshOfTriangles(nodes,elements)

    mesh.AddElementToTag(0,"ZTag1")
    mesh.AddElementToTag(1,"ZTag2")
    mesh.AddElementToTag(2,"ZTag3")

    fileName=tempdir+os.sep+"Test_GmshWriterBasic.msh"

    print(mesh)
    OW = GmshWriter()
    OW.tagMapping=dict(zip(["ZTag1","ZTag2","ZTag3"], [18,100,230]))
    OW.Open(fileName)
    OW.Write(mesh, useOriginalId=False)
    OW.Close()

    expected="$MeshFormat\
    2.2 0 8\
    $EndMeshFormat\
    $Nodes\
    5\
    1 0.0 0.0 0.0\
    2 1.0 0.0 0.0\
    3 1.0 1.0 0.0\
    4 0.0 1.0 0.0\
    5 0.5 0.5 0.0\
    $EndNodes\
    $Elements\
    4\
    1 2 2 18 18 1 2 5\
    2 2 2 100 100 2 3 5\
    3 2 2 230 230 3 4 5\
    4 2 2 231 231 4 5 1\
    $EndElements"
    expected= " ".join(expected.split())
    actual=" ".join(open(fileName).read().split('\n'))
    if actual.strip() == expected.strip():
        return "ok"

def CheckIntegrity_OverlappingTags():
    import os
    from BasicTools.Helpers.Tests import TestTempDir
    tempdir = TestTempDir.GetTempPath()

    from BasicTools.Containers.UnstructuredMeshCreationTools import CreateMeshOfTriangles

    nodes = np.array([[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0.5,0.5,0]],dtype=PBasicFloatType)
    elements = np.array([[0,1,4],[1,2,4],[2,3,4],[3,4,0]])
    mesh= CreateMeshOfTriangles(nodes,elements)

    mesh.AddElementToTag(0,"ZTag1")
    mesh.AddElementToTag(1,"ZTag1")
    mesh.AddElementToTag(1,"ZTag2")
    mesh.AddElementToTag(2,"ZTag2")
    mesh.AddElementToTag(2,"ZTag3")

    fileName=tempdir+os.sep+"Test_GmshWriterBasic.msh"

    print(mesh)
    OW = GmshWriter()
    OW.tagMapping=dict(zip(["ZTag1","ZTag2","ZTag3"], [18,100,230]))
    OW.Open(fileName)
    try:
        OW.Write(mesh, useOriginalId=False)
    except OverlappingTagException:
        OW.Close()
        return "ok"

    return "ok"

def CheckIntegrity():
    totest = [
    CheckIntegrity_SeparatedTags,
    CheckIntegrity_OriginalIdsForTags,
    CheckIntegrity_OverlappingTags
            ]

    for test in totest:
        res =  test()
        if  res.lower() != "ok" :
            return res

    return "OK"

if __name__ == '__main__':
    print(CheckIntegrity())# pragma: no cover
