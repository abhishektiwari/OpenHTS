# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/abhishek/Coding/openhts/src/addedithtsdlg.ui'
#
# Created: Mon Mar 29 00:36:03 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AddEditHTSDialog(object):
    def setupUi(self, AddEditHTSDialog):
        AddEditHTSDialog.setObjectName("AddEditHTSDialog")
        AddEditHTSDialog.resize(454, 256)
        self.buttonBox = QtGui.QDialogButtonBox(AddEditHTSDialog)
        self.buttonBox.setGeometry(QtCore.QRect(110, 220, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_2 = QtGui.QLabel(AddEditHTSDialog)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 71, 26))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(AddEditHTSDialog)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 71, 26))
        self.label_3.setObjectName("label_3")
        self.daylineEdit = QtGui.QLineEdit(AddEditHTSDialog)
        self.daylineEdit.setGeometry(QtCore.QRect(110, 70, 113, 26))
        self.daylineEdit.setMaxLength(2)
        self.daylineEdit.setObjectName("daylineEdit")
        self.label_4 = QtGui.QLabel(AddEditHTSDialog)
        self.label_4.setGeometry(QtCore.QRect(20, 120, 71, 26))
        self.label_4.setObjectName("label_4")
        self.timelineEdit = QtGui.QLineEdit(AddEditHTSDialog)
        self.timelineEdit.setGeometry(QtCore.QRect(110, 120, 113, 26))
        self.timelineEdit.setMaxLength(5)
        self.timelineEdit.setObjectName("timelineEdit")
        self.subjectlineEdit = QtGui.QLineEdit(AddEditHTSDialog)
        self.subjectlineEdit.setGeometry(QtCore.QRect(110, 20, 113, 26))
        self.subjectlineEdit.setObjectName("subjectlineEdit")
        self.label_5 = QtGui.QLabel(AddEditHTSDialog)
        self.label_5.setGeometry(QtCore.QRect(20, 170, 71, 26))
        self.label_5.setObjectName("label_5")
        self.replineEdit = QtGui.QLineEdit(AddEditHTSDialog)
        self.replineEdit.setGeometry(QtCore.QRect(110, 170, 113, 26))
        self.replineEdit.setMaxLength(2)
        self.replineEdit.setObjectName("replineEdit")
        self.label_6 = QtGui.QLabel(AddEditHTSDialog)
        self.label_6.setGeometry(QtCore.QRect(240, 20, 201, 26))
        self.label_6.setObjectName("label_6")
        self.mhclineEdit = QtGui.QLineEdit(AddEditHTSDialog)
        self.mhclineEdit.setGeometry(QtCore.QRect(250, 50, 191, 26))
        self.mhclineEdit.setMaxLength(16)
        self.mhclineEdit.setObjectName("mhclineEdit")
        self.label_7 = QtGui.QLabel(AddEditHTSDialog)
        self.label_7.setGeometry(QtCore.QRect(240, 120, 201, 26))
        self.label_7.setObjectName("label_7")
        self.semlineEdit = QtGui.QLineEdit(AddEditHTSDialog)
        self.semlineEdit.setGeometry(QtCore.QRect(250, 150, 191, 26))
        self.semlineEdit.setObjectName("semlineEdit")
        self.label_2.setBuddy(self.subjectlineEdit)
        self.label_3.setBuddy(self.daylineEdit)
        self.label_4.setBuddy(self.timelineEdit)
        self.label_5.setBuddy(self.replineEdit)
        self.label_6.setBuddy(self.mhclineEdit)
        self.label_7.setBuddy(self.semlineEdit)

        self.retranslateUi(AddEditHTSDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AddEditHTSDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AddEditHTSDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddEditHTSDialog)

    def retranslateUi(self, AddEditHTSDialog):
        AddEditHTSDialog.setWindowTitle(QtGui.QApplication.translate("AddEditHTSDialog", "OpenHTS- Add", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("AddEditHTSDialog", "&Subject:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("AddEditHTSDialog", "&Day:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("AddEditHTSDialog", "&Time:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("AddEditHTSDialog", "&Replicates:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("AddEditHTSDialog", "&Mean hormone concentration:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("AddEditHTSDialog", "&Standard error of the mean:", None, QtGui.QApplication.UnicodeUTF8))

