# author m.cavallerin 2019

import FreeCAD, FreeCADGui
from FreeCAD import Gui
import Part, math, Draft, os
from FreeCAD import Base
import PopUpMenu, NACA4_Generator
from PySide import QtGui, QtCore
import auxFunctions, errorMessage


class airFoil2D():	#part Design method
	
	def GetResources(self):
		os.environ["USER"]
		return {'Pixmap'  : os.path.expandvars("/home/$USER") + ("/.FreeCAD/Mod/airFoil_tools/Resources/icons/airFoilShaper.png"), # the name of a svg file available in the resources
			'Accel' : "Shift+S",
			'MenuText': "airFoil2D",
			'ToolTip' : "airFoil2D: Create new sections for airFoil on sketches; actually only NACA4 digit is supported"}

	def Activated(self, element = 0, name = 'foilSketch'):
		self.element = element
		self.name = name
		N = len(self.name)
		if FreeCAD.activeDocument() == None:
			errorMessage.errors("noFileOpen")
			return

		obj = FreeCAD.ActiveDocument.Objects
		self.element = auxFunctions.counter(N,self.element,obj) #renumbering function in order to have unique name for objects
		staticmethod(airFoilSketcher(self.element, self.name))
		FreeCAD.Console.PrintMessage("new section for wing" + "\n")
		return

	def IsActive(self):
			"""Here you can define if the command must be active or not (greyed) if certain conditions
			are met or not. This function is optional."""
			return True

Gui.addCommand('airFoil2D', airFoil2D())


class wingExtruderPipe():	
	
	def GetResources(self):
		os.environ["USER"]
		return {'Pixmap'  : os.path.expandvars("/home/$USER") + ("/.FreeCAD/Mod/airFoil_tools/Resources/icons/airFoilSketcher.png"), # the name of a svg file available in the resources
			'Accel' : "Shift+S",
			'MenuText': "wingExtruderPipe",
			'ToolTip' : "wingExtruderPipe: Generates solid feature and body using additive pipe PartDesign Feature"}

	def Activated(self, sel = [], element = 0, name = 'foilWing'):

		self.sel = FreeCADGui.Selection.getSelection()
		self.name = name
		self.element = element

		if FreeCAD.activeDocument() == None:
			errorMessage.errors("noFileOpen")
			return
		if len(self.sel) == 0 or len(self.sel) <2:
			errorMessage.errors("wrongSelection1")
			return

		N = len(self.name)
		obj = FreeCAD.ActiveDocument.Objects
		self.element = auxFunctions.counter(N,self.element,obj) #renumbering function in order to have unique name for objects
		wing = self.name + str(self.element)
		solid = "solid" + str(self.element)


		if self.checkPositioning()!=True:
			return
		self.extrudeWing (self.sel, wing, solid)
		FreeCAD.Console.PrintMessage("new wing just ready to fly!" + "\n")
		return

	def pathForPipe(self, List):
		points=[]
		for i in List:
			points.append(i.Placement.Base) #polyline on all origins for airfoils
		wire = Draft.makeWire(points)
		return wire
	
	def extrudeWing(self, selected, wing, solid):
		wire = self.pathForPipe(self.sel)
		
		FreeCAD.ActiveDocument.addObject("PartDesign::Body", wing)
		for i in selected:
			FreeCAD.ActiveDocument.getObject(wing).ViewObject.dropObject(FreeCAD.ActiveDocument.getObject(i.Label),None,'',[]) #ass3Environment
			#FreeCAD.ActiveDocument.getObject(wing).addObject(FreeCAD.ActiveDocument.getObject(i.Label))
		FreeCAD.ActiveDocument.getObject(wing).ViewObject.dropObject(FreeCAD.ActiveDocument.getObject(wire.Label),None,'',[]) #ass3Environment
		#FreeCAD.ActiveDocument.getObject(wing).addObject(FreeCAD.ActiveDocument.getObject(wire.Label))

		FreeCAD.ActiveDocument.getObject(wing).newObject('PartDesign::AdditivePipe',solid)
		FreeCAD.ActiveDocument.getObject(solid).Profile 		= FreeCAD.ActiveDocument.getObject(selected[0].Label)
		FreeCAD.ActiveDocument.getObject(solid).Spine			= FreeCAD.ActiveDocument.getObject(wire.Label)
		FreeCAD.ActiveDocument.getObject(solid).Transformation 	= u"Multisection"
		FreeCAD.ActiveDocument.getObject(solid).Mode 			= u"Fixed"
		FreeCAD.ActiveDocument.getObject(solid).Sections		= selected[1:]
		FreeCAD.ActiveDocument.getObject(solid).Refine 			= True
		FreeCAD.ActiveDocument.getObject(solid).Label2 			= "additivePipe"
		#FreeCAD.ActiveDocument.getObject(solid).Label 			= "additivePipe"
		FreeCAD.ActiveDocument.recompute()
		return

	def checkPositioning(self):
		auxFunctions.bubbleSort(self.sel)
		check = self.sel[0].Placement.Base.z
		for i in self.sel[1:]:
			if i.Placement.Base.z == check:
				errorMessage.errors("buildError1")
				return False
			check = i.Placement.Base.z		
		return True		

	def IsActive(self):
			"""Here you can define if the command must be active or not (greyed) if certain conditions
			are met or not. This function is optional."""
			return True

