import FreeCAD, FreeCADGui
from FreeCAD import Gui
import Part, math, Draft, os
from FreeCAD import Base
import PopUpMenu, NACA4_Generator
from PySide import QtGui, QtCore


class insertFoil():	
	
	def GetResources(self):
		os.environ["USER"]
		return {'Pixmap'  : os.path.expandvars("/home/$USER") + ("/.FreeCAD/Mod/airFoil_tools/Resources/icons/_airFoilShaper.png"), # the name of a svg file available in the resources
			'Accel' : "Shift+S",
			'MenuText': "insertFoil",
			'ToolTip' : "Allows you to add foil section on existing solid wing \n it sorts the foils according to Z axis\n1. Select the 3D feature \n2. Select foils to be added \n 3. For additive pipe select Line"}

	def Activated(self):#, sel=[]):
		sel = FreeCADGui.Selection.getSelection()
		List = sel[1:-1]
		exList = sel[0].Sections
		List.extend(exList)
		staticmethod(bubbleSort(List))
		sel[0].Sections = List
		try:
			sel[-1].End=(sel[-2].Placement.Base.x,sel[-2].Placement.Base.y,sel[-2].Placement.Base.z)
		except:
			pass

		FreeCAD.Console.PrintMessage("new section added on wing" + "\n")
		return

	def IsActive(self):
			"""Here you can define if the command must be active or not (greyed) if certain conditions
			are met or not. This function is optional."""
			return True

Gui.addCommand('insertFoil', insertFoil())


class replaceFoil():	
	
	def GetResources(self):
		os.environ["USER"]
		return {'Pixmap'  : os.path.expandvars("/home/$USER") + ("/.FreeCAD/Mod/airFoil_tools/Resources/icons/_airFoilShaper.png"), # the name of a svg file available in the resources
			'Accel' : "Shift+S",
			'MenuText': "insertFoil",
			'ToolTip' : "Allows you to replace foil section on existing solid wing"}

	def Activated(self):#, sel=[]):

		selN = FreeCADGui.Selection.getObject().Name
		selF = FreeCADGui.Selection.getObject().Label2
		
		element = selN[10:]
		name	= selN[-1]
		
		m			= int(selF[0])
		p			= int(selF[1])
		TH			= int(selF[2:4])
		chord 		= float(selF[5:10])
		resolution 	= float(selF[11:])

		

		FreeCAD.Console.PrintMessage("Foil reaplced" + "\n")
		return

	def IsActive(self):
			"""Here you can define if the command must be active or not (greyed) if certain conditions
			are met or not. This function is optional."""
			return True

Gui.addCommand('insertFoil', insertFoil())

def bubbleSort(alist):
	for passnum in range(len(alist)-1,0,-1):
		for i in range(passnum):
			if alist[i].Placement.Base.z>alist[i+1].Placement.Base.z:
				temp = alist[i]
				alist[i] = alist[i+1]
				alist[i+1] = temp



