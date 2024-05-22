# -*- coding: utf-8 -*-
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
#


import numpy as np
from sympy.matrices import Matrix
import BasicTools.Containers.ElementNames as EN
from BasicTools.FE.Spaces.SymSpace import SymSpaceBase
from BasicTools.NumpyDefs import PBasicFloatType


class TriSpaceBase(SymSpaceBase):
    def __init__(self):
        super(TriSpaceBase,self).__init__()
        self.dimensionality = 2
        self.geoSupport = EN.GeoTri
    def ClampParamCoorninates(self,xietaphi):
        res = xietaphi.copy()
        if res[0]+res[1] > 1:
            dif = res[0]-res[1]
            res[0] = (1+dif)/2.
            res[1] = 1.-res[0]
        res[0] = max(min(res[0],1),0)
        res[1] = max(min(res[1],1),0)
        return res

class Tri_P0_Global(TriSpaceBase):
    def __init__(self):
        super(Tri_P0_Global,self).__init__()
        self.symN = Matrix([1])
        self.posN = np.array([[None,None]])
        self.dofAttachments = [("G",None,None)]

class Tri_P0_Lagrange(TriSpaceBase):
    def __init__(self):
        super(Tri_P0_Lagrange,self).__init__()
        self.symN = Matrix([1])
        self.posN = np.array([[0.33,0.33]])
        self.dofAttachments = [("C",0,None) ]

class Tri_P1_Lagrange(TriSpaceBase):
    def __init__(self):
        super(Tri_P1_Lagrange,self).__init__()
        xi = self.xi
        eta = self.eta
        self.symN = Matrix([(1-xi-eta), xi,eta])
        self.posN = np.array([[0,0],
                              [1,0],
                              [0,1]])

        self.dofAttachments = [("P",0,None),
                               ("P",1,None),
                               ("P",2,None) ]

class Tri_P1Bulle_Lagrange(TriSpaceBase):
    def __init__(self):
        super(Tri_P1Bulle_Lagrange,self).__init__()

        xi = self.xi
        eta = self.eta
        self.symN = Matrix([(1-xi-eta), xi,eta, -1*(xi+eta-1)*xi*eta/27 ])
        self.posN = np.array([[0,0],
                              [1,0],
                              [0,1],
                              [1./3.,1./3.],
                              ])

        self.dofAttachments = [("P",0,None),
                               ("P",1,None),
                               ("P",2,None),
                               ("C",0,None),
                               ]

class Tri_P2_Lagrange(TriSpaceBase):
    def __init__(self):
        super(Tri_P2_Lagrange,self).__init__()

        xi = self.xi
        eta = self.eta

        T = (1-xi-eta)

        self.symN = Matrix([T*(1-2*xi-2*eta),
                            xi *(2*xi-1),
                            eta*(2*eta-1),
                            4*xi*T,
                            4*xi*eta,
                            4*eta*T])

        self.posN = np.array([[0,0],
                              [1,0],
                              [0,1],
                              [0.5,0],
                              [0.5,0.5],
                              [0,0.5]])

#        self.dofAttachments = [("P",0,None),
#                               ("P",2,None),
#                               ("F",1,None),
#                               ("P",1,None),
#                               ("F",0,None),
#                               ("F",2,None)]
        self.dofAttachments = [("P",0,None),
                               ("P",1,None),
                               ("P",2,None),
                               ("F",0,None),
                               ("F",1,None),
                               ("F",2,None)]


def plot2DTriangle(Space):
    import matplotlib.pyplot as plt
    import matplotlib.tri as mtri
    # Create triangulation.
    x = np.asarray([0,1,2,3,4,5,6,0,1,2,3,4,5,0,1,2,3,4,0,1,2,3,0,1,2,0,1,0],dtype=PBasicFloatType)/6.0
    y = np.asarray([0,0,0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,2,3,3,3,3,4,4,4,5,5,6],dtype=PBasicFloatType)/6.0
    triangles = [[ 0, 1, 7],[ 1, 2, 8],[ 2, 3, 9],[ 3, 4, 10], [ 4, 5, 11], [5, 6, 12],
                 [ 1, 8, 7],[ 2, 9, 8],[ 3,10, 9],[ 4,11, 10], [ 5,12, 11],
                 [ 7, 8,13],[ 8, 9,14],[ 9,10,15],[10, 11,16], [11, 12,17],
                 [ 8,14,13],[ 9,15,14],[10,16,15],[11,17,16],
                 [13,14,18],[14,15,19],[15,16,20],[16,17,21],
                 [14,19,18],[15,20,19],[16,21,20],
                 [18,19,22],[19,20,23],[20,21,24],
                 [19,23,22],[20,24,23],
                 [22,23,25],[23,24,26],
                 [23,26,25],
                 [25,26,27],
             ]

    triang = mtri.Triangulation(x, y, triangles)

    z = np.empty((28),dtype=PBasicFloatType)
    print (x)
    print (y)

    for sf in range(Space.posN.shape[0]):
        for i in range(len(x)):
            #z[i] = Space.GetShapeFuncDer([x[i],y[i]])[1,sf]
            z[i] = Space.GetShapeFunc([x[i],y[i]])[sf]
            print(z[i])
        from mpl_toolkits.mplot3d import Axes3D
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        #surf = ax.plot_surface(x, y, z, linewidth=0) #, facecolors=colors
        ax.plot_trisurf(x, y, z, triangles=triangles, cmap=plt.cm.Spectral)
        #plt.plot_trisurf(triang, z)

        #plt.tricontour(triang,z)
        #plt.triplot(triang, 'ko-')
        plt.title('Triangular grid' + str(type(Space)) + " phi : " + str(sf))
        plt.show()
        plt.pause(1)

def CheckIntegrity(GUI=False):
    if GUI:
        plot2DTriangle(Tri_P0_Lagrange())
        plot2DTriangle(Tri_P1_Lagrange())
        plot2DTriangle(Tri_P1Bulle_Lagrange())
        plot2DTriangle(Tri_P2_Lagrange())

    return "OK"


if __name__ == '__main__':
    print(CheckIntegrity(True))# pragma: no cover
