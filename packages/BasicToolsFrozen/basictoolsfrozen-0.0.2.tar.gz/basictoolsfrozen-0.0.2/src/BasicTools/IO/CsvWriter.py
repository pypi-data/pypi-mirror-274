# -*- coding: utf-8 -*-
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
#

"""CSV file reader
"""

import numpy as np
import os

from BasicTools.Helpers.TextFormatHelper import TFormat

from BasicTools.Containers.Filters import ElementFilter, NodeFilter
from BasicTools.IO.WriterBase import WriterBase as WriterBase

def WriteMeshToCsv(filename, baseMeshObject, PointFields = None, CellFields = None, GridFields= None, PointFieldsNames = None, CellFieldsNames=None, GridFieldsNames=None , nFilter= None, eFilter=None):
    """Function API for writing data into a CSV file

    Parameters
    ----------
    fileName : str
        name of the file to be written
    baseMeshObject : UnstructuredMesh
        support of the data to be written
    PointFields : list[np.ndarray], optional
        list of fields defined at the vertices of the mesh, by default None
    CellFields : list[np.ndarray], optional
        list of fields defined at the cells of the mesh, by default None
    GridFields : list[np.ndarray], optional
        list of grid data, by default None
    PointFieldsNames : list[str], optional
        list of field names defined at the vertices of the mesh, by default None
    CellFieldsNames : list[str], optional
        list of field names defined at the cells of the mesh, by default None
    GridFieldsNames : list[str], optional
        list of grid data names, by default None
    nFilter : NodeFilter, optional
        node filter to select a part of baseMeshObject, by default None
    eFilter : ElementFilter, optional
        element filter to select a part of baseMeshObject, by default None
    """
    if PointFields is None:
        PointFields = [];

    if CellFields  is None:
        CellFields   = [];

    if GridFields is None:
        GridFields  = [];

    if PointFieldsNames is None:
        PointFieldsNames  = [];

    if CellFieldsNames is None:
        CellFieldsNames  = [];

    if GridFieldsNames is None:
        GridFieldsNames  = [];

    writer = CsvWriter(filename)
    writer.nodalFilter = nFilter
    writer.elementFilter = eFilter
    writer.Open()
    writer.Write(baseMeshObject,
                 PointFields= PointFields,
                 CellFields = CellFields,
                 GridFields = GridFields,
                 PointFieldsNames = PointFieldsNames,
                 CellFieldsNames = CellFieldsNames,
                 GridFieldsNames = GridFieldsNames
                 )
    writer.Close()

class ElementOP():
    def __init__(self):
        self.cpt = 0
    def __call__(self,name,data,ids):
        self.cpt += len(ids)
        self.name = name
        self.id = ids[0]
        self.globalId = self.id + data.globaloffset
    def PostCondition(self,mesh):
        if self.cpt > 1 or self.cpt < 1:
            raise(Exception("Need a filter extracting only one element"))

class NodalOP():
    def __init__(self):
        self.cpt = 0
    def __call__(self,mesh,node,ids):
        self.cpt += len(ids)
        self.id = ids[0]
    def PostCondition(self,mesh):
        if self.cpt > 1 or self.cpt < 1:
            raise(Exception("Need a filter extracting only one element"))





