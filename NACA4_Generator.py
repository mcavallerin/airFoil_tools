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
	
	def __init__(self):
		pass

	def _Yt (self,maxThick,x): #maxSpessore
		A =  0.2969*math.pow(x,0.5)
		B =  0.1260*math.pow(x,1)
		C =  0.3516*math.pow(x,2)
		D =  0.2843*math.pow(x,3)
		E =  0.1036*math.pow(x,4)
		return (maxThick/100.)*5*(A-B-C+D-E)

	def _Yc (self,m,p,x): #linea mediana
		m = m/100.
		p = p/10.
		if (x<=p):
			return m/math.pow(p,2)*(2*p*x-math.pow(x,2))
		else:
			return m/math.pow(1-p,2)*(1-2*p+2*p*x-math.pow(x,2))
	def _dYc (self,m,p,x): #gradiente di flessione della linea mediana
		m = m/100.
		p = p/10.
		if (x<=p):
			return 2*m/math.pow(p,2)*(p-x)
		else:
			return 2*m/math.pow((1-p),2)*(p-x)

#-------------------------
#builder functions
#-------------------------

	def builderNACA4(self,m, p, TH, chord, resolution, interpolation):
			
		Xp = np.linspace(0,1,resolution)	#list of points on X Axis equally spaced default

		if interpolation == 1:	
			beta = np.linspace(0,math.pi,resolution)
			for i in range(resolution):
				Xp[i] = 0.5*(1-math.cos(beta[i]))

		Yt      = np.linspace(0,1,resolution)					#list of point for thickness
		teta    = np.linspace(0,1,resolution)					#list of point for gradient
		Xu      = np.linspace(0,1,resolution)					#list of point on Xupper Axis				
		Xl      = np.linspace(0,1,resolution)					#list of point on Xlower Axis
		Yu      = np.linspace(0,1,resolution)					#list of point on Yupper Axis
		Yl      = np.linspace(0,1,resolution)					#list of point on YLower Axis
		if m==0 and p ==0:
			for i in range(resolution):
				Yt[i]   = self._Yt(TH,Xp[i])
				Xu[i]   = Xp[i]*chord
				Xl[i]   = Xp[i]*chord
				Yu[i]   = Yt[i]*chord
				Yl[i]   = Yt[i]*chord*(-1)	
		else:		
			for i in range(resolution):  
				Yt[i]   = self._Yt(TH,Xp[i])
				teta[i] = math.atan(self._dYc(m,p,Xp[i]))
				Xu[i]   = (Xp[i]-Yt[i]*math.sin(teta[i]))*chord
				Xl[i]   = (Xp[i]+Yt[i]*math.sin(teta[i]))*chord
				Yu[i]   = (self._Yc(m,p,Xp[i])+Yt[i]*math.cos(teta[i]))*chord
				Yl[i]   = (self._Yc(m,p,Xp[i])-Yt[i]*math.cos(teta[i]))*chord
			
		NACA4=[]
		NACA4.append(Xu)
		NACA4.append(Yu)
		NACA4.append(Xl)
		NACA4.append(Yl)
		NACA4.append(resolution)

		return NACA4

#--------------------------
#plotting/drawing functions
#--------------------------

	def drawAirFoil(self,_NACA4,_xOffSet,_zOffSet):
		'''generate splines'''
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

	def airFoilPlot(self,_NACA4):
		'''use matplotlib to plot NACA4 air foil'''	
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



