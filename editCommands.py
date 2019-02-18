# author m.cavallerin 2019

import FreeCAD, FreeCADGui
from FreeCAD import Gui
import Part, math, Draft, os
from FreeCAD import Base
from PySide import QtGui, QtCore
import auxFunctions, errorMessage, Commands

class insertFoil():	
	
	def GetResources(self):
		os.environ["USER"]
		return {'Pixmap'  : os.path.expandvars("/home/$USER") + ("/.FreeCAD/Mod/airFoil_tools/Resources/icons/_airFoilShaper.png"), # the name of a svg file available in the resources
			'Accel' : "Shift+S",
			'MenuText': "insertFoil",
			'ToolTip' : "Allows you to add foil section on existing solid wing \n it sorts the foils according to Z axis\n1. Select the 3D feature \n2. Select foils to be added \n3.If additive Pipe select also the wire"}

	def Activated(self):
		try:		
			sel = FreeCADGui.Selection.getSelection() 
			if sel[0].Label2 == 'additivePipe':
				List = sel[1:-1]
			if sel[0].Label2 == 'loft':
				List = sel[1:]
			exList = sel[0].Sections
			List.extend(exList)
			auxFunctions.bubbleSort(List)
			sel[0].Sections = List #Multisection list updated
			a = sel[0].Sections
			a.insert(0,sel[0].Profile[0]) #list of sketches needed to define the points for wire
			if sel[0].Label2 == 'additivePipe':
				sel[0].Spine = (Commands.wingExtruderPipe().pathForPipe(a),[])
		except:
			errorMessage.errors('wrongSelection2')

		FreeCAD.ActiveDocument.recompute()
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
			'ToolTip' : "Allows you to replace one-by-one foil section on existing solid wing by selecting external sketch, but not the starting Profile\n1.Feature(wing)\n2.SketchToBeReplaced\n3.New Sketch"}

	def Activated(self):
		try:
			sel = FreeCADGui.Selection.getSelection()
			index = 1		
			for i in sel[0].Sections:
				if i==sel[1]:
					index = sel[0].Sections.index(i)
					List = sel[0].Sections
					List.pop(index)
					List.insert(index,sel[2])
					sel[0].Sections = List
				#else:
				#	sel[0].Profile = i

			if sel[0].Label2 == 'additivePipe':
			#if sel[0].Label == 'additivePipe':
				a = sel[0].Sections
				a.insert(0,sel[0].Profile[0]) #list of sketches needed to define the points for wire
				sel[0].Spine = (Commands.wingExtruderPipe().pathForPipe(a),[])

		except:
			errorMessage.errors('wrongSelection2')

		FreeCAD.ActiveDocument.recompute()
		return

	def IsActive(self):
			"""Here you can define if the command must be active or not (greyed) if certain conditions
			are met or not. This function is optional."""
			return True

Gui.addCommand('replaceFoil', replaceFoil())

class replaceProfile():	
	
	def GetResources(self):
		os.environ["USER"]
		return {'Pixmap'  : os.path.expandvars("/home/$USER") + ("/.FreeCAD/Mod/airFoil_tools/Resources/icons/_airFoilShaper.png"), # the name of a svg file available in the resources
			'Accel' : "Shift+S",
			'MenuText': "insertFoil",
			'ToolTip' : "Allows you to replace the Profile Sketch of the feature, both Loft and additive Pipe\n1. Select Feature(wing)\n2. select New Sketch"}

	def Activated(self):
		try:
			sel = FreeCADGui.Selection.getSelection()
			sel[0].Profile = sel[1]

		except:
			errorMessage.errors('wrongSelection2')

		FreeCAD.ActiveDocument.recompute()
		return

	def IsActive(self):
			"""Here you can define if the command must be active or not (greyed) if certain conditions
			are met or not. This function is optional."""
			return True

Gui.addCommand('replaceProfile', replaceProfile())
