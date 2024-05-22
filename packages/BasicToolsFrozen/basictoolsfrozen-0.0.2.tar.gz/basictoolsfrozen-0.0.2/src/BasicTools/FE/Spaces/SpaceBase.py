# -*- coding: utf-8 -*-
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
#

import numpy as np

from BasicTools.Helpers.BaseOutputObject import BaseOutputObject
from BasicTools.NumpyDefs import PBasicFloatType

class SpaceBase(BaseOutputObject):
    """Base class for a finite element interpolation space for one type of element
    """
    def __init__(self):
        super(SpaceBase,self).__init__()
        self.name = None
        self.fromConnectivityCompatible = False

    def Create(self):
        pass

    @property
    def geoSupport(self):
        return self._geoSupport

    @geoSupport.setter
    def geoSupport(self,gs):
        self._geoSupport = gs

    def GetDimensionality(self):
        return self.geoSupport.dimensionality; #pragma: no cover

    def SetIntegrationRule(self, points, weights):
        raise NotImplementedError("SetIntegrationRule not implemented")

    def ClampParamCoorninates(self,xietaphi):
        """ Clamps the xi eta and phi to othe intervals [0,1] for the first dim coordinates,
        the others are set to zero """
        res = xietaphi.copy()
        for cpt, d in enumerate(xietaphi):
            if cpt < self.GetDimensionality():
                res[cpt] = max(0.,d)
                res[cpt] = min(1.,res[cpt])
            else:
                res[cpt] = 0
        return res

    def GetNormal(self, Jacobian):
        # Edge in 2D
        if Jacobian.shape[0] == 1 and Jacobian.shape[1] == 2 :
            res = np.array([Jacobian[0,1],-Jacobian[0,0]],dtype =PBasicFloatType)
            #res = np.array([Jack[1,:] -Jack[0,:]],dtype =PBasicFloatType) #ANCIENNE VERSION

        # Edge in 3D, we return the xy projection of the normal
        elif Jacobian.shape[0] == 1 and Jacobian.shape[1] == 3 :
            res = np.array([Jacobian[0,1],-Jacobian[0,0]],dtype =PBasicFloatType)

        # surface in 3D
        elif Jacobian.shape[0] == 2 and Jacobian.shape[1] == 3 :
            res =  np.cross(Jacobian[0,:],Jacobian[1,:])
        else:
            print("Shape of Jacobian not coherent. Possible error: an elset has the same name of the considered faset")

        #normalisation
        res /= np.linalg.norm(res)
        return res

    def GetJackAndDet(self,Nfder, xcoor):
        """Deprecated Please use GetJacobianDeterminantAndInverse """
        return self.GetJacobianDeterminantAndInverse(Nfder, xcoor)

    def GetJacobianDeterminantAndInverse(self, Nfder, xcoor):

       dim = self.GetDimensionality()

       if dim == 0:
           return np.array([[1.]]), 1, lambda x:x

       Jacobian = np.dot(Nfder, xcoor)

       s = xcoor.shape[1]

       if dim == s:
            Jdet = np.linalg.det(Jacobian)

            if dim == 3:
               def jinv(vec,jack=Jacobian):
                   m1, m2, m3, m4, m5, m6, m7, m8, m9 = jack.flatten()
                   determinant = m1*m5*m9 + m4*m8*m3 + m7*m2*m6 - m1*m6*m8 - m3*m5*m7 - m2*m4*m9
                   return np.dot(np.array([[m5*m9-m6*m8, m3*m8-m2*m9, m2*m6-m3*m5],
                       [m6*m7-m4*m9, m1*m9-m3*m7, m3*m4-m1*m6],
                       [m4*m8-m5*m7, m2*m7-m1*m8, m1*m5-m2*m4]]),vec) /determinant
               return Jacobian, Jdet, jinv
            elif dim == 2:
               return Jacobian, Jdet, np.linalg.inv(Jacobian).dot
       elif dim == 0:
           Jdet = 1
       elif dim == 1:
           Jdet = np.linalg.norm(Jacobian)
       elif dim == 2:
           Jdet = np.linalg.norm(np.cross (Jacobian[0,:],Jacobian[1,:]))

       q,r = np.linalg.qr(Jacobian)
       qt = q.T

       jinv = lambda vec,qt=qt,r=r: np.linalg.lstsq(r, np.dot(qt,vec), rcond = None)[0]

       return Jacobian, Jdet, jinv

class SpaceAtIntegrationPoints():
    def __init__(self,space = None, points = None, weights = None):

        if space is not None and points is not None and weights is not None:
            self.SetIntegrationRule( space, points, weights)
        else:
            self.nbPoints =  0
            self.space = None
            self.weights = None
            self.points = None
            self.valN = [None]*self.nbPoints
            self.valdphidxi = [None]*self.nbPoints

    def SetIntegrationRule(self, space, points, weights):
        self.space = space
        self.weights = weights
        self.points = points
        self.nbPoints = len(weights)

        self.valN = [None]*self.nbPoints
        self.valdphidxi = [None]*self.nbPoints

        for pp in range(self.nbPoints):
           point = points[pp]
           self.valN[pp] = space.GetShapeFunc(point)
           self.valdphidxi[pp] = space.GetShapeFuncDer(point)

    def GetJacobianDeterminantAndInverseAtIP(self, pp, xcoor):
        return self.GetJacobianDeterminantAndInverse(self.valdphidxi[pp], xcoor)

    def GetJacobianDeterminantAndInverse(self, Nfder, xcoor):
        return self.space.GetJacobianDeterminantAndInverse(self, Nfder, xcoor)

    def GetJackAndDetI(self, pp, xcoor):
        """Deprecated Please use GetJacobianDeterminantAndInverseAtIP """
        return self.GetJackAndDet(self.valdphidxi[pp], xcoor)

    def GetJackAndDet(self, Nfder, xcoor):
        """Deprecated Please use GetJacobianDeterminantAndInverse """
        return self.space.GetJackAndDet(Nfder, xcoor)

    def GetNormal(self,Jack):
        return self.space.GetNormal(Jack)