Gui.addCommand('wingExtruderPipe', wingExtruderPipe())

class wingExtruderLoft(wingExtruderPipe):	
	
	def GetResources(self):
		os.environ["USER"]
		return {'Pixmap'  : os.path.expandvars("/home/$USER") + ("/.FreeCAD/Mod/airFoil_tools/Resources/icons/airFoilSketcher.png"), # the name of a svg file available in the resources
			'Accel' : "Shift+S",
			'MenuText': "wingExtruderLoft",
			'ToolTip' : "wingExtruderLoft: Generates solid feature and body using loft PartDesign Feature"}


	def extrudeWing(self, selected, wing, solid):
		FreeCAD.ActiveDocument.addObject("PartDesign::Body", wing)
		for i in selected:
			FreeCAD.ActiveDocument.getObject(wing).ViewObject.dropObject(FreeCAD.ActiveDocument.getObject(i.Label),None,'',[])
			#FreeCAD.ActiveDocument.getObject(wing).addObject(FreeCAD.ActiveDocument.getObject(i.Label))	
		FreeCAD.ActiveDocument.getObject(wing).newObject('PartDesign::AdditiveLoft',solid)
		FreeCAD.ActiveDocument.getObject(solid).Profile 	= FreeCAD.ActiveDocument.getObject(selected[0].Label)
		FreeCAD.ActiveDocument.getObject(solid).Sections	= selected[1:]
		FreeCAD.ActiveDocument.getObject(solid).Ruled 		= True
		FreeCAD.ActiveDocument.getObject(solid).Closed 		= True
		FreeCAD.ActiveDocument.getObject(solid).Refine 		= True
		FreeCAD.ActiveDocument.getObject(solid).Label2 		= "loft"
		#FreeCAD.ActiveDocument.getObject(solid).Label 		= "loft"
		FreeCAD.ActiveDocument.recompute()
		return



Gui.addCommand('wingExtruderLoft', wingExtruderLoft())

#----------------------------------------------------------------------------------------------------------------------------------------
#static methods
#----------------------------------------------------------------------------------------------------------------------------------------

def airFoilSketcher(element,name):

	form1 = PopUpMenu.PopUpNACA4()
	form1.exec_()
	
	m				=	int(form1.numericInput1.text())
	p				= 	int(form1.numericInput2.text())
	TH 				=	int(form1.numericInput3.text())
	chord			=	float(form1.numericInput4.text())
	resolution 		= 	int(form1.numericInput5.text())
	xOffSet			=	float(form1.numericInput6.text())
	zOffSet			=	float(form1.numericInput7.text())

#	if form1.interpolation == userLinear:
#		interpolation = 0
#	else:
	interpolation = 1
	
	foil = NACA4_Generator.NACA4_Generator(m,p,TH,chord,resolution,interpolation)

	if form1.result == userPlot:
		auxFunctions.airFoilPlot(foil)
		return airFoilSketcher(element, name)

	if form1.result==userCancelled:
		pass

	if form1.result==userApplied:
		next = auxFunctions.sketchOnPlane(foil, element, name,xOffSet, zOffSet)
		wing = airFoil2D()
		return wing.Activated(next)

	if form1.result==userOK:
		next = auxFunctions.sketchOnPlane(foil, element, name,xOffSet, zOffSet)
		pass

#-----------------------------------------------------------------

userLinear		= 0
userCosine		= 1
userPlot        = "Plotted"
userCancelled	= "Cancelled"
userApplied     = "Applied"
userOK			= "OK"






