# -*- coding: utf-8 -*-
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
#
"""Ut file reader (Zset result file)
"""
import os

import numpy as np

from BasicTools.IO.ReaderBase import ReaderBase
from BasicTools.NumpyDefs import PBasicFloatType

def ReadFieldFromUt(fileName = None, fieldname = None, time = None, timeIndex = None, string = None, atIntegrationPoints = False):
    """Function API for reading a field defined in an ut file

    Parameters
    ----------
    fileName : str, optional
        name of the file to be read, by default None
    fieldname : str, optional
        name of the field to be read, by default None
    time : float, optional
        time at which the field is read, by default None
    timeIndex : int, optional
        time index at which the field is read, by default None
    string : str, optional
        data to be read as a string instead of a file, by default None
    atIntegrationPoints : bool, optional
        if True, field is read at integration points (from .integ file), by default False

    Returns
    -------
    np.ndarray
        field read
    """
    reader = UtReader()
    reader.SetFileName(fileName)
    reader.SetStringToRead(string)
    reader.atIntegrationPoints = atIntegrationPoints
    reader.ReadMetaData()
    reader.SetFieldNameToRead(fieldname)
    reader.SetTimeToRead(time=time, timeIndex=timeIndex)
    return reader.ReadField()


def ReadUTMetaData(fileName):
    """Function API for reading of metadate of an ut file

    Parameters
    ----------
    fileName : str, optional
        name of the file to be read, by default None

    Returns
    -------
    dict
        metadate of the ut file
    """
    reader = UtReader()
    reader.SetFileName(fileName)
    reader.ReadUTMetaData()
    metaData = {}
    metaData["meshFile"] = reader.meshfile
    metaData["node"]     = reader.node
    metaData["integ"]    = reader.integ
    metaData["element"]  = reader.element
    metaData["time"]     = reader.time
    return metaData



