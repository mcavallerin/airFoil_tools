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

class NACA4_Generator:
	
	def __init__(self, m=4, p=4, TH=12, chord=100, resolution=100, interpolation=1):
				self.m 				= m
				self.p 				= p
				self.TH 			= TH
				self.chord			= chord
				self.resolution		 = resolution
				self.interpolation	  = interpolation
			

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
		m = self.m/100.
		p = self.p/10.
		if (x<=self.p):
			return m/math.pow(p,2)*(2*p*x-math.pow(x,2))
		else:
			return m/math.pow((1-p),2)*(1-2*p+2*p*x-math.pow(x,2))

	def _dYc (self,x):
		'''gradient of chamber line'''
		m = self.m/100.
		p = self.p/10.
		if (x<=p):
			return 2*m/math.pow(p,2)*(p-x)
		else:
			return 2*m/math.pow((1-p),2)*(p-x)

	def _Xp(self, resolution):
			
		Xp = np.linspace(0,1,self.resolution)	#list of points on X Axis equally spaced default

		if self.interpolation == 1:	
			beta = np.linspace(0,math.pi,self.resolution)
			for i in range(self.resolution):
				Xp[i] = 0.5*(1-math.cos(beta[i]))
		
		return Xp

#-------------------------
#builder functions
#-------------------------

	def builderNACA4(self):
			
#		Xp = np.linspace(0,1,self.resolution)	#list of points on X Axis equally spaced default

#		if self.interpolation == 1:	
#			beta = np.linspace(0,math.pi,self.resolution)
#			for i in range(self.resolution):
#				Xp[i] = 0.5*(1-math.cos(beta[i]))
		Xp = self._Xp(self.resolution)

		Yt	  = np.linspace(0,1,self.resolution)				#list of point for thickness
		teta	= np.linspace(0,1,self.resolution)					#list of point for gradient
		Xu	  = np.linspace(0,1,self.resolution)					#list of point on Xupper Axis				
		Xl	  = np.linspace(0,1,self.resolution)					#list of point on Xlower Axis
		Yu	  = np.linspace(0,1,self.resolution)					#list of point on Yupper Axis
		Yl	  = np.linspace(0,1,self.resolution)					#list of point on YLower Axis
		Yc    = np.linspace(0,1,self.resolution)					#list of point on chamber line
		if (self.m==0 and self.p ==0):
			for i in range(self.resolution):
				Yt[i]   = self._Yt(self.TH,Xp[i])
				Xu[i]   = Xp[i]*self.chord
				Xl[i]   = Xp[i]*self.chord
				Yu[i]   = Yt[i]*self.chord
				Yl[i]   = Yt[i]*self.chord*(-1)
				Yc[i]	= Xp[i] #dummy
		else:		
			for i in range(self.resolution):  
				Yt[i]   = self._Yt(self.TH,Xp[i])
				teta[i] = math.atan(self._dYc(Xp[i]))
				Xu[i]   = (Xp[i]-Yt[i]*math.sin(teta[i]))*self.chord
				Xl[i]   = (Xp[i]+Yt[i]*math.sin(teta[i]))*self.chord
				Yu[i]   = (self._Yc(Xp[i])+Yt[i]*math.cos(teta[i]))*self.chord
				Yl[i]   = (self._Yc(Xp[i])-Yt[i]*math.cos(teta[i]))*self.chord
				Yc[i]	= (self._Yc(Xp[i]))*self.chord
		
		#coincident constrain for points on CAD
		Xl[0] = Xu[0]
		Yl[0] = Yu[0]
		Xl[-1] = Xu[-1]
		Yl[-1] = Yu[-1]
		


		NACA4=[]
		NACA4.append(Xu)
		NACA4.append(Yu)
		NACA4.append(Xl)
		NACA4.append(Yl)
		NACA4.append(self.resolution)
		NACA4.append(str(self.m)+str(self.p)+str(self.TH)+"c"+str(self.chord)+"r"+str(self.resolution))
		NACA4.append(Yc)

		return NACA4

	def alignOXY (self):
		'''to calculate rotation angle and align the foil to origin'''
		Xp = self._Xp(self.resolution)		
		Yt   = self._Yt(self.TH,Xp[-1])
		teta = math.atan(self._dYc(Xp[-1]))
		Xu   = (Xp[-1]-Yt*math.sin(teta))*self.chord
		print (Xu)
		Yc	= (self._Yc(Xp[-1]))*self.chord
		print (Yc)
		beta = math.degrees(math.atan(Yc/Xu)) #alignment angle			
		return -beta

#--------------------------
#drawing functions
#--------------------------

def sketchOnPlane(_foil,element,name,_zOffSet):

	_name = name + str(element)
	_NACA4 = NACA4_Generator.builderNACA4(_foil)
	_beta = NACA4_Generator.alignOXY(_foil)
	print (_beta)
	upperList=[]
	lowerList=[]

	FreeCAD.activeDocument().addObject('Sketcher::SketchObject',_name)
	FreeCAD.activeDocument().getObject(_name).Placement = FreeCAD.Placement(FreeCAD.Vector(0.000000,0.000000,_zOffSet),FreeCAD.Rotation(FreeCAD.Vector(0.000000,0.000000,1.000000),_beta))
	FreeCAD.activeDocument().getObject(_name).MapMode = "Deactivated"

	for i in range (_NACA4[4]):
			point = FreeCAD.Vector(_NACA4[0][i], _NACA4[1][i], 0)
			upperList.append(point)
			point = FreeCAD.Vector(_NACA4[2][i], _NACA4[3][i], 0)
			lowerList.append(point)
	
	FreeCAD.activeDocument().getObject(_name).addGeometry(Part.BSplineCurve(upperList,None,None,False,3,None,False),False)
	FreeCAD.activeDocument().getObject(_name).addGeometry(Part.BSplineCurve(lowerList,None,None,False,3,None,False),False)
	FreeCAD.activeDocument().getObject(_name).Label2 = _NACA4[5]

	element +=1

	return element

#--------------------------
#plotting functions
#--------------------------

def airFoilPlot(_foil):
		'''use matplotlib to plot NACA4 air foil'''	
		_NACA4 = NACA4_Generator.builderNACA4(_foil)
		
		lista = [[],[],[],[],[]]
		
		for j in range (4):
				for i in range (_NACA4[4]):
						if j%2==0:
								lista[j].append(_NACA4[j][i])
						else:
								lista[j].append(_NACA4[j][i])
		
		for i in range (_NACA4[4]):
			lista[4].append(_NACA4[6][i])

		plt.figure(figsize=(10,2))
		plt.plot(lista[0],lista[1])
		plt.plot(lista[2],lista[3])
		plt.plot(lista[0],lista[4])
		plt.show()

#-----------------------------------------------------------------------------------------



