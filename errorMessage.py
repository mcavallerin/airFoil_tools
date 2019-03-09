# author m.cavallerin 2019

from PySide import QtGui, QtCore

def errors(a):
#file errors
	if a == "noFileOpen":
		QtGui.QMessageBox.information(
			QtGui.QApplication.activeWindow(),
			"No File Open",
			"First create a new a file, or open an existing one"
			)
#Selection errors
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
			"Please select at least two sketches"
			)
	if a == "wrongSelection4":
		QtGui.QMessageBox.information(
			QtGui.QApplication.activeWindow(),
			"Different foils",
			"Please select two foils both with High or Low Label3 property"
			)
#3D Feature errors
	if a == "buildError1":
		QtGui.QMessageBox.information(
			QtGui.QApplication.activeWindow(),
			"Build Error",
			"Sections could have same placement"
			)