class UtReader(ReaderBase):
    """Ut Reader class
    """
    def __init__(self):
        super(UtReader,self).__init__()
        self.commentChar ="#"
        self.meshfile = None
        self.node = []
        self.integ = []
        self.element = []
        self.time = None

        self.fieldNameToRead = None
        self.timeToRead = -1
        self.atIntegrationPoints = False
        self.meshMetadata = None
        self.cache = None
        self.oldtimeindex = None

        self.canHandleTemporal = True

    def Reset(self):
        """Resets the reader
        """
        self.meshfile = None
        self.node = []
        self.integ = []
        self.element =[]
        self.time = []

    def SetFieldNameToRead(self, fieldname):
        """Sets the name of the field to read

        Parameters
        ----------
        fieldname : str
            name of the field to read
        """
        if fieldname is not None:
            self.fieldNameToRead = fieldname

    def SetTimeToRead(self, time = None, timeIndex = None):
        """Sets the time at which the data is read

        Parameters
        ----------
        time : float, optional
            time at which the data is read, by default None
        timeIndex : int, optional
            time index at which the data is read, by default None

        Returns
        -------
        int
            time index at which the data is read
        """
        if (time is None) and (timeIndex is None):
            if self.timeToRead == -1:
                self.timeToRead = self.time[-1][4]
                return len(self.time)-1
            else:
                return [data[4]for data in self.time].index(self.timeToRead)

        if (time is not None) and (timeIndex is not None):
            raise(Exception("Cannot specify both time and timeIndex"))

        if time is None:
            self.timeToRead = self.time[timeIndex][4]
            return timeIndex
        elif time == -1:
            self.timeToRead = self.time[-1][4]
            return timeIndex
        else:
            self.timeToRead = time
            return [data[4]for data in self.time].index(self.timeToRead)


    def GetAvailableTimes(self):
        """Returns the available times at which data can be read

        Returns
        -------
        np.ndarray
            available times at which data can be read
        """
        return self.time[:,4]

    def ReadUTMetaData(self):
        """Function that performs the reading of the metadata of an ut file
        """
        self.StartReading()

        self.Reset()

        while(True):
            line = self.ReadCleanLine()
            if line == None :
                break
            if line.find("**meshfile")>-1 :
                s = line.split()
                if len(s) == 1 :
                    line = self.ReadCleanLine()
                    self.meshfile = line
                else:
                    self.meshfile = s[-1]
                continue

            if line.find("**node")>-1 :
                s = line.split()
                self.node = s[1:]
                continue

            if line.find("**integ")>-1 :
                s = line.split()
                self.integ = s[1:]
                continue

            if line.find("**element")>-1 :
                s = line.split()
                self.element = s[1:]
                continue

            #all the rest are the times
            s = line.split()

            self.time.append( [b(a) for a,b in zip(s,[int, int, int, int, float] )])
        self.time = np.array(self.time)
        self.EndReading()


    def ReadMetaData(self):
        """Function that performs the reading of the metadata of an ut file, and of the mesh defined in it

        Returns
        -------
        dict
            global information on the mesh defined in the ut file
        """
        self.ReadUTMetaData()

        if self.meshMetadata is not None : return self.meshMetadata

        if self.meshfile[-5:] == ".geof":
            from BasicTools.IO.GeofReader import GeofReader
            GR = GeofReader()
        else:
            from BasicTools.IO.GeoReader import GeoReader
            GR = GeoReader()

        if os.path.isabs(self.meshfile):
            GR.SetFileName(self.meshfile )
        else:
            GR.SetFileName(self.filePath +self.meshfile )
        self.meshMetadata = GR.ReadMetaData()
        return self.meshMetadata


    def SetMeshMetaData(self, meshMetadata):
        """
        To prevent reading the mesh file again in case multiple ut files are related to the same mesh file
        """
        self.meshMetadata = meshMetadata


    def Read(self):
        """Function that performs the reading of the data defined in an ut file

        Returns
        -------
        UnstructuredMesh
            output unstructured mesh object containing reading result
        """
        if self.meshfile[-5:] == ".geof":
            from BasicTools.IO.GeofReader import GeofReader
            GR = GeofReader()
        else:
            from BasicTools.IO.GeoReader import GeoReader
            GR = GeoReader()

        GR.SetFileName(self.filePath + self.meshfile)

        mesh = GR.Read()
        for nodefield in self.node:
            mesh.nodeFields[nodefield] = self.ReadField(fieldname= nodefield)

        return mesh


    def ReadField(self,fieldname = None, time = None, timeIndex = None):
        """Function that performs the reading of a field defined in an ut file

        Parameters
        ----------
        fieldname : str, optional
            name of the field to be read, by default None
        time : float, optional
            time at which the field is read, by default None
        timeIndex : int, optional
            time index at which the field is read, by default None

        Returns
        -------
        np.ndarray
            field read
        """
        self.ReadMetaData()
        postfix = ""
        if self.fileName[-1] == "p":
            postfix = "p"

        self.SetFieldNameToRead(fieldname)
        timeIndex = self.SetTimeToRead(time, timeIndex)

        if timeIndex != self.oldtimeindex:
            self.cache = None
            self.oldtimeindex = timeIndex


        self.PrintVerbose("Reading timeIndex : " + str(timeIndex) )

        basename = ".".join(self.fileName.split(".")[0:-1])
        #find the field to read
        idx = None
        res = None

        nbUsednodes = self.meshMetadata['nbNodes']
        nbNodes = self.meshMetadata['nbNodes']
        nbIntegrationPoints = self.meshMetadata['nbIntegrationPoints']
        nbElements = self.meshMetadata['nbElements']
        IPPerElement = self.meshMetadata['IPPerElement']

        if self.atIntegrationPoints :
            try:
                idx = self.integ.index(self.fieldNameToRead)
                offset =  nbIntegrationPoints * len(self.integ)*timeIndex
                count = nbIntegrationPoints
                ffn = basename + ".integ"
            except:
                raise(Exception("unable to find field " +str(self.fieldNameToRead) ))

            self.PrintVerbose("Opening file : " + str(ffn) )
            res = np.empty(count,dtype=PBasicFloatType)
            try:
                if len(self.integ)==1 :
                    with open(ffn+postfix,"rb") as datafile:
                        datafile.seek(offset*4)
                        res = np.fromfile(datafile ,count=count, dtype=np.float32).byteswap()
                elif np.min(IPPerElement) == np.max(IPPerElement)  :
                    # the .intef file is homogenius
                    with open(ffn+postfix,"rb") as datafile:
                        datafile.seek(offset*4)
                        nip = IPPerElement[0]

                        if self.cache is None:
                            self.cache = np.fromfile(datafile ,count=nip*nbElements* len(self.integ), dtype=np.float32).byteswap()
                            self.cache.shape = (nbElements,nip* len(self.integ))

                        res = self.cache[:,idx*nip:(idx+1)*nip].flatten()
                else:
                    with open(ffn+postfix,"rb") as datafile:
                        self.PrintDebug("Offset : " + str(offset*4))
                        self.PrintDebug("count : " + str(count))
                        datafile.seek(offset*4)
                        cpt =0
                        oldStep = 0
                        for el in range(nbElements):
                            #for sv in range(len(self.integ)):
                                #for ip in range(IPPerElement[el]):
                                    #res[cpt] = np.fromfile(datafile ,count=1, dtype=np.float32).byteswap()

                            nip = IPPerElement[el]
                            oldStep += nip*idx
                            datafile.seek(4*(oldStep),1)
                            res[cpt:cpt +nip] = np.fromfile(datafile ,count=nip, dtype=np.float32).byteswap()
                            cpt += nip

                            oldStep = (len(self.integ)-idx-1)*nip

            except:
                print("Error Reading field : " + str(self.fieldNameToRead) + " (not read)")

        else:
            try:
                idx = self.node.index(self.fieldNameToRead)
                offset = nbNodes * len(self.node)*timeIndex + idx*nbNodes
                count = nbNodes
                ffn = basename + ".node"
            except:
                try:
                    idx = self.integ.index(self.fieldNameToRead)
                    offset = nbUsednodes * len(self.integ)*timeIndex + idx*nbUsednodes
                    count = nbUsednodes
                    ffn = basename + ".ctnod"
                except:
                    raise(Exception("unable to find field " +str(self.fieldNameToRead) + " in file " + self.fileName))

            self.PrintVerbose("Opening file : " + str(ffn) )
            res = None
            try:
                with open(ffn+postfix,"rb") as datafile:
                    self.PrintDebug("Offset : " + str(offset*4))
                    self.PrintDebug("count : " + str(count))
                    datafile.seek(offset*4)
                    res = np.fromfile(datafile ,count=count, dtype=np.float32).byteswap()
            except:
                print("Error Reading field : " + str(self.fieldNameToRead) + " (not read)")

        return res

    def __str__(self):
        res = ""
        res +=  "class UtReader ("+str(id(self)) + ")\n"
        res +=  "  meshfile : "+str(self.meshfile)+ "\n"
        res +=  "  node : "+str(self.node)+ "\n"
        res +=  "  integ : "+str(self.integ)+ "\n"
        res +=  "  element : "+str(self.element)+ "\n"
        res +=  "  times : \n"
        for i in self.time:
            res += "     " +str(i)+ "\n"
        return res

