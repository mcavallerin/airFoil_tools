# author m.cavallerin 2019

import FreeCAD, FreeCADGui
from FreeCAD import Gui
import Part, math, Draft, os
from FreeCAD import Base
import NACA4_Generator
import matplotlib.pyplot as plt


#--------------------------------------
#Skectching functions
#--------------------------------------

def sketchOnPlane(_foil,element,name,_xOffSet,_zOffSet):

	_name = name + str(element)
	_NACA4 = NACA4_Generator.NACA4_Generator.builderNACA4(_foil)
	_beta = NACA4_Generator.NACA4_Generator.alignOXY(_foil)
	upperList=[]
	lowerList=[]

	FreeCAD.activeDocument().addObject('Sketcher::SketchObjectPython',_name)
	FreeCAD.activeDocument().getObject(_name).addProperty("App::PropertyString","Label2")
	FreeCAD.activeDocument().getObject(_name).Placement = FreeCAD.Placement(FreeCAD.Vector(_xOffSet,0.000000,_zOffSet),FreeCAD.Rotation(FreeCAD.Vector(0.000000,0.000000,1.000000),_beta))
	FreeCAD.activeDocument().getObject(_name).MapMode = "Deactivated"

	for i in range (_NACA4[4]):
			point = FreeCAD.Vector(_NACA4[0][i], _NACA4[1][i], 0)
			upperList.append(point)
			point = FreeCAD.Vector(_NACA4[2][i], _NACA4[3][i], 0)
			lowerList.append(point)
	
	FreeCAD.activeDocument().getObject(_name).addGeometry(Part.BSplineCurve(upperList,None,None,False,3,None,False),False)
	FreeCAD.activeDocument().getObject(_name).addGeometry(Part.BSplineCurve(lowerList,None,None,False,3,None,False),False)
	FreeCAD.activeDocument().getObject(_name).Label2 = _NACA4[5]
	FreeCAD.activeDocument().getObject(_name).ViewObject.Proxy=1
	FreeCAD.activeDocument().getObject(_name).Label = _name
	FreeCAD.activeDocument().recompute()

	element +=1

	return element

def sketchOnRails(_foil,element,name,_xOffSet,_zOffSet): #Curves_integration
	_name = name + str(element)
	_NACA4 = NACA4_Generator.NACA4_Generator.builderNACA4(_foil)
	_beta = NACA4_Generator.NACA4_Generator.alignOXY(_foil)
	upperList=[]


	FreeCAD.activeDocument().addObject('Sketcher::SketchObjectPython',_name)
	FreeCAD.activeDocument().getObject(_name).addProperty("App::PropertyString","Label2")
	FreeCAD.activeDocument().getObject(_name).addProperty("App::PropertyString","Label3")
	FreeCAD.activeDocument().getObject(_name).Placement = FreeCAD.Placement(FreeCAD.Vector(_xOffSet,0.000000,_zOffSet),FreeCAD.Rotation(FreeCAD.Vector(0.000000,0.000000,1.000000),_beta))
	FreeCAD.activeDocument().getObject(_name).MapMode = "Deactivated"

	for i in range (_NACA4[4]):
			point = FreeCAD.Vector(_NACA4[0][i], _NACA4[1][i], 0)
			upperList.append(point)
	
	FreeCAD.activeDocument().getObject(_name).addGeometry(Part.BSplineCurve(upperList,None,None,False,3,None,False),False)
	FreeCAD.activeDocument().getObject(_name).Label2 = _NACA4[5]
	FreeCAD.activeDocument().getObject(_name).Label3 = "High"
	FreeCAD.activeDocument().getObject(_name).ViewObject.Proxy=1
	FreeCAD.activeDocument().getObject(_name).Label = _name
	FreeCAD.activeDocument().recompute()

	element +=1

	_name = name + str(element)
	_NACA4 = NACA4_Generator.NACA4_Generator.builderNACA4(_foil)
	_beta = NACA4_Generator.NACA4_Generator.alignOXY(_foil)
	lowerList=[]


	FreeCAD.activeDocument().addObject('Sketcher::SketchObjectPython',_name)
	FreeCAD.activeDocument().getObject(_name).addProperty("App::PropertyString","Label2")
	FreeCAD.activeDocument().getObject(_name).addProperty("App::PropertyString","Label3")
	FreeCAD.activeDocument().getObject(_name).Placement = FreeCAD.Placement(FreeCAD.Vector(_xOffSet,0.000000,_zOffSet),FreeCAD.Rotation(FreeCAD.Vector(0.000000,0.000000,1.000000),_beta))
	FreeCAD.activeDocument().getObject(_name).MapMode = "Deactivated"

	for i in range (_NACA4[4]):
			point = FreeCAD.Vector(_NACA4[2][i], _NACA4[3][i], 0)
			lowerList.append(point)
	
	FreeCAD.activeDocument().getObject(_name).addGeometry(Part.BSplineCurve(lowerList,None,None,False,3,None,False),False)
	FreeCAD.activeDocument().getObject(_name).Label2 = _NACA4[5]
	FreeCAD.activeDocument().getObject(_name).Label3 = "Low"
	FreeCAD.activeDocument().getObject(_name).ViewObject.Proxy=1
	FreeCAD.activeDocument().getObject(_name).Label = _name
	FreeCAD.activeDocument().recompute()

	element +=1

	return element


#-------------------------------------
#Utilities
#-------------------------------------

def counter(nameSize,Number,objs = []):
	size = len(objs) #number of elements on tree of features
	for j in range(size):
		for i in objs:
			try:
				if int(i.Name[nameSize:]) == Number: #i.Name is a unique read-only property of FreeCAD, if number of element already given, number+1
					Number +=1
			except:
				continue
	return Number

def bubbleSort(alist):
	for passnum in range(len(alist)-1,0,-1):
		for i in range(passnum):
			if alist[i].Placement.Base.z>alist[i+1].Placement.Base.z:
				temp = alist[i]
				alist[i] = alist[i+1]
				alist[i+1] = temp

def splitListSketches(alist, key):
	newList = []
	for i in alist:
		if hasattr (alist[i], "Label3"):
			if alist[i].Label3 == 'Low':
				newList.append(alist[i])
		else:
			return
	return newList

def pathForPipe(List):
	points=[]
	for i in List:
		points.append(i.Placement.Base) #polyline on all origins for airfoils
	wire = Draft.makeWire(points)
	return wire

def pathForRails(List): #needs a getSelectionEx() List
	#define two dummy FreeCAD.Vector

	V1 = FreeCAD.Vector()
	V2 = FreeCAD.Vector()
	Coord = ['x','y','z'] #define iterator for coordinates coordinates
	for i in range(len(List)-1):
		for j in Coord:
			V1.Coord[j] = List.sel[i+1].Shape.Edges[0].Vertexes[i+1].Coord[j]
			V2.Coord[j] = List.sel[i].Shape.Edges[0].Vertexes[i].Coord[j]
	points = [V1,V2]
	pl = FreeCAD.Placement()
	line = Draft.makeWire(points,placement=pl,closed=False,face=True,support=None)
	return line

#-------------------------
#Plot Functions
#-------------------------

def airFoilPlot(_foil):
		'''use matplotlib to plot NACA4 air foil'''	
		_NACA4 = NACA4_Generator.NACA4_Generator.builderNACA4(_foil)
		
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
