import FreeCAD, FreeCADGui
from FreeCAD import Gui
import Part, math, Draft, os
from FreeCAD import Base
import PopUpMenu, NACA4_Generator
from PySide import QtGui, QtCore


class airFoil2D():	#part Design method
	
	def GetResources(self):
		os.environ["USER"]
		return {'Pixmap'  : os.path.expandvars("/home/$USER") + ("/.FreeCAD/Mod/airFoil_tools/Resources/icons/airFoilShaper.png"), # the name of a svg file available in the resources
			'Accel' : "Shift+S",
			'MenuText': "airFoil2D",
			'ToolTip' : "Create new sections for airFoil on sketches; actually only NACA4 digit is supported"}

	def Activated(self, element = 0, name ='foilSketch'):
		self.element = element
		self.name = name

		N = len(self.name)
		if FreeCAD.activeDocument() == None:
			QtGui.QMessageBox.information(
				QtGui.QApplication.activeWindow(),
				"No active Document error",
				"First create a new a file!"
				)
			return

		obj = FreeCAD.ActiveDocument.Objects
		size = len(obj)
		for j in range(size):
			for i in obj:
				try:
					if int(i.Name[N:]) == self.element:
						self.element +=1
				except:
					continue
#		staticmethod(counter(N, self.element))

		staticmethod(airFoilSketcher(self.element, self.name))
		FreeCAD.Console.PrintMessage("new section for wing" + "\n")
		return

	def IsActive(self):
			"""Here you can define if the command must be active or not (greyed) if certain conditions
			are met or not. This function is optional."""
			return True

Gui.addCommand('airFoil2D', airFoil2D())

class wingExtruderPipe():	#part Design method
	
	def GetResources(self):
		os.environ["USER"]
		return {'Pixmap'  : os.path.expandvars("/home/$USER") + ("/.FreeCAD/Mod/airFoil_tools/Resources/icons/airFoilSketcher.png"), # the name of a svg file available in the resources
			'Accel' : "Shift+S",
			'MenuText': "wingExtruderPipe",
			'ToolTip' : "Generates solid feature and body using additive pipe PartDesign Feature"}

	def Activated(self, sel = [], element = 0, name ='foilWing'):
		self.sel = FreeCADGui.Selection.getSelection()
		self.name = name
		self.element = element
		
		N = len(self.name)

		obj = FreeCAD.ActiveDocument.Objects
		size = len(obj)
		for j in range(size):
			for i in obj:
				try:
					if int(i.Name[N:]) == self.element:
						self.element +=1
				except:
					continue

		if FreeCAD.activeDocument() == None:
			QtGui.QMessageBox.information(
				QtGui.QApplication.activeWindow(),
				"No active Document error",
				"First create a new a file!"
				)
			return
		
		if len(self.sel) == 0 or len(self.sel) <2:
			QtGui.QMessageBox.information(
				QtGui.QApplication.activeWindow(),
				"Inconsistent number of foil",
				"At least two sketchs have to be selected"
				)
			return

		points=[]
		check = -999999.
		for i in self.sel:
			if i.Placement.Base.z == check or i.Placement.Base.z < check:
				QtGui.QMessageBox.information(
					QtGui.QApplication.activeWindow(),
					"Section for foil error",
					"Sections could have same Placement, please adjust before to fly"
					)
				return				
#			points.append(i.Placement.Base) #polyline on all origins for airfoils
			check = i.Placement.Base.z
		points.append(self.sel[0].Placement.Base)
		points.append(self.sel[-1].Placement.Base)


		wing = self.name + str(self.element)
		solid = "solid" + str(self.element)

