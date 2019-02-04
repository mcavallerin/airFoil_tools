import FreeCAD, FreeCADGui
from FreeCAD import Gui
import Part, math, Draft, os
from FreeCAD import Base



def counter(nameSize,Number,objs = []):

	#obj = FreeCAD.ActiveDocument.Objects
	size = len(objs) #number of elements on tree of features
	for j in range(size):
		for i in objs:
			try:
				if int(i.Name[nameSize:]) == Number: #i.Name is a unique read-only property of FreeCAD, if number of element already given, number+1
					Number +=1
			except:
				continue
	return Number

def bubbleSort(alist):
	for passnum in range(len(alist)-1,0,-1):
		for i in range(passnum):
			if alist[i].Placement.Base.z>alist[i+1].Placement.Base.z:
				temp = alist[i]
				alist[i] = alist[i+1]
				alist[i+1] = temp
