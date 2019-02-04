import FreeCAD, FreeCADGui
from FreeCAD import Gui
import Part, math, Draft, os
from FreeCAD import Base
from PySide import QtGui, QtCore
import auxFunctions, errorMessage

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
		auxFunctions.bubbleSort(List)
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
			'ToolTip' : "Allows you to replace foil section on existing solid wing by selecting external sketch \n1.Make a selection of two sketches: first is the new one, second is inside a 3d Feature\n2.Activate the command"}

	def Activated(self):#, sel=[]):
		sel = FreeCADGui.Selection.getSelection()
		if len(sel)<3 or len(sel)>3:
			QtGui.QMessageBox.information(
				QtGui.QApplication.activeWindow(),
				"Selection error",
				"You have to select:\n1.Feature(wing)\n2.SketchToBeReplaced\n3.New Sketch"
				)
			return	
		index = 1		
		for i in sel[0].Sections:
			if i==sel[1]:
				index = sel[0].Sections.index(i)
				print (index)
				List = sel[0].Sections
				List.pop(index)
				List.insert(index,sel[2])
				sel[0].Sections = List

		FreeCAD.Console.PrintMessage("Foil replaced" + "\n")
		return

	def IsActive(self):
			"""Here you can define if the command must be active or not (greyed) if certain conditions
			are met or not. This function is optional."""
			return True

Gui.addCommand('replaceFoil', replaceFoil())



