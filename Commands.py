import FreeCAD, FreeCADGui
from FreeCAD import Gui
import Part, math, Draft, os
from FreeCAD import Base
import PopUpMenu, NACA4_Generator
import matplotlib.pyplot as plt
from PySide import QtGui, QtCore


class airFoil2D():
	""" """
	def GetResources(self):
		os.environ["USER"]
		return {'Pixmap'  : os.path.expandvars("/home/$USER") + ("/.FreeCAD/Mod/airFoil_tools/Resources/icons/airFoilShaper.png"), # the name of a svg file available in the resources
			'Accel' : "Shift+S",
			'MenuText': "My New Command",
			'ToolTip' : "Create new sections for wing"}

	def Activated(self):
		if FreeCAD.activeDocument() == None:
			QtGui.QMessageBox.information(
				QtGui.QApplication.activeWindow(),
				"No active Document error",
				"First create a new a file!"
				)
			return
		staticmethod(airFoilBuilder())
		FreeCAD.Console.PrintMessage("new section for wing" + "\n")
		return

	def IsActive(self):
			"""Here you can define if the command must be active or not (greyed) if certain conditions
			are met or not. This function is optional."""
			return True

Gui.addCommand('airFoil_2D', airFoil2D())

class airFoil2DPD():
	""" """
	def GetResources(self):
		os.environ["USER"]
		return {'Pixmap'  : os.path.expandvars("/home/$USER") + ("/.FreeCAD/Mod/airFoil_tools/Resources/icons/airFoilShaper.png"), # the name of a svg file available in the resources
			'Accel' : "Shift+S",
			'MenuText': "My New Command",
			'ToolTip' : "Create new sections for wing"}

	def Activated(self, element = 0):
		self.element = element
		if FreeCAD.activeDocument() == None:
			QtGui.QMessageBox.information(
				QtGui.QApplication.activeWindow(),
				"No active Document error",
				"First create a new a file!"
				)
			return
		staticmethod(airFoilSketcher(self.element))
		FreeCAD.Console.PrintMessage("new section for wing" + "\n")
		return

	def IsActive(self):
			"""Here you can define if the command must be active or not (greyed) if certain conditions
			are met or not. This function is optional."""
			return True

Gui.addCommand('airFoil2D_PD', airFoil2DPD())


def airFoilBuilder():

	form1 = PopUpMenu.PopUpNACA4()
	form1.exec_()
	
	m				=	int(form1.numericInput1.text())
	p				= 	int(form1.numericInput2.text())
	TH 				=	int(form1.numericInput3.text())
	chord			=	float(form1.numericInput4.text())
	resolution 		= 	int(form1.numericInput5.text())
	if form1.interpolation == userLinear:
		interpolation = 0
	else:
		interpolation = 1

	foil = NACA4_Generator.NACA4_Generator(m,p,TH,chord,resolution,interpolation)
	
	if form1.result == userPlot:
		NACA4_Generator.airFoilPlot(foil)
		return airFoilBuilder()

	if form1.result==userCancelled:
		pass

	if form1.result==userApplied:
		NACA4_Generator.drawAirFoil(foil)
		airFoilBuilder()

	if form1.result==userOK:
		NACA4_Generator.drawAirFoil(foil)

def airFoilSketcher(element):

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
		return airFoilSketcher(element)

	if form1.result==userCancelled:
		pass

	if form1.result==userApplied:
		next = NACA4_Generator.sketchOnPlane(foil, element,zOffSet)
		wing = airFoil2DPD()
		return wing.Activated(next)

	if form1.result==userOK:
		next = NACA4_Generator.sketchOnPlane(foil, element, zOffSet)
		pass

userLinear	= 0
userCosine	= 1
userPlot        = "Plotted"
userCancelled	= "Cancelled"
userApplied     = "Applied"
userOK		= "OK"