from BasicTools.IO.IOFactory import RegisterReaderClass
RegisterReaderClass(".ut",UtReader)
RegisterReaderClass(".utp",UtReader)

def CheckIntegrity():

    __teststring = u"""
**meshfile cube.geof
**node U1 U2 U3
**integ sig11 sig22 sig33 sig12 sig23 sig31
**element
1 1 1 1 0.000000000000000e+00
1 1 1 1 1.000000000000000e+00
"""
    numberOfnodeVariables = 3
    numberOfIntegVariables = 6
    from BasicTools.Helpers.Tests import WriteTempFile
    from BasicTools.Helpers.Tests import TestTempDir

    # to work on ramdisk
    #TestTempDir.GetTempPath(onRam=True)

    tempfileName = WriteTempFile("UtReaderTest.ut",content=__teststring)

    import BasicTools.TestData as BasicToolsTestData

    import shutil

    shutil.copy(BasicToolsTestData.GetTestDataPath() + "cube.geof",
                TestTempDir.GetTempPath() + "cube.geof")
    reader = UtReader()
    reader.SetFileName(tempfileName)
    reader.ReadMetaData()
    nbNodes = reader.meshMetadata['nbNodes']
    nbIP = reader.meshMetadata['nbIntegrationPoints']
    nbElements = reader.meshMetadata['nbElements']
    IPPerElement = reader.meshMetadata['IPPerElement']
    np.arange(nbNodes*numberOfnodeVariables*2, dtype=np.float32).byteswap().tofile(TestTempDir.GetTempPath() + "UtReaderTest.node")
    off1 = nbNodes*numberOfnodeVariables*2
    (np.arange(nbNodes*numberOfIntegVariables*2, dtype=np.float32)+off1).byteswap().tofile(TestTempDir.GetTempPath() + "UtReaderTest.ctnod")
    off2 = (nbNodes*numberOfnodeVariables*2+nbNodes*numberOfIntegVariables*2)

    ipdata = np.empty((nbElements,numberOfIntegVariables,27)  ,dtype=int)
    for el in range(nbElements):
        nip = IPPerElement[el]
        for sv in range(numberOfIntegVariables):
            for ip in range(nip):
                ipdata[el,sv,ip] = el*10000+ sv*100+ip

    #print(ipdata[:,0,:] )
    #ipdata.astype(np.float32).byteswap().tofile(TestTempDir.GetTempPath() + "UtReaderTest.integ")

    #(np.arange(216*numberOfIntegVariables*27*2, dtype=np.float32)+off2).byteswap().tofile(TestTempDir.GetTempPath() + "UtReaderTest.integ")


    with open(TestTempDir.GetTempPath() + "UtReaderTest.integ","wb") as datafile:
        for i in range(2):
            for el in range(nbElements):
                nip = IPPerElement[el]
                for sv in range(numberOfIntegVariables):
                    for ip in range(nip):
                        np.array(ipdata[el,sv,ip] + i *1000000).astype(np.float32).byteswap().tofile(datafile)

    offset = 0
    for t in [0., 1.]:
        for f in ["U1","U2","U3"]:
            if np.any (reader.ReadField(fieldname=f,time=t) != np.arange(offset, offset+nbNodes, dtype=np.float32) ):
                raise(Exception("Error Reading field " + f ))
            offset += nbNodes

    offset = 0
    for t in [0., 1.]:
        for f in ["sig11","sig22","sig33","sig12","sig23","sig31"]:
            data = reader.ReadField(fieldname=f,time=t)
            if np.any (data !=  np.arange(offset, offset+nbNodes, dtype=np.float32)+off1 ):
                raise(Exception("Error Reading field " + f ))
            offset += nbNodes

    reader.atIntegrationPoints = True
    offset = 0
    for t in [0., 1.]:
        cpt =0
        for f in ["sig11","sig22","sig33","sig12","sig23","sig31"]:

            data = reader.ReadField(fieldname=f,time=t)
            if np.any (data != ipdata[:,cpt,:].ravel()+ t *1000000 ):
                print(data)
                print(' '.join( [ str(int(x)) for x in data[0:30] ] ))
                print(' '.join( [ str(x) for x in ipdata[:,cpt,:].ravel()[0:30] ] ))
                print(len(data)),
                print(ipdata[:,cpt,:].size),
                print(ipdata.shape)

                raise(Exception("Error Reading field " + f ))
            offset += nbIP
            cpt +=1

    ReadFieldFromUt(tempfileName,fieldname="U1",time=0.)
    ReadUTMetaData(tempfileName)

    return "ok"

if __name__ == '__main__':# pragma: no cover
    #from BasicTools.Helpers.BaseOutputObject import BaseOutputObject
    #BaseOutputObject.SetGlobalDebugMode(True)
    import time
    a =  time.time()
    print(CheckIntegrity())# pragma: no cover
    print(time.time() - a)