class CsvWriter(WriterBase):
    """Class to writes a CSV file on disk
    """
    def __init__(self, fileName = None):
        super(CsvWriter,self).__init__()
        self.canHandleTemporal = True
        self.canHandleAppend = True
        self.canHandleMultidomain = False

        self.fileName = None;

        self.SetBinary(False)
        self.SetFileName(fileName)
        self.separator = ","
        self.nodalFilter = None
        self.elementFilter = None
        self.currentTime = 0.
        self.cpt = 0

    def __str__(self):
        res  = 'CsvWriter : \n'
        res += '   FileName : '+ str(self.fileName) +'\n'
        if self.isOpen():
            res += '   The File is Open!! \n'
        res += str(self.nodalFilter) + '\n'
        res += str(self.elementFilter)
        return res

    def SetETag(self,string):
        """Add the tag "string" to the class element filter

        Parameters
        ----------
        string : str
            element tag to add
        """
        self.elementFilter = ElementFilter(None)
        self.elementFilter.AddTag(string)

    def SetNTag(self,string):
        """Add the tag "string" to the class node filter

        Parameters
        ----------
        string : str
            node tag to add
        """
        self.nodalFilter = NodeFilter(None)
        self.nodalFilter.AddTag(string)


    def WriteHead(self, mesh, PointFieldsNames, CellFieldsNames, GridFieldsNames):
        """Function to write the header of the output CSV file

        Parameters
        ----------
        mesh : UnstructuredMesh
            support of the data to be written
        PointFieldsNames : list[str], optional
            list of field names defined at the vertices of the mesh, by default None
        CellFieldsNames : list[str], optional
            list of field names defined at the cells of the mesh, by default None
        GridFieldsNames : list[str], optional
            list of grid data names, by default None
        """
        sep = self.separator + " "

        self.writeText("Step")
        self.writeText(sep)

        self.nodalFields = []
        self.elementFields = []
        self.globalFields = []

        for name in GridFieldsNames:

            self.writeText(name)
            self.writeText(sep)

            self.globalFields.append(name)


        if self.nodalFilter is not None:
            self.nodalFilter.mesh = mesh

            op = NodalOP()
            try:
                self.nodalFilter.ApplyOnNodes(op)
            except IndexError:
                notFoundTags=set(self.nodalFilter.tags).difference(set(mesh.nodesTags.keys()))
                if len(notFoundTags):
                    raise Exception("Nodal Tag(s) not found in the mesh: ",list(notFoundTags))
                else:
                    emptyNodalTags=[tagname for tagname in self.nodalTags if len(mesh.nodesTags[tagname]) == 0]
                    raise Exception("Empty nodal tag(s) in mesh: ",emptyNodalTags)


            #conn = mesh.GetElementsOfType(op.name).connectivity[op.id,:]
            self.writeText("PointId")
            self.writeText(sep)
            for name in PointFieldsNames:
                self.writeText(name)
                self.nodalFields.append(name)
                self.writeText(sep)

        if self.elementFilter is not None:
            self.elementFilter.mesh = mesh
            op = ElementOP()

            self.elementFilter.ApplyOnElements(op)
            #conn = mesh.GetElementsOfType(op.name).connectivity[op.id,:]
            self.writeText("CellId")
            self.writeText(sep)
            self.writeText("CellGlobalId")
            self.writeText(sep)
            self.writeText("CellType")
            self.writeText(sep)

            nprint = False
            for name in CellFieldsNames:
                if nprint:
                    self.writeText(sep)
                self.writeText(name)
                self.elementFields.append(name)
                nprint = True


        self.writeText("\n")

    def Step(self, dt = 1.):
        """Function to increase current time by a time increment

        Parameters
        ----------
        dt : int, optional
            time increment, by default 1.
        """
        self.currentTime += dt

    def Write(self,baseMeshObject, PointFields = None, CellFields = None, GridFields= None, PointFieldsNames = None, CellFieldsNames= None, GridFieldsNames=None , Time= None, TimeStep = None, domainName=None):
        """Function to writes a CSV file on disk

        Parameters
        ----------
        fileName : str
            name of the file to be written
        baseMeshObject : UnstructuredMesh
            support of the data to be written
        PointFields : list[np.ndarray], optional
            list of fields defined at the vertices of the mesh, by default None
        CellFields : list[np.ndarray], optional
            list of fields defined at the cells of the mesh, by default None
        GridFields : list[np.ndarray], optional
            list of grid data, by default None
        PointFieldsNames : list[str], optional
            list of field names defined at the vertices of the mesh, by default None
        CellFieldsNames : list[str], optional
            list of field names defined at the cells of the mesh, by default None
        GridFieldsNames : list[str], optional
            list of grid data names, by default None
        Time : float, optional
            time at which the data is written, by default None
        TimeStep : float, optional
            number of the time step at which the data is written, by default None
        domainName : str, optional
            name of domain to write, by default None
        """

        sep = self.separator + " "

        if PointFields is None:
            PointFields = [];

        if CellFields  is None:
            CellFields   = [];

        if GridFields is None:
            GridFields  = [];

        if PointFieldsNames is None:
            PointFieldsNames  = [];

        if CellFieldsNames is None:
            CellFieldsNames  = [];

        if GridFieldsNames is None:
            GridFieldsNames  = [];

        if not self.isOpen() :
            if self.automaticOpen:
                self.Open()
            else:
                print(TFormat.InRed("Please Open The writer First!!!"))
                raise Exception


        if self.filePointer.tell() == 0:
            self.WriteHead(baseMeshObject,PointFieldsNames=PointFieldsNames,CellFieldsNames=CellFieldsNames,GridFieldsNames=GridFieldsNames)

        dt = 1
        if Time is not None:
            dt = Time - self.currentTime
        elif TimeStep is not None:
            dt = TimeStep

        if self.IsTemporalOutput():
            self.Step(dt)


        #self.currentTime
        self.writeText(str(self.cpt))
        self.writeText(sep)


        data = { a:b for a,b in zip(GridFieldsNames, GridFields) }

        for name in self.globalFields:
            if name in data:
                self.writeText(str(data[name]))
            else:
                self.writeText("nan")
            self.writeText(sep)


        if self.nodalFilter is not None:
            self.nodalFilter.mesh = baseMeshObject
            op = NodalOP()
            self.nodalFilter.ApplyOnNodes(op)
            #conn = mesh.GetElementsOfType(op.name).connectivity[op.id,:]
            self.writeText(str(op.id))
            self.writeText(sep)
            data = { a:b for a,b in zip(PointFieldsNames,PointFields) }
            for name in self.nodalFields:
                if name in data:
                    if len(data[name].shape) == 1:
                        self.writeText(str(data[name][op.id]))
                    else:
                        self.writeText(str(data[name][op.id,:]))
                else:
                    self.writeText("nan")
                self.writeText(sep)

        nprint = False
        if self.elementFilter is not None:
            self.elementFilter.mesh = baseMeshObject

            op = ElementOP()
            self.elementFilter.ApplyOnElements(op)
            #conn = mesh.GetElementsOfType(op.name).connectivity[op.id,:]
            self.writeText(str(op.id))
            self.writeText(sep)
            self.writeText(str(op.globalId))
            self.writeText(sep)
            self.writeText(str(op.name))
            self.writeText(sep)
            data = { a:b for a,b in zip(CellFieldsNames,CellFields) }
            for name in self.elementFields:
                if nprint:
                    self.writeText(sep)
                if name in data:
                    if len(data[name].shape) == 1:
                        self.writeText(str(data[name][op.globalId]))
                    else:
                        self.writeText(str(data[name][op.globalId,:]))
                else:
                    self.writeText("nan")
                nprint = True


        self.writeText("\n")

        self.filePointer.flush()
        self.cpt += 1

    def Close(sefl):
        pass

