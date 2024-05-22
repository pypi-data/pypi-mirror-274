# -*- coding: utf-8 -*-
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
#

"""Xdmf file writer
"""

import numpy as np
import os

from BasicTools.Helpers.TextFormatHelper import TFormat

import BasicTools.Containers.ElementNames as EN
from BasicTools.IO.WriterBase import WriterBase as WriterBase
from BasicTools.Helpers.MPIInterface import MPIInterface as MPI
from BasicTools.NumpyDefs import PBasicIndexType
from BasicTools.IO.XdmfTools import XdmfName,XdmfNumber, HasHdf5Support

def ArrayToString(data):
    return " ".join(str(x) for x in data)


#* Xdmf supports the following topology types:
# *   NoTopologyType
# *   Polyvertex - Unconnected Points
# *   Polyline - Line Segments
# *   Polygon - N Edge Polygon
# *   Triangle - 3 Edge Polygon
# *   Quadrilateral - 4 Edge Polygon
# *   Tetrahedron - 4 Triangular Faces
# *   Wedge - 4 Triangular Faces, Quadrilateral Base
# *   Hexahedron - 6 Quadrilateral Faces
# *   Edge_3 - 3 Node Quadratic Line
# *   Triangle_6 - 6 Node Quadratic Triangle
# *   Quadrilateral_8 - 8 Node Quadratic Quadrilateral
# *   Quadrilateral_9 - 9 Node Bi-Quadratic Quadrilateral
# *   Tetrahedron_10 - 10 Node Quadratic Tetrahedron
# *   Pyramid_13 - 13 Node Quadratic Pyramid
# *   Wedge_15 - 15 Node Quadratic Wedge
# *   Wedge_18 - 18 Node Bi-Quadratic Wedge
# *   Hexahedron_20 - 20 Node Quadratic Hexahedron
# *   Hexahedron_24 - 24 Node Bi-Quadratic Hexahedron
# *   Hexahedron_27 - 27 Node Tri-Quadratic Hexahedron
# *   Hexahedron_64 - 64 Node Tri-Cubic Hexahedron
# *   Hexahedron_125 - 125 Node Tri-Quartic Hexahedron
# *   Hexahedron_216 - 216 Node Tri-Quintic Hexahedron
# *   Hexahedron_343 - 343 Node Tri-Hexic Hexahedron
# *   Hexahedron_512 - 512 Node Tri-Septic Hexahedron
# *   Hexahedron_729 - 729 Node Tri-Octic Hexahedron
# *   Hexahedron_1000 - 1000 Node Tri-Nonic Hexahedron
# *   Hexahedron_1331 - 1331 Node Tri-Decic Hexahedron
# *   Hexahedron_Spectral_64 - 64 Node Spectral Tri-Cubic Hexahedron
# *   Hexahedron_Spectral_125 - 125 Node Spectral Tri-Quartic Hexahedron
# *   Hexahedron_Spectral_216 - 216 Node Spectral Tri-Quintic Hexahedron
# *   Hexahedron_Spectral_343 - 343 Node Spectral Tri-Hexic Hexahedron
# *   Hexahedron_Spectral_512 - 512 Node Spectral Tri-Septic Hexahedron
# *   Hexahedron_Spectral_729 - 729 Node Spectral Tri-Octic Hexahedron
# *   Hexahedron_Spectral_1000 - 1000 Node Spectral Tri-Nonic Hexahedron
# *   Hexahedron_Spectral_1331 - 1331 Node Spectral Tri-Decic Hexahedron
#  *   Mixed - Mixture of Unstructured Topologies


def WriteMeshToXdmf(filename,
                    baseMeshObject,
                    PointFields = None,
                    CellFields = None,
                    GridFields= None,
                    IntegrationPointData=None,
                    PointFieldsNames = None,
                    CellFieldsNames=None,
                    GridFieldsNames=None,
                    IntegrationPointDataNames=None,
                    IntegrationRule=None,
                    Binary= True,
                    HDF5 = True):
    """Function API for writing mesh in the xdmf format file.

    Parameters
    ----------
    fileName : str
        name of the file to be written
    baseMeshObject : UnstructuredMesh
        the mesh to be written
    PointFields : list[np.ndarray], optional
        fields to write defined at the vertices of the mesh, by default None
    CellFields : list[np.ndarray], optional
        fields to write defined at the elements of the mesh, by default None
    GridFields : list[np.ndarray], optional
        grid fields to write, by default None
    IntegrationPointData : list[np.ndarray], optional
        fields defined at the integration points, by default None
    PointFieldsNames : list[str], optional
        names of the fields to write defined at the vertices of the mesh, by default None
    CellFieldsNames : list[str], optional
        names of the fields to write defined at the elements of the mesh, by default None
    GridFieldsNames : list[str], optional
        names of the grid fields to write, by default None
    IntegrationPointDataNames : list[str], optional
        names of the fields defined at the integration points, by default None
    IntegrationRule : dict[IntegrationRuleType], optional
        integration rules associated to the integration point data, by default None
    Binary : bool, optional
        if True, file is written as binary, by default True
    HDF5 : bool, optional
        if True, file is written as hdf5 format, by default True
    """

    if PointFields is None:
        PointFields = []

    if CellFields  is None:
        CellFields   = []

    if GridFields is None:
        GridFields  = []

    if PointFieldsNames is None:
        PointFieldsNames  = []

    if CellFieldsNames is None:
        CellFieldsNames  = []

    if GridFieldsNames is None:
        GridFieldsNames  = []

    if IntegrationPointData is None:
        IntegrationPointData  = []

    if IntegrationPointDataNames is None:
        IntegrationPointDataNames  = []

    writer = XdmfWriter(filename)
    writer.SetBinary(Binary)
    writer.SetHdf5(HDF5)
    writer.Open()
    writer.Write(baseMeshObject,
                PointFields= PointFields,
                CellFields = CellFields,
                GridFields = GridFields,
                IntegrationPointData=IntegrationPointData,
                PointFieldsNames = PointFieldsNames,
                CellFieldsNames = CellFieldsNames,
                GridFieldsNames = GridFieldsNames,
                IntegrationPointDataNames=IntegrationPointDataNames,
                IntegrationRule=IntegrationRule,
                )
    writer.Close()
#

class InMemoryFile():
    """
    Helper class to write the xmf part of the file into memory
    """
    def __init__(self,saveFilePointer):
        self.data = ""
        self.saveFilePointer = saveFilePointer
    def write(self,data):
        self.data += data
    def tell(self):
        return 0
    def seek(self,pos):
        return 0
    def close(self):
        pass
    def flush():
        pass

class BinaryStorage(object):
    """Class to deal with binary storage"""
    def __init__(self,data=None, filePointer=None):
        self.filename = ""
        self.offset = 0
        self.type = None
        self.itemSize = 0
        self.vectorSize = 0
        self.usedByNInstances = 0
        if data is not None:
            self.usedByNInstances += 1
            self.type = data.dtype
            self.itemSize = data.dtype.itemsize
            self.vectorSize = data.size

        if filePointer is not None:
            self.filename = filePointer.name
            self.offset = filePointer.tell()

    def __str__(self):
        return str(self.vectorSize) +":"+str(self.usedByNInstances)

    def ChangePathOfBinaryStorage(self,newPath):
        import os
        self.filename = newPath + os.sep + os.path.basename(self.filename)

    def GetData(self):
        f = open(self.filename,'rb')
        f.seek(self.offset,0)
        data = np.fromfile(f,self.type,self.vectorSize,sep="")
        f.close()
        return data

    def UpdateHeavyStorage(self,data):
        if self.usedByNInstances > 1:
            raise Exception("This pointer is used for more than 1 field please (overwrite or setup the writer with the option maxStorageSize=0")

        if data.size != self.vectorSize:
            raise Exception("Size of data and storage not compatible")

        f = open(self.filename,'r+b')
        f.seek(self.offset,0)
        data.astype(self.type).ravel().tofile(f)
        f.close()

