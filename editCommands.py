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
			'ToolTip' : "Allows you to add foil section on existing solid wing \n it sirts the foil according to Z axis"}

	def Activated(self, sel=[]):
		self.sel = FreeCADGui.Selection.getSelection()
		List = self.sel[1:]
		exList = self.sel[0].Sections
		List.extend(exList)
		bridge = []
		for i in List:
			bridge.append((i.Name,i.Placement.Base.z))	
		self.sel[0].Sections = List


		FreeCAD.Console.PrintMessage("new section added on wing" + "\n")
		return

	def IsActive(self):
			"""Here you can define if the command must be active or not (greyed) if certain conditions
			are met or not. This function is optional."""
			return True

Gui.addCommand('insertFoil', insertFoil())



#		if self.sel[0] != <PartDesign::AdditivePipe>:
#			QtGui.QMessageBox.information(
#				QtGui.QApplication.activeWindow(),
#				"Selection error",
#				"Select solidX before sketches"
#				)
#			return