from BasicTools.IO.IOFactory import RegisterWriterClass
RegisterWriterClass(".csv",CsvWriter)


def CheckIntegrity(GUI=False):
    from BasicTools.Helpers.Tests import TestTempDir
    from BasicTools.Containers.UnstructuredMeshCreationTools import CreateMeshOfTriangles
    import BasicTools.Containers.ElementNames as EN

    tempdir = TestTempDir.GetTempPath()


    res = CreateMeshOfTriangles([[0.,0.,0],[1.,2.,3],[1, 3, 2]], np.array([[0,1,2]]))
    print(res)
    if GUI:
        res.SetGlobalDebugMode()

    elements = res.GetElementsOfType(EN.Bar_2)
    elements.AddNewElement([1,2],1)
    elements.tags.CreateTag("First_bar").SetIds([0])
    print(elements.tags.CreateTag("First_bar",False).GetIds())
    elements = res.GetElementsOfType(EN.Point_1)
    elements.AddNewElement([0],2)
    res.GetNodalTag("First_Point").AddToTag(0)

    nfilt = NodeFilter(res)
    nfilt.AddTag("First_Point")

    efilt = ElementFilter(res)
    efilt.AddTag("First_bar")

    WriteMeshToCsv(tempdir+"TestUnstructured.csv", res, PointFields = [np.array([1.,2,3]),res.nodes],
                    CellFields =[ np.array([1])] ,GridFields= [[0],  np.array([1,2,3]).astype(np.int64) ],
                    PointFieldsNames = ["PS","nodes"],
                    CellFieldsNames = ["CS"],
                    GridFieldsNames = ["GS", "GV"], nFilter=nfilt, eFilter=efilt)

    return 'ok'

if __name__ == '__main__':
    print(CheckIntegrity(GUI=True)) # pragma: no cover
