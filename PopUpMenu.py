# author m.cavallerin 2019
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import statements

from PySide import QtGui, QtCore


# UI Class definitions

class PopUpNACA4(QtGui.QDialog):
	""""""
	def __init__(self):
		super(PopUpNACA4, self).__init__()
		self.initUI()

	def initUI(self, menu =""):
		self.result = "Cancelled"
		self.interpolation = 0
		self.menu = menu
		# create our window
		# define window		xLoc,yLoc,xDim,yDim
		self.setGeometry(	250, 250, 600, 410)
		self.setWindowTitle("Define NACA4 data (XXXX): ")
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
	
		# create some Labels
		self.label1 = QtGui.QLabel("Define maximum chamber [X...]", self)
		self.label1.move(20, 20)
		self.label2 = QtGui.QLabel('location of max chamber [.X..]', self)
		self.label2.move(20, 70)
		self.label3 = QtGui.QLabel('define thickness [.XX]', self) #max thickness
		self.label3.move(20, 120)
		self.label4 = QtGui.QLabel('chord lenght [mm]', self)
		self.label4.move(20, 170)
		self.label5 = QtGui.QLabel('resolution [pts]', self)
		self.label5.move(20, 210)
		self.label6 = QtGui.QLabel("leading edge starting point [mm] ", self)
		self.label6.move(20, 250)
		self.label7 = QtGui.QLabel('profile plane offset [mm] ', self)
		self.label7.move(20, 290)

		# radio buttons
		self.radioButton1 = QtGui.QRadioButton("linear spacing",self)
		self.radioButton1.clicked.connect(self.onRadioButton1)
		self.radioButton1.move(370,70)

		self.radioButton2 = QtGui.QRadioButton("cosine spacing",self)
		self.radioButton2.clicked.connect(self.onRadioButton2)
		self.radioButton2.toggle()
		self.radioButton2.move(370,120)

		# numeric input field
		self.numericInput1 = QtGui.QLineEdit(self)
		self.numericInput1.setInputMask("9")
		self.numericInput1.setText("4")
		self.numericInput1.setFixedWidth(50)
		self.numericInput1.move(210, 20)

		self.numericInput2 = QtGui.QLineEdit(self)
		self.numericInput2.setInputMask("9")
		self.numericInput2.setText("4")
		self.numericInput2.setFixedWidth(50)
		self.numericInput2.move(210, 70)

		self.numericInput3 = QtGui.QLineEdit(self)
		self.numericInput3.setInputMask("99")
		self.numericInput3.setText("15")
		self.numericInput3.setFixedWidth(50)
		self.numericInput3.move(210, 120)

		self.numericInput4 = QtGui.QLineEdit(self)
		self.numericInput4.setInputMask("#xxxxxx")
		self.numericInput4.setText("100")
		self.numericInput4.setFixedWidth(100)
		self.numericInput4.move(210, 170)

		self.numericInput5 = QtGui.QLineEdit(self)
		self.numericInput5.setInputMask("999")
		self.numericInput5.setText("100")
		self.numericInput5.setFixedWidth(100)
		self.numericInput5.move(210, 210)

		self.numericInput6 = QtGui.QLineEdit(self)
		self.numericInput6.setInputMask("#xxxxxxxxx")
		self.numericInput6.setText("0")
		self.numericInput6.setFixedWidth(100)
		self.numericInput6.move(210, 250)

		self.numericInput7 = QtGui.QLineEdit(self)
		self.numericInput7.setInputMask("#xxxxxxxxx")
		self.numericInput7.setText("0")
		self.numericInput7.setFixedWidth(100)
		self.numericInput7.move(210, 290)

		# cancel button
		cancelButton = QtGui.QPushButton('Cancel', self)
		cancelButton.clicked.connect(self.onCancel)
		cancelButton.setAutoDefault(True)
		cancelButton.move(150, 370)
		# applyButton button
		applyButton = QtGui.QPushButton('Apply', self)
		applyButton.clicked.connect(self.onApply)
		applyButton.move(260, 370)
		# OK button
		okButton = QtGui.QPushButton('OK', self)
		okButton.clicked.connect(self.onOk)
		okButton.move(370, 370)
		# plot button
		plotButton = QtGui.QPushButton('Plot', self)
		plotButton.clicked.connect(self.onPlot)
		plotButton.setAutoDefault(True)
		plotButton.move(370,20)
		# now make the window visible
		self.show()
		#

	def onRadioButton1(self):
		self.interpolation = 0
		pass
	def onRadioButton2(self):
		self.interpolation = 1
		pass

	def onCancel(self):
		self.result			= "Cancelled"
		self.close()
	def onApply(self):
		self.result			= "Applied"
		self.close()
	def onOk(self):
		self.result			= "OK"
		self.close()
	def onPlot(self):
		self.result			= "Plotted"
		self.close()


