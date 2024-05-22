# -*- coding: utf-8 -*-
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
#

"""Gcode file reader
"""

import numpy as np

import BasicTools.Containers.ElementNames as EN
import BasicTools.Containers.UnstructuredMesh  as UM

from BasicTools.IO.ReaderBase import ReaderBase
from BasicTools.NumpyDefs import PBasicFloatType, PBasicIndexType


def ReadGCode(fileName=None,string=None ):
    """Function API for reading a Gcode mesh file

    Parameters
    ----------
    fileName : str, optional
        name of the file to be read, by default None
    string : str, optional
        data to be read as a string instead of a file, by default None

    Returns
    -------
    UnstructuredMesh
        output unstructured mesh object containing reading result
    """
    reader = GReader()
    reader.SetFileName(fileName)
    reader.SetStringToRead(string)
    return reader.Read()

class GReader(ReaderBase):
    """Gcode Reader class
    """
    def __init__(self):
        super(GReader,self).__init__()


    def Read(self):
        """Function that performs the reading of an Gcode file

        Returns
        -------
        UnstructuredMesh
            output unstructured mesh object containing reading result
        """
        extrudeur = 0

        self.StartReading()
        res = UM.UnstructuredMesh()
        res.nodes = np.empty((0,3), float)

        currentposx = 0.
        currentposy = 0.
        currentposz = 0.
        nodes = []
        thicknes = []
        firsttime = True
        for line in self.filePointer:
            l = line.strip('\n').lstrip().rstrip()
            #empty line
            if len(l) == 0: continue
            #comment
            if l[0] == ";": continue
            l = l.split(';')[0]
            st = l.split()

            if st[0][0] == "N":
                st.pop(0)


            if st[0][0:2] == "G0" or st[0] == "G1" or st[0][0] == "X" or st[0][0] == "Y"or st[0][0] == "Z":
                thi = 0
                for s in st:
                    if s[0] == "X":
                        currentposx = float(s[1:])
                    if s[0] == "Y":
                        currentposy = float(s[1:])
                    if s[0] == "Z":
                        currentposz = float(s[1:])
                    if s[0] == "E":
                        val = float(s[1:])
                        if val > extrudeur :
                            thi = 1
                        else:# pragma: no cover
                            thi = 0
                        extrudeur = val

                if firsttime:
                    firsttime = False
                else :
                    thicknes.append(thi)
                nodes.append(currentposx)
                nodes.append(currentposy)
                nodes.append(currentposz)

                continue
            if st[0] == "G92":
                for s in st:
                    if s[0] == "E":
                        extrudeur = float(s[1:])
                continue

            if st[0] == "M106":
                continue

            print("ignoring line " + str(l) )
        self.EndReading()

        res.nodes = np.reshape(np.asarray(nodes,dtype=PBasicFloatType),newshape=(len(nodes)//3, 3))

        res.originalIDNodes = np.arange(res.GetNumberOfNodes(),dtype=PBasicIndexType)
        elems = res.GetElementsOfType(EN.Bar_2)
        elems.Allocate(res.GetNumberOfNodes()-1)
        elems.connectivity[:,0] = range(res.GetNumberOfNodes()-1)
        elems.connectivity[:,1] = range(1,res.GetNumberOfNodes())
        res.elemFields = {}
        G = np.array(thicknes)

        G.shape =  (res.GetNumberOfNodes()-1,1)
        res.elemFields['OnOff'] = G
        return res

from BasicTools.IO.IOFactory import RegisterReaderClass
RegisterReaderClass(".gcode",GReader)

def CheckIntegrity():
    from BasicTools.TestData import GetTestDataPath

    res = ReadGCode(fileName=GetTestDataPath()+ "GCodeTest.gcode" )

    print(res)

    return 'ok'

if __name__ == '__main__':
    print(CheckIntegrity())# pragma: no cover
