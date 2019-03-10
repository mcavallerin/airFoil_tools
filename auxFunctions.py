# author m.cavallerin 2019

import FreeCAD, FreeCADGui
from FreeCAD import Gui
import Part, math, Draft, os, sys
from FreeCAD import Base
import NACA4_Generator
import matplotlib.pyplot as plt

sys.path.append(os.path.expandvars("/home/$USER/.FreeCAD/Mod/Curves"))
import Sweep2Rails as S2R


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
		if hasattr (i, "Label3"):
			if i.Label3 == key:
				newList.append(i)
		else:
			return
	return newList

def pathForPipe(List):
	points=[]
	for i in List:
		points.append(i.Placement.Base) #polyline on all origins for airfoils
	wire = Draft.makeWire(points)
	return wire

def geoForRails(List): #needs a getSelectionEx() List
	#define two dummy FreeCAD
	listOfG = []
	V1 = FreeCAD.Vector()
	V2 = FreeCAD.Vector()
	for j in range(len(List)):
		name = 'line'+str(j)
		for i in range(len(List)-1):
			V1.x = List[i].Shape.Edges[0].Vertexes[j].Point.x
			V2.x = List[i+1].Shape.Edges[0].Vertexes[j].Point.x
			V1.y = List[i].Shape.Edges[0].Vertexes[j].Point.y
			V2.y = List[i+1].Shape.Edges[0].Vertexes[j].Point.y
			V1.z = List[i].Shape.Edges[0].Vertexes[j].Point.z
			V2.z = List[i+1].Shape.Edges[0].Vertexes[j].Point.z
			points = [V1,V2]
			pl = FreeCAD.Placement()
			name = Draft.makeWire(points,placement=pl,closed=False,face=True,support=None)
			FreeCAD.ActiveDocument.recompute()
		listOfG.append(name)
	plane = FreeCAD.ActiveDocument.addObject('Part::RuledSurface', 'Ruled Surface')
	FreeCAD.ActiveDocument.ActiveObject.Curve1=(listOfG[0],[''])
	FreeCAD.ActiveDocument.ActiveObject.Curve2=(listOfG[1],[''])
	FreeCAD.ActiveDocument.recompute()
	List.append(plane) 
	return List

def foilToRails(List,key): 

    myS2R = FreeCAD.ActiveDocument.addObject("App::FeaturePython",key)
    S2R.sweep2rails(myS2R)
    S2R.sweep2railsVP(myS2R.ViewObject)

    parseList = S2R.s2rCommand()
    myS2R.Birail = parseList.parseSel(List)[0]
    myS2R.Profiles = parseList.parseSel(List)[1]

    myS2R.Birail.ViewObject.Visibility = False
    for p in myS2R.Profiles:
        p.ViewObject.Visibility = False
	FreeCAD.ActiveDocument.recompute()

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
