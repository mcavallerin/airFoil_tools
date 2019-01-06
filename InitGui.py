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
		self.__class__.ToolTip = "workbench per generare profili NACA"

	def Initialize(self):
		"This function is executed when FreeCAD starts"
		import Commands # import here all the needed files that create your FreeCAD commands
		self.list = ["airFoil_Shaper", "Wing_Creation"] # A list of command names created in the line above
		self.appendToolbar("My Commands", self.list) # creates a new toolbar with your commands
		#self.appendMenu("Il menu dei nastri", self.list) # creates a new menu
		#self.appendMenu(["An existing Menu","My submenu"],self.list) # appends a submenu to an existing menu 


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
