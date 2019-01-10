#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Part, math
from FreeCAD import Base
import FreeCADGui
import FreeCAD
import DraftVecUtils
import Draft
import math
import numpy as np
import matplotlib.pyplot as plt
#se nel costruttore definisco le variabili base, i metodi seguenti non devono ricevere dei parametri perchè li ereditano dal costruttore iniziale
class NACA4_Generator:
	
	def __init__(self, m, p, TH, chord, resolution, interpolation):
		self.m 		        = m
		self.p 		        = p
		self.TH 	        = TH
		self.chord	        = chord
		self.resolution         = resolution
		self.interpolation      = interpolation

	def _Yt (self,_TH,x):
		'''max thickness'''
		A =  0.2969*math.pow(x,0.5)
		B =  0.1260*math.pow(x,1)
		C =  0.3516*math.pow(x,2)
		D =  0.2843*math.pow(x,3)
		E =  0.1036*math.pow(x,4)
		return (_TH/100.)*5*(A-B-C+D-E)

	def _Yc (self,x):
		'''chamber line'''
		self.m = self.m/100.
		self.p = self.p/10.
		if (x<=self.p):
			return self.m/math.pow(self.p,2)*(2*self.p*x-math.pow(x,2))
		else:
			return self.m/math.pow(1-self.p,2)*(1-2*self.p+2*self.p*x-math.pow(x,2))

	def _dYc (self,x):
		'''gradient of chamber line'''
		m = self.m/100.
		p = self.p/10.
		if (x<=p):
			return 2*m/math.pow(p,2)*(p-x)
		else:
			return 2*m/math.pow((1-p),2)*(p-x)

#-------------------------
#builder functions
#-------------------------

	def builderNACA4(self):
			
		Xp = np.linspace(0,1,self.resolution)	#list of points on X Axis equally spaced default

		if self.interpolation == 1:	
			beta = np.linspace(0,math.pi,self.resolution)
			for i in range(self.resolution):
				Xp[i] = 0.5*(1-math.cos(beta[i]))

		Yt      = np.linspace(0,1,self.resolution)					#list of point for thickness
		teta    = np.linspace(0,1,self.resolution)					#list of point for gradient
		Xu      = np.linspace(0,1,self.resolution)					#list of point on Xupper Axis				
		Xl      = np.linspace(0,1,self.resolution)					#list of point on Xlower Axis
		Yu      = np.linspace(0,1,self.resolution)					#list of point on Yupper Axis
		Yl      = np.linspace(0,1,self.resolution)					#list of point on YLower Axis
		if self.m==0 and self.p ==0:
			for i in range(self.resolution):
				Yt[i]   = self._Yt(self.TH,Xp[i])
				Xu[i]   = Xp[i]*self.chord
				Xl[i]   = Xp[i]*self.chord
				Yu[i]   = Yt[i]*self.chord
				Yl[i]   = Yt[i]*self.chord*(-1)	
		else:		
			for i in range(self.resolution):  
				Yt[i]   = self._Yt(self.TH,Xp[i])
				teta[i] = math.atan(self._dYc(Xp[i]))
				Xu[i]   = (Xp[i]-Yt[i]*math.sin(teta[i]))*self.chord
				Xl[i]   = (Xp[i]+Yt[i]*math.sin(teta[i]))*self.chord
				Yu[i]   = (self._Yc(Xp[i])+Yt[i]*math.cos(teta[i]))*self.chord
				Yl[i]   = (self._Yc(Xp[i])-Yt[i]*math.cos(teta[i]))*self.chord
			
		NACA4=[]
		NACA4.append(Xu)
		NACA4.append(Yu)
		NACA4.append(Xl)
		NACA4.append(Yl)
		NACA4.append(self.resolution)

		return NACA4

#--------------------------
#plotting/drawing functions
#--------------------------

def drawAirFoil(_foil,_xOffSet,_zOffSet):
        '''generate splines'''
        _NACA4 = NACA4_Generator.builderNACA4(_foil)
        upperList=[]
        lowerList=[]
        for i in range (_NACA4[4]):
                point = FreeCAD.Vector(_NACA4[0][i]+_xOffSet, _NACA4[1][i], _zOffSet)
                upperList.append(point)
                point = FreeCAD.Vector(_NACA4[2][i]+_xOffSet, _NACA4[3][i], _zOffSet)
                lowerList.append(point)

        Draft.makeBSpline(upperList, closed=False)
        Draft.makeBSpline(lowerList, closed=False)
        FreeCADGui.activeDocument().activeView().viewAxonometric()
        FreeCADGui.SendMsgToActiveView("ViewFit")

def airFoilPlot(_foil):
        '''use matplotlib to plot NACA4 air foil'''	
        _NACA4 = NACA4_Generator.builderNACA4(_foil)
        lista = [[],[],[],[]]
        
        for j in range (4):
                for i in range (_NACA4[4]):
                        if j%2==0:
                                lista[j].append(_NACA4[j][i])
                        else:
                                lista[j].append(_NACA4[j][i])
                
        plt.figure(figsize=(10,2))
        plt.plot(lista[0],lista[1],lista[0],lista[3])
        plt.show()


#-----------------------------------------------------------------------------------------