#		staticmethod(pipeWing(self.sel,points, wing, solid))
		self.extrudeWing (self.sel,points, wing, solid)

		FreeCAD.Console.PrintMessage("new wing just ready to fly!" + "\n")
		return

	def extrudeWing(self, selected, points, wing, solid):
		FreeCAD.ActiveDocument.addObject("PartDesign::Body", wing)
		for i in selected:
			FreeCAD.ActiveDocument.getObject(wing).ViewObject.dropObject(FreeCAD.ActiveDocument.getObject(i.Label),None,'',[])	
		line = Draft.makeWire(points)
		FreeCAD.ActiveDocument.getObject(wing).ViewObject.dropObject(FreeCAD.ActiveDocument.getObject(line.Label),None,'',[])
		FreeCAD.ActiveDocument.getObject(wing).newObject('PartDesign::AdditivePipe',solid)

		FreeCAD.ActiveDocument.getObject(solid).Profile 		= FreeCAD.ActiveDocument.getObject(selected[0].Label)
		FreeCAD.ActiveDocument.getObject(solid).Spine			= FreeCAD.ActiveDocument.getObject(line.Label)
		FreeCAD.ActiveDocument.getObject(solid).Transformation 	= u"Multisection"
		FreeCAD.ActiveDocument.getObject(solid).Mode 			= u"Fixed"
		FreeCAD.ActiveDocument.getObject(solid).Sections		= selected[1:]
		FreeCAD.ActiveDocument.getObject(solid).Refine 			= True
		FreeCAD.ActiveDocument.getObject(solid).Label2 			= "additivePipe"
		FreeCAD.ActiveDocument.recompute()
		return


	def IsActive(self):
			"""Here you can define if the command must be active or not (greyed) if certain conditions
			are met or not. This function is optional."""
			return True

Gui.addCommand('wingExtruderPipe', wingExtruderPipe())

class wingExtruderLoft(wingExtruderPipe):	#part Design method
	
	def GetResources(self):
		os.environ["USER"]
		return {'Pixmap'  : os.path.expandvars("/home/$USER") + ("/.FreeCAD/Mod/airFoil_tools/Resources/icons/airFoilSketcher.png"), # the name of a svg file available in the resources
			'Accel' : "Shift+S",
			'MenuText': "wingExtruderLoft",
			'ToolTip' : "Generates solid feature and body using loft PartDesign Feature"}


	def extrudeWing(self, selected, points, wing, solid):
		FreeCAD.ActiveDocument.addObject("PartDesign::Body", wing)
		for i in selected:
			FreeCAD.ActiveDocument.getObject(wing).ViewObject.dropObject(FreeCAD.ActiveDocument.getObject(i.Label),None,'',[])	
		FreeCAD.ActiveDocument.getObject(wing).newObject('PartDesign::AdditiveLoft',solid)
		FreeCAD.ActiveDocument.getObject(solid).Profile 	= FreeCAD.ActiveDocument.getObject(selected[0].Label)
		FreeCAD.ActiveDocument.getObject(solid).Sections	= selected[1:]
		FreeCAD.ActiveDocument.getObject(solid).Ruled 		= True
		FreeCAD.ActiveDocument.getObject(solid).Closed 		= True
		FreeCAD.ActiveDocument.getObject(solid).Refine 		= True
		FreeCAD.ActiveDocument.getObject(solid).Label2 		= "loft"
		FreeCAD.ActiveDocument.recompute()
		return



Gui.addCommand('wingExtruderLoft', wingExtruderLoft())









#----------------------------------------------------------------------------------------------------------------------------------------
#static methods
#----------------------------------------------------------------------------------------------------------------------------------------

def airFoilSketcher(element,name):

	form1 = PopUpMenu.PopUpNACA4()
	form1.exec_()
	
	m			=	int(form1.numericInput1.text())
	p			= 	int(form1.numericInput2.text())
	TH 			=	int(form1.numericInput3.text())
	chord			=	float(form1.numericInput4.text())
	resolution 		= 	int(form1.numericInput5.text())
	if form1.interpolation == userLinear:
		interpolation = 0
	else:
		interpolation = 1

	foil = NACA4_Generator.NACA4_Generator(m,p,TH,chord,resolution,interpolation)
	
	zOffSet			=	float(form1.numericInput7.text())

	if form1.result == userPlot:
		NACA4_Generator.airFoilPlot(foil)
		return airFoilSketcher(element, name)

	if form1.result==userCancelled:
		pass

	if form1.result==userApplied:
		next = NACA4_Generator.sketchOnPlane(foil, element, name, zOffSet)
		wing = airFoil2D()
		return wing.Activated(next)
		

	if form1.result==userOK:
		next = NACA4_Generator.sketchOnPlane(foil, element, name, zOffSet)
		pass

#def counter(nameSize,Number):
#
#	obj = FreeCAD.ActiveDocument.Objects
#	size = len(obj) #number of elements on tree of features
#	for j in range(size):
#		for i in obj:
#			try:
#				if int(i.Name[nameSize:]) == Number: #i.Name is a unique read-only property of FreeCAD, if number of element already given, number+1
#					Number +=1
#			except:
#				continue
#	return Number

#-----------------------------------------------------------------

userLinear		= 0
userCosine		= 1
userPlot        = "Plotted"
userCancelled	= "Cancelled"
userApplied     = "Applied"
userOK			= "OK"






