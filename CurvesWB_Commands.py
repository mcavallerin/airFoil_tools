# author m.cavallerin 2019

import FreeCAD, FreeCADGui
from FreeCAD import Gui
import Part, math, Draft, os
from FreeCAD import Base
import PopUpMenu, NACA4_Generator
from PySide import QtGui, QtCore
import auxFunctions, errorMessage


class airFoilRails2D():	#part Design method
	
	def GetResources(self):
		os.environ["USER"]
		return {'Pixmap'  : os.path.expandvars("/home/$USER") + ("/.FreeCAD/Mod/airFoil_tools/Resources/icons/airFoilShaper.png"), # the name of a svg file available in the resources
			'Accel' : "Shift+S",
			'MenuText': "airFoilRails2D",
			'ToolTip' : "Create new sections for airFoil on sketches; actually only NACA4 digit is supported"}

	def Activated(self, element = 0, name = 'foilSketch'):
		self.element = element
		self.name = name
		N = len(self.name)
		if FreeCAD.activeDocument() == None:
			errorMessage.errors("noFileOpen")
			return

		obj = FreeCAD.ActiveDocument.Objects
		self.element = auxFunctions.counter(N,self.element,obj) #renumbering function in order to have unique name for objects
		staticmethod(airFoilRailsSketcher(self.element, self.name))
		FreeCAD.Console.PrintMessage("new section for wing" + "\n")
		return

	def IsActive(self):
			"""Here you can define if the command must be active or not (greyed) if certain conditions
			are met or not. This function is optional."""
			return True

Gui.addCommand('airFoilRails2D', airFoilRails2D())


#----------------------------------------------------------------------------------------------------------------------------------------
#static methods
#----------------------------------------------------------------------------------------------------------------------------------------

def airFoilRailsSketcher(element,name):

	form1 = PopUpMenu.PopUpNACA4()
	form1.exec_()
	
	m				=	int(form1.numericInput1.text())
	p				= 	int(form1.numericInput2.text())
	TH 				=	int(form1.numericInput3.text())
	chord			=	float(form1.numericInput4.text())
	resolution 		= 	int(form1.numericInput5.text())
	xOffSet			=	float(form1.numericInput6.text())
	zOffSet			=	float(form1.numericInput7.text())

	if form1.interpolation == userLinear:
		interpolation = 0
	else:
		interpolation = 1
	
	foil = NACA4_Generator.NACA4_Generator(m,p,TH,chord,resolution,interpolation)

	if form1.result == userPlot:
		auxFunctions.airFoilPlot(foil)
		return airFoilRailsSketcher(element, name)

	if form1.result==userCancelled:
		pass

	if form1.result==userApplied:
		next = auxFunctions.sketchOnRails(foil, element, name,xOffSet, zOffSet)
		wing = airFoilRails2D()
		return wing.Activated(next)

	if form1.result==userOK:
		next = auxFunctions.sketchOnRails(foil, element, name,xOffSet, zOffSet)
		pass

#-----------------------------------------------------------------

userLinear		= 0
userCosine		= 1
userPlot        = "Plotted"
userCancelled	= "Cancelled"
userApplied     = "Applied"
userOK = "OK"
