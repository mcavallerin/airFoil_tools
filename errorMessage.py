# author m.cavallerin 2019

from PySide import QtGui, QtCore

def errors(a):
	
	if a == "noFileOpen":
		QtGui.QMessageBox.information(
			QtGui.QApplication.activeWindow(),
			"No File Open",
			"First create a new a file, or open an existing one"
			)

	if a == "wrongSelection1":
		QtGui.QMessageBox.information(
			QtGui.QApplication.activeWindow(),
			"Wrong Selection",
			"At least two sketches have to be selected"
			)

	if a == "wrongSelection2":
		QtGui.QMessageBox.information(
			QtGui.QApplication.activeWindow(),
			"Wrong Selection",
			"You haven't selected the right features"
			)

	if a == "wrongSelection3":
		QtGui.QMessageBox.information(
			QtGui.QApplication.activeWindow(),
			"List is empty",
			"Please Select at Least two sketches"
			)

	if a == "buildError1":
		QtGui.QMessageBox.information(
			QtGui.QApplication.activeWindow(),
			"Build Error",
			"Sections could have same placement"
			)