class XdmfWriter(WriterBase):
    """
    Class to Write Xdmf files for:
        - classic finite element solutions
        - domain decomposition problem (multi mesh)
        - transient solution (the mesh changes in time)
        - solution written in parafac format (monolithic or in ddm mpi)
    """


    def __init__(self, fileName = None):
        super(XdmfWriter,self).__init__()
        self.canHandleTemporal = True
        self.canHandleAppend = True
        self.canHandleMultidomain = True

        self.fileName = None
        self.timeSteps = []
        self.parafacCpt = 0
        self.ddmCpt = 0
        self.currentTime = 0
        self.__XmlSizeLimit = 0
        self.__chunkSize = 2**30
        self.automaticOpen = False

        try:
            import h5py
            self.__isHdf5 = True
        except:
            self.__isHdf5 = False

        self.__hdf5FileName = ""
        self.__hdf5FileNameOnly = None
        self.__hdf5FilePointer = None
        self.__hdf5NameCpt = 0

        self.SetBinary(True)
        self.__binFileName = ""
        self.__filePointer = None
        #self.__isOpen = False
        self.__binaryCpt = 0
        self.__hdf5cpt = 0
        self.__binFileCounter = 0
        self.__hdf5FileCounter = 0
        self.__keepXmlFileInSaneState = True
        self.__isParafacFormat = False

        #set to off is you what to put the time at the end of the temporal grid
        #keep this option True to be compatible with the XDMF3 reader of ParaView
        self.__printTimeInsideEachGrid = True

        self.SetFileName(fileName)
        self.pointFieldsStorage = {}
        self.cellFieldsStorage = {}
        self.gridFieldsStorage = {}
        self.ipStorage = {}
        self.globalStorage = {}
        self.maxStorageSize = 50

    def IsHdf5(self):
        return self.GetHdf5()

    def SetBinary(self, val = True):
        """Sets the binary status of the file to read

        Parameters
        ----------
        val : bool, optional
            if True, sets the file to read as binary, by default True
        """
        super(XdmfWriter,self).SetBinary(val)

    def isBinary(self):
        return super().isBinary() and not self.__isHdf5

    def GetHdf5(self):
        return self.__isHdf5 and super().isBinary()

    def SetHdf5(self, val=True):
        if val :
            self.SetBinary(True)

        try:
            import h5py
            self.__isHdf5 = val
        except:
            self.__isHdf5 = False
            if val:
                print("h5py not available using binary file for output")

    def SetChunkSize(self,size):
        self.__chunkSize = size

    def __str__(self):
        res  = 'XdmfWriter : \n'
        res += '   FileName : '+ str(self.fileName) +'\n'
        res += '   isParafacFormat : '+ ('True' if self.__isParafacFormat else "False") +'\n'
        if self.isBinary():
            res += '   Binary output Active \n'
            if self.__binFileName is not None:
                res += '   Binary FileName : '+ self.__binFileName +'\n'
        if self.IsHdf5():
            res += '   Hdf5 output Active \n'
            res += '   Hdf5 FileName : '+ self.__hdf5FileName +'\n'
        if self.IsTemporalOutput():
            res += '   Temporal output Active \n'
            res += '   TimeSteps : '+ str(self.timeSteps) + '\n'
        if self.isOpen():
            res += '   The File is Open!! \n'
        return res

    def SetFileName(self, fileName ):
        """Sets the fileName parameter of the class

        Parameters
        ----------
        string : str
            fileName to set
        """
        if fileName is None :
            self.fileName = None
            self.__path = None
            return

        self.fileName = fileName
        self.__path  = os.path.abspath(os.path.dirname(fileName))
        self.binFileCounter = 0
        self.NewBinaryFilename()
        self.NewHdf5Filename()

    def SetParafac(self,val = True):
        self.__isParafacFormat = val

    def IsParafacOutput(self):
        return self.__isParafacFormat

    def NewBinaryFilename(self):
        name = os.path.splitext(os.path.abspath(self.fileName))[0]
        name += "" +str(self.__binFileCounter)
        if MPI.IsParallel():
            name += "D"+ str(MPI.Rank())
        name += ".bin"

        self.__binFileName = name
        self.__binFileNameOnly = os.path.basename(self.__binFileName)
        self.__binFileCounter +=1

    def NewHdf5Filename(self):
        name = os.path.splitext(os.path.abspath(self.fileName))[0]
        name += "" +str(self.__hdf5FileCounter)
        if MPI.IsParallel():
            name += "D"+ str(MPI.Rank())
        name += ".h5"

        self.__hdf5FileName = name
        self.__hdf5FileNameOnly = os.path.basename(self.__hdf5FileName)
        self.__hdf5FileCounter +=1

    def Step(self, dt = 1):
        self.currentTime += dt
        self.timeSteps.append(self.currentTime)


    def SetXmlSizeLimit(self,val):
        self.__XmlSizeLimit= val

    def Open(self, filename = None):
        """Open file for writing

        Parameters
        ----------
        filename : str, optional
            name of the file to write
        """

        # we don't use the open from WriterBase because the set binary is used
        # for the .bin file and not for the .xdmf file

        if self.isOpen() :
            print(TFormat.InRed("The file is already open !!!!!"))
            return

        if filename is not None:
            self.SetFileName(filename)

        ## we use unbuffered so we can repairer broken files easily
        try :
            # in python 3 we cant use unbuffered  text I/O (bug???)
            #self.filePointer = open(self.fileName, 'w',0)
            if self.InAppendMode():
                if self.isBinary() == False:
                    raise(Exception("Append Mode only works in binary mode") )

                self.filePointer = open(self.fileName, 'r+')
                self.filePointer.seek(-100,2)

                lines = self.filePointer.readlines()
                for line in lines:
                    if line.find("<!--Temporal") != -1:
                        l = line.find('pos="')
                        r = line.find('" ',l+1)
                        pos = int(line[l+5:r])


                        #__binFileCounter
                        l = line.find('ter="')
                        r = line.find('" ',l+1)
                        binFileCounter = int(line[l+5:r])

                        self.NewBinaryFilename()
                        self.__binaryFilePointer = open (self.__binFileName, "wb")
                        self.__binaryCpt = 0

                        #time
                        l = line.find('ime="')
                        r = line.find('" ',l+1)
                        currentTime = float(line[l+5:r])

                        self.filePointer.seek(pos)
                        self._isOpen = True
                        self.__binFileCounter = binFileCounter
                        self.currentTime = currentTime
                        return
                raise Exception("Unable Open file in append mode ")
            else:
                mpi = MPI()
                if mpi.IsParallel():
                    self.__keepXmlFileInSaneState = False
                    if mpi.rank > 0:
                        self.filePointer = InMemoryFile(self.filePointer)
                    else:
                        self.filePointer = open(self.fileName, 'w')
                else:
                    self.filePointer = open(self.fileName, 'w')

        except: # pragma: no cover
            print(TFormat.InRed("Error File Not Open"))
            raise

        self._isOpen = True

        self.filePointer.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self.filePointer.write('<Xdmf xmlns:xi="http://www.w3.org/2001/XInclude" Version="2.92">\n')
        self.filePointer.write('<Domain>\n')

        if self.IsTemporalOutput():
            self.filePointer.write('<Grid Name="Grid_T" GridType="Collection" CollectionType="Temporal"  >\n')
        if self.IsMultidomainOutput():
            self.filePointer.write('<Grid Name="Grid_S" GridType="Collection" CollectionType="Spatial" >\n')

        ## here we recover the output for the slave nodes (rank> 0) and then we
        ## write this information in the master node (rank = 0)
        self._OpenParallelWriter()

        if self.IsParafacOutput():
            self.filePointer.write('<Grid Name="Grid_P" GridType="Collection" CollectionType="None" >\n')

        if self.isBinary():
            self.__binaryFilePointer = open (self.__binFileName, "wb")

        if self.IsHdf5():
            import h5py
            self.__hdf5FilePointer = h5py.File(self.__hdf5FileName, 'w')

        if self.__keepXmlFileInSaneState:
            self.WriteTail()

    def _OpenParallelWriter(self):

        mpi = MPI()
        if mpi.mpiOK:
            self.__keepXmlFileInSaneState = False
            if mpi.rank > 0:
                self.filePointer = InMemoryFile(self.filePointer )

    def _CloseParallelWriter(self):

        mpi = MPI()
        if mpi.mpiOK and mpi.rank > 0:
            mpi.comm.send(self.filePointer.data, dest=0)
            self.filePointer = self.filePointer.saveFilePointer
        else:
            for i in range(1,mpi.size):
                data = mpi.comm.recv( source=i)
                self.filePointer.write(data)

    def Close(self):
        """Closes writen file after writing operations are done
        """
        if self.isOpen():
            self.WriteTail()
            self.filePointer.close()
            self._isOpen = False
            if self.isBinary():
                self.__binaryFilePointer.close()
            if self.IsHdf5():
                self.__hdf5FilePointer.close()
            #print("File : '" + self.fileName + "' is close.")

    def WriteTail(self):
        """Writes the end of the file
        """
        if self.isOpen():

            filePosition  = self.filePointer.tell()

            if self.IsParafacOutput():
                self.filePointer.write('</Grid> <!-- Parafac grid -->\n')

            self._CloseParallelWriter()

            if self.IsMultidomainOutput() :
                self.filePointer.write('</Grid> <!-- collection grid -->\n')



            if self.IsTemporalOutput():
                self.__WriteTime()
                self.filePointer.write('    </Grid><!--Temporal pos="'+str(filePosition )+'" __binFileCounter="'+str(self.__binFileCounter)+'" time="'+str(self.currentTime)+'" -->\n')
            self.filePointer.write('  </Domain>\n')
            self.filePointer.write('</Xdmf>\n')
            # we put the pointer just before the tail so we can continue writing
            # to the file for a new time step
            self.filePointer.seek(filePosition )

    def __WriteGeoAndTopo(self,baseMeshObject,name=None):

        if self.__isParafacFormat:
            if "ParafacDims" in baseMeshObject.props:
                self.filePointer.write('    <Information Name="Dims" Value="'+str(baseMeshObject.props["ParafacDims"])+'" /> \n')
                for i in range(baseMeshObject.props["ParafacDims"]):
                    self.filePointer.write('    <Information Name="Dim'+str(i)+'" Value="'+baseMeshObject.props["ParafacDim"+str(i)]+'" /> \n')
                if   "ParafacUnit0" in baseMeshObject.props:
                    for i in range(baseMeshObject.props["ParafacDims"]):
                        self.filePointer.write('    <Information Name="Unit'+str(i)+'" Value="'+baseMeshObject.props["ParafacUnit"+str(i)]+'" /> \n')

        if baseMeshObject.IsConstantRectilinear() :
            origin = baseMeshObject.GetOrigin()
            spacing = baseMeshObject.GetSpacing()
            dims = baseMeshObject.GetDimensions() ## number of nodes per
            dimensionality = baseMeshObject.GetDimensionality()
            if dimensionality != 3:
                origin = np.append(origin,0)
                spacing = np.append(spacing,1)
                dims = np.append(dims,1)

            dimensionality = 3
            #if dimensionality == 3:
            self.filePointer.write('    <Geometry Type="ORIGIN_DXDYDZ">\n')
            #else:
            #    self.filePointer.write('    <Geometry Type="ORIGIN_DXDY">\n')
            self.filePointer.write('      <DataItem DataType="Float" Dimensions="'+str(dimensionality)+'" Format="XML" Precision="8">'+ArrayToString(reversed(origin)) +'</DataItem>\n')
            self.filePointer.write('      <DataItem DataType="Float" Dimensions="'+str(dimensionality)+'" Format="XML" Precision="8">'+ArrayToString(reversed(spacing)) +'</DataItem>\n')
            self.filePointer.write('    </Geometry>\n')
            self.filePointer.write('    <Topology Dimensions="'+ArrayToString(reversed(dims))  +'" Type="'+str(dimensionality)+'DCoRectMesh"/>\n')
        elif baseMeshObject.IsRectilinear() :# pragma: no cover
            print(TFormat.InRed("Mesh Type Rectilinear Not Supported"))        # pragma: no cover
            raise Exception                                                    # pragma: no cover
        elif baseMeshObject.IsStructured() :
            dimensionality = baseMeshObject.GetDimensionality()
            dims = baseMeshObject.GetDimensions() ## number of nodes per

            self.filePointer.write('    <Geometry Type="XYZ">\n')
            self.__WriteDataItem(baseMeshObject.GetPosOfNodes().ravel(), (baseMeshObject.GetNumberOfNodes(),3) , name="GEO_S_"+str(name) )
            self.filePointer.write('    </Geometry>\n')
            self.filePointer.write('    <Topology Dimensions="'+ArrayToString(reversed(dims))  +'" Type="'+str(dimensionality)+'DSMesh"/>\n')
        elif baseMeshObject.IsUnstructured() :
            self.filePointer.write('    <Geometry Type="XYZ">\n')
            if ( baseMeshObject.GetDimensionality()  == 2 ):
                nodes = baseMeshObject.GetPosOfNodes()
                nodes = np.concatenate((nodes,np.zeros((baseMeshObject.GetNumberOfNodes(),1))), axis=1 )
                self.__WriteDataItem(nodes.ravel(), (baseMeshObject.GetNumberOfNodes(),3)  , name="GEO_U_"+str(name) )
            else:
                self.__WriteDataItem(baseMeshObject.GetPosOfNodes().ravel(), (baseMeshObject.GetNumberOfNodes(),3)  , name="GEO_U_"+str(name) )

            self.filePointer.write('    </Geometry>\n')
            if len(baseMeshObject.elements) > 1:
                self.filePointer.write('    <Topology TopologyType="Mixed" NumberOfElements="{0}">\n'.format(baseMeshObject.GetNumberOfElements()))
                nbTotalEntries = 0
                for elemType, data in baseMeshObject.elements.items():
                    nbTotalEntries += data.GetNumberOfElements()*(data.GetNumberOfNodesPerElement()+1)
                    if data.elementType == 'bar2' or data.elementType == 'point1':
                        nbTotalEntries += data.GetNumberOfElements()



                dataArray = np.empty((nbTotalEntries,),dtype=PBasicIndexType)
                cpt =0
                for elemType, data in baseMeshObject.elements.items():
                    xdmfElemTypeNumber = XdmfNumber[elemType]
                    for i in range(data.GetNumberOfElements() ):
                        dataArray[cpt] = xdmfElemTypeNumber
                        cpt += 1
                        if xdmfElemTypeNumber == 0x2 :
                            dataArray[cpt] = 2
                            cpt += 1
                        elif xdmfElemTypeNumber == 0x1 :
                            dataArray[cpt] = 1
                            cpt += 1

                        for j in range(data.GetNumberOfNodesPerElement()):
                            dataArray[cpt] = data.connectivity[i,j]
                            cpt += 1

                self.__WriteDataItem(dataArray, name="Topo_U_"+str(name) )
            elif len(baseMeshObject.elements):
                elements = list(baseMeshObject.elements.keys())[0]
                elementType = XdmfName[elements]
                self.filePointer.write('    <Topology TopologyType="{}" NumberOfElements="{}" '.format(elementType,baseMeshObject.GetNumberOfElements()))
                if XdmfNumber[elements] == 0x2:
                    self.filePointer.write('NodesPerElement="2"  ')
                if XdmfNumber[elements] == 0x1:
                    self.filePointer.write('NodesPerElement="1"  ')
                self.filePointer.write(' >\n')
                self.__WriteDataItem(baseMeshObject.elements[elements].connectivity.ravel(), name="Topo_U_"+str(name) )
            else:
                self.filePointer.write('    <Topology TopologyType="mixed" NumberOfElements="0"  >\n')

            self.filePointer.write('    </Topology> \n')

        else:                                                                  # pragma: no cover
            print(TFormat.InRed("Mesh Type Not Supported"))                    # pragma: no cover
            raise Exception                                                    # pragma: no cover

    def __WriteAttribute(self,data,name,center,baseMeshObject):
        data = data.view()

        shape = None
        if center == "Node":
            nbData = baseMeshObject.GetNumberOfNodes()
        elif center == "Cell":
            nbData = baseMeshObject.GetNumberOfElements()
        elif center == "Grid":
            nbData = 1
        else:
            raise Exception('Cant treat this type of field support' + center )    # pragma: no cover

        if data.size == nbData:
            arrayType = "Scalar"
            #print(shape)
            #print(data.shape)
            if baseMeshObject.IsConstantRectilinear():
                if center == "Node":
                    shape = baseMeshObject.GetDimensions()
                elif center == "Cell":
                    shape = baseMeshObject.GetDimensions() -1
                else:
                    shape = [1]

                if len(shape)>1 :
                    if len(data.shape) <= 2:
                        data.shape = tuple(shape)
                        data = data.T
                    else:
                        data = data.T


            if baseMeshObject.IsConstantRectilinear():
                shape = np.array(shape)
                if center == "Node":
                    shape = shape.T
                elif center == "Cell":
                    shape = shape.T

        elif data.size == nbData*3:

            arrayType = "Vector"
            if baseMeshObject.IsConstantRectilinear() :
                if center == "Node":
                    shape = baseMeshObject.GetDimensions()
                elif center == "Cell":
                    shape = baseMeshObject.GetDimensions() - 1
                else:
                    shape = [1]

                if len(shape)>1:
                    if baseMeshObject.GetDimensionality() == 2:
                        shape = tuple(shape) + (1,3,)
                    else:
                        shape = tuple(shape) + (3,)

                    if len(data.shape) <= 2:
                        data.shape = shape
                    data = data.transpose(2,1,0,3)

            if baseMeshObject.IsConstantRectilinear():
                shape = np.array(shape)
                if center == "Node":
                    shape = shape[[2,1,0,3]]
                elif center == "Cell":
                    shape = shape[[2,1,0,3]]

        elif data.size == nbData*6:
            arrayType = "Vector"
            if baseMeshObject.IsConstantRectilinear():
                if center == "Node":
                    shape = baseMeshObject.GetDimensions()
                elif center == "Cell":
                    shape = baseMeshObject.GetDimensions() - 1
                else:
                    shape = [1]

        elif data.size == nbData*9:

            arrayType = "Vector"
            if baseMeshObject.IsConstantRectilinear() :
                if center == "Node":
                    shape = baseMeshObject.GetDimensions()
                elif center == "Cell":
                    shape = baseMeshObject.GetDimensions() - 1
                else:
                    shape = [1]

        elif data.size == nbData*2:
            if baseMeshObject.IsConstantRectilinear() :
                if center == "Node":
                    shape = baseMeshObject.GetDimensions()
                elif center == "Cell":
                    shape = baseMeshObject.GetDimensions() - 1
                else:
                    shape = [1]

            # add an extra zeros to the data and print it out as Vector 3
            if baseMeshObject.GetDimensionality() == 2:
                    shape = (data.size//2,1,2,)
            else:
                    shape = (data.size//2,2,)

            if len(data.shape) <= 2:
                data.shape = shape

            #data = data.transpose(1,0,2)

            shape = list(data.shape)
            shape [-1] = 3
            shape = tuple(shape)
            data1 = np.zeros(shape, dtype=data.dtype)

            data1[...,0:2] = data

            self.__WriteAttribute(data1.ravel(),name,center,baseMeshObject)

            return
        else:
            print(TFormat.InRed("I don't kow how to treat fields '"+ str(name)+"' with " +str(data.size/nbData) +" components"))  # pragma: no cover
            print(TFormat.InRed("Data has size : " + str(data.size) ))  # pragma: no cover
            print(TFormat.InRed("But support has size : " + str(nbData) ))  # pragma: no cover

            raise Exception                                                                                    # pragma: no cover
        self.filePointer.write('    <Attribute Center="'+center+'" Name="'+name+'" Type="'+arrayType+'">\n')#

        try:
            self.__WriteDataItem(data.ravel(),shape,name=name)
        except:
            print("Error Writing heavy data of field: " + str(name))
            raise

        self.filePointer.write('    </Attribute>\n')

    def WriteIntegrationsPoints(self, allData):
        """Writes integration points information to file
        """
        for elemName, data in allData.items():
            points, weight = data
            npData = np.asarray(points,dtype=float).copy()
            nip = npData.shape[0]
            if npData.shape[1] < 3:
                b = np.zeros((nip,3))
                b[:,:-1] = npData
                npData = b

            self.filePointer.write('    <Information Name="QP" Value="')#
            self.filePointer.write(str(EN.numberOfNodes[elemName]) + " ")
            self.filePointer.write(str(XdmfNumber[elemName]) + " ")
            self.filePointer.write(str(nip) + '" > \n')

            self.__WriteDataItem(npData.ravel(),[npData.size],name="ip")
            self.filePointer.write('</Information> \n')#

    def WriteIntegrationsPointData(self, names, allData):
        """Writes integration points data to file
        """
        for i, name in enumerate(names):
            data = allData[i]
            self.filePointer.write('    <Information Name="IPF" Value="'+str(name)+'" > \n')#
            self.ipStorage[name] = self.__WriteDataItem(data.ravel(),[data.size],name='IPD_'+name)
            self.filePointer.write('</Information> \n')#

    def NextDomain(self):
        self.parafacCpt = 0
        self.ddmCpt += 1
        if self.IsMultidomainOutput() :
            if self.IsParafacOutput():
                self.filePointer.write('</Grid> <!-- Parafac grid -->\n')
                self.filePointer.write('<Grid Name="Grid_P" GridType="Collection" CollectionType="None" >\n')
        else:
            raise Exception("Cant make a new domain without a multi domain output")

    def MakeStep(self, Time = None, TimeStep = None):
        """Increases time step in output files

        Parameters
        ----------
        Time : float, optional
            time value of the time step, by default None
        TimeStep : int, optional
            number of the time step, by default None
        """
        if self.IsMultidomainOutput():
            self.filePointer.write('</Grid> <!-- collection grid -->\n')
            self.filePointer.write('<Grid Name="Collection" GridType="Collection" CollectionType="Spatial" >\n')

        dt = 1
        if Time is not None:
            dt = Time - self.currentTime
        elif TimeStep is not None:
            dt = TimeStep

        if self.IsTemporalOutput():
            self.Step(dt)

        if self.IsTemporalOutput() and self.__printTimeInsideEachGrid and (self.IsMultidomainOutput() == False) :
            self.filePointer.write('    <Time Value="'+str(self.currentTime)+'" /> \n')

    def Write(self,baseMeshObject, PointFields = None, CellFields = None, GridFields= None, PointFieldsNames = None, CellFieldsNames= None, GridFieldsNames=None , Time= None, TimeStep = None,domainName=None, IntegrationRule=None, IntegrationPointData=None, IntegrationPointDataNames=None ):
        """Write data to file in xdmf format

        Parameters
        ----------
        baseMeshObject : UnstructuredMesh
            the mesh to be written
        PointFields : list[np.ndarray], optional
            fields to write defined at the vertices of the mesh, by default None
        CellFields : list[np.ndarray], optional
            fields to write defined at the elements of the mesh, by default None
        GridFields : list[np.ndarray], optional
            grid fields to write, by default None
        PointFieldsNames : list[str], optional
            names of the fields to write defined at the vertices of the mesh, by default None
        CellFieldsNames : list[str], optional
            names of the fields to write defined at the elements of the mesh, by default None
        GridFieldsNames : list[str], optional
            names of the grid fields to write, by default None
        Time : float, optional
            time at which the data is read, by default None
        TimeStep : int, optional
            time index at which the data is read, by default None
        domainName : str, optional
            Not Used, by default None
        IntegrationRule : dict[IntegrationRuleType], optional
            integration rules associated to the integration point data, by default None
        IntegrationPointData : list[np.ndarray], optional
            fields defined at the integration points, by default None
        IntegrationPointDataNames : list[str], optional
            names of the fields defined at the integration points, by default None
        """
        if (Time is not None or TimeStep is not None) and self.IsMultidomainOutput():
            raise(Exception("set time using MakeStep, not the Write option") )

        if PointFields is None:
            PointFields = []

        if CellFields  is None:
            CellFields   = []

        if GridFields is None:
            GridFields  = []

        if PointFieldsNames is None:
            PointFieldsNames  = []

        if CellFieldsNames is None:
            CellFieldsNames  = []

        if GridFieldsNames is None:
            GridFieldsNames  = []

        if IntegrationRule is None:
            IntegrationRule  = {}

        if IntegrationPointData is None:
            IntegrationPointData  = []

        if IntegrationPointDataNames is None:
            IntegrationPointDataNames  = []

        self.pointFieldsStorage = {}
        self.cellFieldsStorage = {}
        self.gridFieldsStorage = {}
        self.ipStorage = {}

        if not self.isOpen() :
            if self.automaticOpen:
                self.Open()
            else:
                print(TFormat.InRed("Please Open The writer First!!!"))
                raise Exception

        if not self.IsMultidomainOutput():
            dt = 1
            if Time is not None:
                dt = Time - self.currentTime
            elif TimeStep is not None:
                dt = TimeStep
            if self.IsTemporalOutput():
                self.Step(dt)

        if self.IsParafacOutput ():
            suffix = "P" + str(self.parafacCpt)
            self.parafacCpt += 1
        else:
            suffix = str(len(self.timeSteps))

        if self.IsMultidomainOutput():
            if MPI.IsParallel():
                suffix += "_D" + str(MPI.Rank())
            else:
                suffix += "_D" + str(self.ddmCpt)

        #if we have a constantRectilinear mesh with more than only "bulk"
        # elements, we add a collection to add all the rest of the elements

        if baseMeshObject.IsConstantRectilinear() and len(baseMeshObject.elements) > 1:
            self.filePointer.write('<Grid Name="Grid_S'+suffix+'" GridType="Collection" CollectionType="Spatial" >\n')
            if self.IsTemporalOutput() and self.__printTimeInsideEachGrid and (self.IsMultidomainOutput() == False) :
                self.filePointer.write('    <Time Value="'+str(self.currentTime)+'" /> \n')
            self.filePointer.write('    <Grid Name="Bulk">\n')
        else:
            self.filePointer.write('    <Grid Name="Grid_'+suffix+'">\n')
            if self.IsTemporalOutput() and self.__printTimeInsideEachGrid and (self.IsMultidomainOutput() == False) :
                self.filePointer.write('    <Time Value="'+str(self.currentTime)+'" /> \n')

        self.__WriteGeoAndTopo(baseMeshObject,name=suffix)
        self.__WriteNodesTagsElementsTags(baseMeshObject,PointFieldsNames,CellFieldsNames)
        self.__WriteNodesFieldsElementsFieldsGridFields(baseMeshObject,
                                                PointFieldsNames,PointFields,
                                                CellFieldsNames,CellFields,
                                                GridFieldsNames,GridFields)

        self.WriteIntegrationsPoints(IntegrationRule)
        self.WriteIntegrationsPointData(IntegrationPointDataNames,IntegrationPointData)

        if baseMeshObject.IsConstantRectilinear() and len(baseMeshObject.elements) > 1:
            self.filePointer.write('    </Grid>\n')
            from BasicTools.Containers.UnstructuredMesh import UnstructuredMesh
            tempMesh = UnstructuredMesh()
            tempMesh.nodes = baseMeshObject.nodes
            tempMesh.originalIDNodes = baseMeshObject.originalIDNodes
            for name, data in baseMeshObject.elements.items():
                if data.mutable :
                    tempMesh.elements[name] =  data
            self.filePointer.write('    <Grid Name="Sets">\n')
            self.__WriteGeoAndTopo(tempMesh)
            self.__WriteNodesTagsElementsTags(tempMesh,[],[])
            self.filePointer.write('    </Grid>\n')

        self.filePointer.write('    </Grid>\n')

        if(self.__keepXmlFileInSaneState):
            self.WriteTail()

        self.filePointer.flush()

        if self.isBinary() :# pragma: no cover
            self.__binaryFilePointer.flush()
    def __WriteNodesFieldsElementsFieldsGridFields(self,baseMeshObject,
                                                PointFieldsNames,PointFields,
                                                CellFieldsNames,CellFields,
                                                GridFieldsNames,GridFields):

        for i in range(len(PointFields)):
            name = 'PField'+str(i)
            if len(PointFields)  == len(PointFieldsNames):
                name = PointFieldsNames[i]
            self.pointFieldsStorage[name] = self.__WriteAttribute(np.asarray(PointFields[i]), name, "Node",baseMeshObject)

        for i in range(len(CellFields)):
            name = 'CField'+str(i)
            if len(CellFields) == len(CellFieldsNames):
                name = CellFieldsNames[i]

            self.cellFieldsStorage[name] = self.__WriteAttribute(np.asarray(CellFields[i]), name, "Cell",baseMeshObject)

        for i in range(len(GridFields)):

            name = 'GField'+str(i)
            if len(GridFields) == len(GridFieldsNames):
                name = GridFieldsNames[i]

            self.gridFieldsStorage[name] = self.__WriteAttribute(np.asarray(GridFields[i]), name, "Grid",baseMeshObject)

    def __WriteNodesTagsElementsTags(self,baseMeshObject,PointFieldsNames,CellFieldsNames):
        for tag in baseMeshObject.nodesTags:
            if tag.name in PointFieldsNames:
                name = "Tag_" + tag.name
            else:
                name = tag.name

            data = np.zeros((baseMeshObject.GetNumberOfNodes(),1),dtype=np.int8)
            data[baseMeshObject.nodesTags[tag.name].GetIds()] = 1
            self.__WriteAttribute(np.asarray(data), name, "Node",baseMeshObject)

        #Cell Tags
        baseMeshObject.PrepareForOutput()

        if baseMeshObject.IsConstantRectilinear():
            cellTags = baseMeshObject.GetNamesOfElemTagsBulk()
            GetElementsInTag = baseMeshObject.GetElementsInTagBulk
        else:
            cellTags = baseMeshObject.GetNamesOfElemTags()
            GetElementsInTag = baseMeshObject.GetElementsInTag

        for tagname in cellTags:
            if tagname in CellFieldsNames:
                name = "Tag_" + tagname
            else:
                name = tagname
            data = GetElementsInTag(tagname)
            res = np.zeros((baseMeshObject.GetNumberOfElements(),1),dtype=np.int8)
            res[data] = 1

            self.__WriteAttribute(np.asarray(res), name, "Cell", baseMeshObject)

    def __WriteTime(self):
        """ this function is called by the WriteTail, this function must NOT change
        the state of the instance, also no writing to binary neither hdf5 files """
        if self.isOpen() and self.__printTimeInsideEachGrid == False:
            #self.filePointer.write('<Time TimeType="List">\n')
            #self.__WriteDataItem(self.timeSteps)
            #self.filePointer.write('</Time>\n')
            self.filePointer.write('<Time Value="'+ (" ".join(str(x) for x in self.timeSteps)) +'"/>\n')

    def __WriteDataItem(self,_data, _shape= None,name=None):

        import numpy as np
        data = np.asarray(_data)
        if _shape is None:
            _shape = _data.shape
        shape = np.asarray(_shape)

        if self.isOpen():
            if data.dtype == np.float64:
                typename = 'Float'
                s = data.dtype.itemsize
            elif data.dtype == np.float32:
                typename = 'Float'
                s = data.dtype.itemsize
            elif data.dtype == np.int32:
                typename = 'Int'
                s = data.dtype.itemsize
            elif data.dtype == np.int64:
                typename = 'Int'
                s = data.dtype.itemsize
            elif data.dtype == np.int8:
                typename = 'Char'
                s = data.dtype.itemsize
            else:
                print(f"Warning : skipping field '{name}' of type '{type(data[0])}' not supported'")
                return None

            dimension = ArrayToString(shape)

            if self.isBinary() and len(data) > self.__XmlSizeLimit:# pragma: no cover

                # to test this feature a big file must be created (so we don't test it)
                if self.__binaryCpt > self.__chunkSize :
                    self.__binaryFilePointer.close()
                    self.NewBinaryFilename()
                    self.__binaryFilePointer = open (self.__binFileName, "wb")
                    self.__binaryCpt = 0

                gsData,gsStorage = self.globalStorage.get(str(name),(None,None))

                dataToWrite = data.ravel()
                if np.array_equal(gsData, dataToWrite):
                    binaryFile = gsStorage.filenameOnly
                    seek = gsStorage.offset
                    gsStorage.usedByNInstances += 1
                    self.globalStorage[str(name)] = (gsData.copy(),gsStorage)
                    res = gsStorage
                else:
                    res = BinaryStorage(data=data,filePointer=self.__binaryFilePointer)
                    res.filenameOnly = self.__binFileNameOnly
                    binaryFile = self.__binFileNameOnly
                    seek = self.__binaryCpt
                    data.ravel().tofile(self.__binaryFilePointer)
                    self.__binaryCpt += s*len(dataToWrite)
                    if len(self.globalStorage) > self.maxStorageSize-1:
                        usage = [x[1].usedByNInstances for x in self.globalStorage.values()]
                        #print(usage)
                        minUsage = min(usage)
                        newGlobalStorage = {}
                        GT = len(self.globalStorage)
                        for i,d in self.globalStorage.items():
                            if d[1].usedByNInstances == minUsage:
                                GT -= 1
                                if GT < self.maxStorageSize-1:
                                    break
                                continue
                            newGlobalStorage[i]=d
                        self.globalStorage = newGlobalStorage
                    self.globalStorage[str(name)] = (dataToWrite.copy(),res)


                self.filePointer.write(' <DataItem Format="Binary"'+
                ' NumberType="'+typename+'"'+
                ' Dimensions="'+dimension+'" '+
                ' Seek="'+str(seek)+'" '+
                ' Endian="Native" '+
                ' Precision="'+str(s)+'" '+

                ' Compression="Raw" >')
                self.filePointer.write(binaryFile)
                self.filePointer.write('</DataItem>\n')

                return res
            elif self.IsHdf5():
                if self.__hdf5cpt > self.__chunkSize :
                    import h5py
                    self.__hdf5FilePointer.close()
                    self.NewHdf5Filename()
                    self.__hdf5FilePointer = h5py.File(self.__hdf5FileName, 'w')
                    self.__hdf5cpt = 0

                if name is None:
                    name = "dataset_"+ str(self.__hdf5NameCpt)
                else:
                    name += "_"+ str(self.__hdf5NameCpt)

                self.__hdf5NameCpt += 1


                self.__hdf5FilePointer.create_dataset(name, data=data)
                self.__hdf5cpt += s*data.size
                self.filePointer.write(' <DataItem Format="HDF"'+
                ' NumberType="'+typename+'"'+
                ' Dimensions="'+dimension+'" '+
                ' Precision="'+str(s)+'" >')
                self.filePointer.write(self.__hdf5FileNameOnly)
                self.filePointer.write(":")
                self.filePointer.write(name)
                self.filePointer.write('</DataItem>\n')
            else:
                self.filePointer.write(' <DataItem Format="XML" NumberType="'+typename+'" Dimensions="'+dimension+'">')
                self.filePointer.write(" ".join(str(x) for x in data.ravel()))

                self.filePointer.write('</DataItem>\n')
                return None


from BasicTools.IO.IOFactory import RegisterWriterClass
RegisterWriterClass(".xdmf",XdmfWriter)
RegisterWriterClass(".xmf",XdmfWriter)

def WriteTest(tempdir, Temporal, Binary, Hdf5 ):

    from BasicTools.Containers.ConstantRectilinearMesh import ConstantRectilinearMesh

    myMesh = ConstantRectilinearMesh()
    myMesh.SetDimensions([2,3,4])
    print(" a  ",myMesh.GetDimensions())
    print(" b  ",myMesh.structElements.GetNumberOfElements())
    print(myMesh.GetNumberOfElements())
    myMesh.SetSpacing([0.1, 0.1, 0.1])
    myMesh.SetOrigin([-2.5,-1.2,-1.5])

    dataT = np.arange(24,dtype=np.float32)
    dataT.shape = (2,3,4)
    dataDep = np.arange(24*3)+0.3

    dataDep.shape = (2,3,4,3)

    writer = XdmfWriter(tempdir + 'TestOutput_Bin_'+str(Binary)+'_hdf5_'+str(Hdf5)+'_Temp_'+str(Temporal)+'.xmf')
    writer.SetTemporal(Temporal)
    writer.SetBinary(Binary)
    writer.SetHdf5(Hdf5)
    writer.Open()
    print(writer)
    writer.Write(myMesh,PointFields=[dataT, dataDep], PointFieldsNames=["Temp","Dep"],CellFields=[np.arange(6)],CellFieldsNames=['S'], Time=0)
    writer.Write(myMesh,GridFields=[0, 1], GridFieldsNames=['K','P'], TimeStep = 1)
    writer.Close()

def WriteTestAppend(tempdir, Temporal, Binary):

    from BasicTools.Containers.ConstantRectilinearMesh import ConstantRectilinearMesh

    myMesh = ConstantRectilinearMesh()
    myMesh.SetDimensions([2,3,4])
    myMesh.SetSpacing([0.1, 0.1, 0.1])
    myMesh.SetOrigin([-2.5,-1.2,-1.5])

    dataT = np.arange(24,dtype=np.float32)
    dataT.shape = (2,3,4)
    dataDep = np.arange(24*3)+0.3

    dataDep.shape = (2,3,4,3)

    writer = XdmfWriter(tempdir + 'TestOutput_Bin_'+str(Binary)+'_Temp_'+str(Temporal)+'.xmf')
    writer.SetAppendMode(True)
    writer.SetTemporal(Temporal)
    writer.SetBinary(Binary)
    writer.Open()
    print(writer)
    writer.Write(myMesh,PointFields=[dataT, dataDep], PointFieldsNames=["Temp","Dep"],CellFields=[np.arange(6)],CellFieldsNames=['S'])
    writer.Write(myMesh,GridFields=[0, 1], GridFieldsNames=['K','P'], TimeStep = 1)
    writer.Close()

def CheckIntegrity(GUI=False):
    from BasicTools.Helpers.Tests import TestTempDir
    from BasicTools.Containers.ConstantRectilinearMesh import ConstantRectilinearMesh
    import BasicTools.Containers.UnstructuredMesh as UM
    from BasicTools.Containers.UnstructuredMeshCreationTools import CreateMeshOfTriangles

    tempdir = TestTempDir.GetTempPath()

    res = CreateMeshOfTriangles([[0.,0.,0],[1.,2.,3],[1, 3, 2]], np.asarray([[0,1,2]]))
    print(res)
    if GUI:
        res.SetGlobalDebugMode()

    WriteMeshToXdmf(tempdir+"TestUnstructured.xdmf", res, PointFields = [np.array([1.,2,3])], CellFields =[ np.array([1])] ,GridFields= [[0],  np.array([1,2,3]).astype(np.int64) ],
                                                                    PointFieldsNames = ["PS"],
                                                                    CellFieldsNames = ["CS"],
                                                                    GridFieldsNames = ["GS", "GV"] , Binary= True)

    elements = res.GetElementsOfType(EN.Bar_2)
    elements.AddNewElement([1,2],1)
    elements = res.GetElementsOfType(EN.Point_1)
    elements.AddNewElement([0],2)
    res.nodes = np.ascontiguousarray(res.nodes[:,0:2])
    res.GetNodalTag("First_Point").AddToTag(0)

    res.AddElementToTagUsingOriginalId(1,"bars")

    WriteMeshToXdmf(tempdir+"TestUnstructured_multiElements.xdmf", res, PointFields = [np.array([1.,2,3])], CellFields =[ np.array([1,0,4])] ,GridFields= [[0]],
                                                                    PointFieldsNames = ["PS"],
                                                                    CellFieldsNames = ["CS"],
                                                                    GridFieldsNames = ["GS"] , Binary= True)
    #----------------------
    res = UM.UnstructuredMesh()
    WriteMeshToXdmf(tempdir+"TestUnstructured_EmptyMesh.xdmf", res)

    res.SetNodes([[0,0,0],[1,0,0]],np.arange(2))
    elements = res.GetElementsOfType(EN.Point_1)
    elements.AddNewElement([0],1)

    WriteMeshToXdmf(tempdir+"TestUnstructured_OnlyPoints.xdmf", res)

    res = UM.UnstructuredMesh()
    res.nodes = np.array([[0,0,0],[1,0,0]],dtype=np.float32)
    res.originalIDNodes = np.arange(res.GetNumberOfNodes())
    elements = res.GetElementsOfType(EN.Bar_2)
    elements.AddNewElement([0,1],1)
    WriteMeshToXdmf(tempdir+"TestUnstructured_OnlyBars.xdmf", res)
    #----------------------

    WriteTest(tempdir, False, False, False)
    WriteTest(tempdir, False, True,  False)
    WriteTest(tempdir, False, False, True)

    WriteTest(tempdir,True, False,  False)
    WriteTest(tempdir,True, True,  False)
    WriteTest(tempdir,True, False, True)

    WriteTestAppend(tempdir,True, True)



    WriteMeshToXdmf(tempdir+'testDirect.xdmf',ConstantRectilinearMesh() )

    writer = XdmfWriter()
    writer.SetFileName(None)
    writer.SetFileName(tempdir+'testErrors.xdmf')
    writer.SetXmlSizeLimit(0)
    writer.Open()

    ## test of the errors
    try:
        writer.SetTemporal()
        return 'Not ok'# pragma: no cover
    except:
        pass

    try:
        writer.SetBinary()
        return 'Not ok'# pragma: no cover
    except:
        pass

    # no error anymore just a warning
    #try:
    writer.Open()
    #except:
    #    pass

    writer.Close()

    try:
        writer.Write(ConstantRectilinearMesh())
        return "Not   ok"# pragma: no cover
    except:
        pass

    # for the moment we comment this test (verification of "unable to open file")
    # need to find a way to raise an exception in linux and in windows with the
    # same filename
    #
    #try:
    #    writer.Open("c:\\")  # in windows this will raise an exception
    #    writer.Open("\")     # in linux this will raise an exception
    #    return 'Not ok'# pragma: no cover
    #except:
    #    pass

    print("ConstantRectilinearMesh in 2D")
    CRM2D = ConstantRectilinearMesh(2)

    writer = XdmfWriter()
    writer.SetFileName(None)
    writer.SetXmlSizeLimit(0)
    writer.SetBinary(True)
    writer.Open(filename=tempdir+'testDirect.xdmf')
    writer.Write(CRM2D, PointFields = [ np.zeros((CRM2D.GetNumberOfNodes(),) ).astype(np.float32), np.zeros((CRM2D.GetNumberOfNodes(),) ).astype(int) ],
                                                            PointFieldsNames = ["Test", "testInt"],
                                                            CellFields= [ np.arange(CRM2D.GetNumberOfElements()*2 ).astype(np.float64)],
                                                            CellFieldsNames = [ "TestV"] )
    writer.Close()


    CRM2D = ConstantRectilinearMesh(2)

    writer = XdmfWriter()
    writer.SetFileName(None)
    writer.SetXmlSizeLimit(0)
    writer.SetBinary(True)
    writer.SetMultidomain()
    writer.Open(filename=tempdir+'testDirectTwoDomains.xdmf')


    writer.Write(CRM2D, PointFields = [ np.zeros((CRM2D.GetNumberOfNodes(),) ).astype(np.float32), np.zeros((CRM2D.GetNumberOfNodes(),) ).astype(int) ],
                                                            PointFieldsNames = ["Test", "testInt"],
                                                            CellFields= [ np.arange(CRM2D.GetNumberOfElements()*2 ).astype(np.float64)],
                                                            CellFieldsNames = [ "TestV"] )
    CRM3D = ConstantRectilinearMesh(3)
    writer.Write(CRM3D)

    writer.Close()
    if GUI :
        from BasicTools.Actions.OpenInParaView import OpenInParaView
        OpenInParaView(filename = tempdir+'testDirectTwoDomains.xdmf')


    writer = XdmfWriter()
    writer.SetFileName(None)
    writer.SetXmlSizeLimit(0)
    writer.SetBinary(True)
    writer.SetMultidomain()
    writer.SetTemporal()
    writer.Open(filename=tempdir+'testDirectTwoDomainsTwoSteps.xdmf')
    writer.Write(CRM2D)
    writer.Write(CRM3D)
    writer.MakeStep(Time=1.5)
    writer.Write(CRM3D)
    writer.Write(CRM2D)
    writer.Close()

    if GUI:
        from BasicTools.Actions.OpenInParaView import OpenInParaView
        OpenInParaView(filename = tempdir+'testDirectTwoDomainsTwoSteps.xdmf')

    ####### work for PXDMF 2.0 #################
    writer = XdmfWriter()
    writer.SetFileName(None)
    writer.SetXmlSizeLimit(0)
    writer.SetBinary(True)
    writer.SetHdf5(False)
    writer.SetParafac(True)
    writer.Open(filename=tempdir+'parafac.pxdmf')
    from BasicTools.Containers.UnstructuredMeshCreationTools import  CreateMeshFromConstantRectilinearMesh as CreateMeshFromConstantRectilinearMesh
    from BasicTools.Containers.UnstructuredMeshCreationTools import  CreateUniformMeshOfBars

    mesh1DTime = CreateUniformMeshOfBars(2,5,10)
    mesh1DTime.props['ParafacDims'] = 1
    mesh1DTime.props['ParafacDim0'] = "T"

    cMesh2D = ConstantRectilinearMesh(2)
    cMesh2D.SetDimensions([4,4])
    mesh2DParameters = CreateMeshFromConstantRectilinearMesh(cMesh2D)
    mesh2DParameters.props['ParafacDims'] = 2
    mesh2DParameters.props['ParafacDim0'] = "Px"
    mesh2DParameters.props['ParafacDim1'] = "Py"

    cMesh3D = ConstantRectilinearMesh(3)
    cMesh3D.SetDimensions([8,8,8])
    mesh3DSpace = CreateMeshFromConstantRectilinearMesh(cMesh3D)

    from BasicTools.FE.IntegrationsRules import LagrangeIsoParam

    IntegrationPointData = np.arange(mesh2DParameters.GetNumberOfElements()*len(LagrangeIsoParam[EN.Quadrangle_4][1]) )+0.1

    IntegrationPointAllData = [IntegrationPointData]
    writer.Write(mesh2DParameters,
                IntegrationRule=LagrangeIsoParam,
                IntegrationPointData=IntegrationPointAllData,
                IntegrationPointDataNames=["IPId_0"])

    print(IntegrationPointAllData)
    writer.ipStorage["IPId_0"].UpdateHeavyStorage(IntegrationPointData+10)

    writer.Write(mesh1DTime, CellFields = [np.arange(mesh1DTime.GetNumberOfElements())+0.1 ], CellFieldsNames=["IPId_0"])
    writer.Write(mesh3DSpace, CellFields = [np.arange(mesh3DSpace.GetNumberOfElements())+0.1 ], CellFieldsNames=["IPId_0"])
    writer.Close()

    if GUI :
        from BasicTools.Actions.OpenInParaView import OpenInParaView
        OpenInParaView(filename = tempdir+'parafac.pxdmf')

    from BasicTools.IO.XdmfReader import XdmfReader  as XR
    f = XR(filename = tempdir+'testDirect.xdmf' )
    f.lazy = False
    f.Read()
    print(tempdir+'testDirect.xdmf')
    f.xdmf.GetDomain(0).GetGrid(0).GetFieldsOfType("Cell")
    print(f.xdmf.GetDomain(0).GetGrid(0).attributes )

    domain = f.xdmf.GetDomain(0)
    grid  = domain.GetGrid(0)
    grid.GetFieldsOfType("Cell")

    ### Domain Decomposition and Parafac

    res = CheckIntegrityDDM(GUI=GUI)
    if res.lower() != "ok": return res

    CheckIntegrityHdf5(tempdir)

    return 'ok'

def CheckIntegrityHdf5(tempdir):

    from BasicTools.Containers.ConstantRectilinearMesh import ConstantRectilinearMesh

    myMesh = ConstantRectilinearMesh()
    myMesh.SetDimensions([20,30,40])
    myMesh.SetSpacing([0.1, 0.1, 0.1])
    myMesh.SetOrigin([-2.5,-1.2,-1.5])

    dataT = np.arange(24000,dtype=np.float32)
    dataT.shape = (20,30,40)
    dataDep = np.arange(24000*3)+0.3
    dataDep.shape = (20,30,40,3)

    writer = XdmfWriter(tempdir + 'TestHDF5_.xmf')
    writer.SetChunkSize(2**20)
    writer.SetTemporal(True)
    writer.SetHdf5(True)
    writer.Open()
    print(writer)
    for i in range(3):
        dataT = np.random.rand(24000)
        dataT.shape = (20,30,40)
        dataDep = np.random.rand(24000*3)+0.3
        dataDep.shape = (20,30,40,3)
        writer.Write(myMesh,PointFields=[dataT, dataDep], PointFieldsNames=["Temp","Dep"],CellFields=[np.arange(19*29*39)],CellFieldsNames=['S'])
    writer.Close()

def CheckIntegrityDDM(GUI=False):
    """ this test function can be launched using the mpirun -n 2 ...
    to test the writer in mpi mode
    """

    from BasicTools.Helpers.Tests import TestTempDir
    tempdir = TestTempDir.GetTempPath()


    from BasicTools.Containers.UnstructuredMeshCreationTools import  CreateUniformMeshOfBars

    mesh1D = CreateUniformMeshOfBars(0,5,10)
    mesh1D.props['ParafacDims'] = 1
    mesh1D.props['ParafacDim0'] = "T"

    from BasicTools.Helpers.MPIInterface import MPIInterface as MPI

    writer = XdmfWriter()
    writer.SetFileName(None)
    writer.SetXmlSizeLimit(0)
    writer.SetBinary(True)
    writer.SetMultidomain()
    writer.SetParafac(True)
    mpi = MPI()
    print("rank ", mpi.rank)
    writer.Open(filename=tempdir+'DDM_parafac.pxdmf')


    mpi = MPI()
    if mpi.Rank() == 0:
        mesh1D.props['ParafacDim0'] = "D0_P0"
        writer.Write(mesh1D, CellFields = [np.arange(mesh1D.GetNumberOfElements())+0.1 ], CellFieldsNames=["IPId_0"])

        mesh1D.nodes[:,0] += 1
        mesh1D.props['ParafacDim0'] = "D0_P1"
        writer.Write(mesh1D, CellFields = [np.arange(mesh1D.GetNumberOfElements())+0.1 ], CellFieldsNames=["IPId_0"])

    if mpi.IsParallel() == 0 :
        writer.NextDomain()

    if mpi.Rank() == mpi.size-1 :

        mesh1D.nodes[:,0] += 1
        mesh1D.props['ParafacDim0'] = "D1_P0"
        writer.Write(mesh1D, CellFields = [np.arange(mesh1D.GetNumberOfElements())+0.1 ], CellFieldsNames=["IPId_0"])

        mesh1D.nodes[:,0] += 1
        mesh1D.props['ParafacDim0'] = "D1_P1"
        writer.Write(mesh1D, CellFields = [np.arange(mesh1D.GetNumberOfElements())+0.1 ], CellFieldsNames=["IPId_0"])

    writer.Close()
    if HasHdf5Support():
        return "ok"
    else:
        return "ok, but no hdf5 support"


if __name__ == '__main__':
    #from BasicTools.Helpers.Tests import TestTempDir
    #TestTempDir.SetTempPath("/tmp/BasicTools_Test_Directory__is42mzi_safe_to_delete/")
    print(CheckIntegrity(GUI=False)) # pragma: no cover
