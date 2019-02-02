# Part gui init module
# (c) 2003 Juergen Riegel
#
# Gathering all the information to start FreeCAD
# This is the second one of three init scripts, the third one
# runs when the gui is up

class airFoil_toolsWorkbench ( Workbench ):
	"Part workbench object"
	def __init__(self):

		import os

		os.environ["USER"]
		self.__class__.Icon = os.path.expandvars("/home/$USER") + "/.FreeCAD/Mod/airFoil_tools/Resources/icons/WorkBench.png"    
		self.__class__.MenuText = "airFoil_tools"
		self.__class__.ToolTip = "workbench for airFoils"

	def Initialize(self):
		"This function is executed when FreeCAD starts"
		import Commands # import here all the needed files that create your FreeCAD commands

		foilDef_Gen = [
			'airFoil_2D',
			'wingModeller_3D'
			]
		self.appendToolbar(
			'Foil Generators',
			foilDef_Gen
			)
	
		commandslist = list()
		commandslist.extend(foilDef_Gen)
	
		self.appendMenu(
			'airFoilTools',
			commandslist
			)

	def Activated(self):
		"This function is executed when the workbench is activated"
		return

	def Deactivated(self):
		"This function is executed when the workbench is deactivated"
		return

	def ContextMenu(self, recipient):
		"This is executed whenever the user right-clicks on screen"
		# "recipient" will be either "view" or "tree"
		self.appendContextMenu("My commands",self.list) # add commands to the context menu

	def GetClassName(self): 
		# this function is mandatory if this is a full python workbench
		return "Gui::PythonWorkbench"

Gui.addWorkbench(airFoil_toolsWorkbench())
