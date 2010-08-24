#!/usr/bin/env python
# OpenHTS Copyright (c) 2010 Abhishek Tiwari. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.
import platform
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import qrc_resources
import helpform
import HTSdata
import addedithtsdlg

__version__ = "1.0.0"

class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.hts = HTSdata.HTSContainer()
        self.table = QTableWidget()
        self.setCentralWidget(self.table)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)
        fileNewAction = self.createAction("&New...", self.fileNew,
                "filenew", QKeySequence.New,
                "Create a HTS data file")
        fileOpenAction = self.createAction("&Open...", self.fileOpen,
                "fileopen", QKeySequence.Open,
                "Open an existing  HTS data file")
        fileSaveAction = self.createAction("&Save", self.fileSave,
                "filesave", QKeySequence.Save, "Save the HTS data")
        fileSaveAsAction = self.createAction("Save &As...",
                self.fileSaveAs, icon="filesaveas",
                tip="Save the HTS data using a new name")
        fileImportDOMAction = self.createAction(
                "&Import from XML (DOM)...", self.fileImportDOM,
                "fileimport", tip="Import the HTS data from an XML file")
        fileImportSAXAction = self.createAction(
                "I&mport from XML (SAX)...", self.fileImportSAX,
                "fileimport", tip="Import the HTS data from an XML file")
        fileExportXmlAction = self.createAction(
                "E&xport as XML...", self.fileExportXml,
                "fileexport", tip="Export the HTS data to an XML file")
        fileQuitAction = self.createAction("&Quit", self.close,
                "filequit", "Ctrl+Q", "Close the application")
        editAddAction = self.createAction("&Add...", self.editAdd,
                "editadd", "Ctrl+A", "Add a HTS data point")
        editEditAction = self.createAction("&Edit...", self.editEdit,
                "editedit",  "Ctrl+E", "Edit the current HTS data point")
        editRemoveAction = self.createAction("&Remove...",
                self.editRemove, "editdelete", "Del", 
                "Remove a HTS data point")
        toolEntropyAction = self.createAction("&Entropy", self.toolEntropy,
                "toolentropy", "Entropy calculator for HTS")
        toolPulseAction = self.createAction("&Pulse", self.toolPulse,
                "toolpulse", "Pulse detection for HTS")
        toolModelAction = self.createAction("&Model", self.toolModel,
                "toolCellML", "CellML Models for HPA Axis")
        helpHelpAction = self.createAction("&Help", self.helpHelp,
                "helphelp", "F1", "Help content for the OpenHTS")
        helpAboutAction = self.createAction("&About", self.helpAbout,
                "helpabout", "Ctrl+H", tip="About the application")

        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, (fileNewAction, fileOpenAction,
                fileSaveAction, fileSaveAsAction, None,
                fileImportDOMAction, fileImportSAXAction,
                fileExportXmlAction, None, fileQuitAction))
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (editAddAction, editEditAction,
                editRemoveAction))
        toolMenu = self.menuBar().addMenu("&Tools")
        self.addActions(toolMenu,(toolEntropyAction, toolPulseAction, None, toolModelAction))
        helpMenu = self.menuBar().addMenu("&Help")
        self.addActions(helpMenu,(helpHelpAction, None, helpAboutAction))
        
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
                                      fileSaveAsAction, toolEntropyAction, toolPulseAction, toolModelAction, helpHelpAction, helpAboutAction))
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")
        self.addActions(editToolbar, (editAddAction, editEditAction,
                                      editRemoveAction))
        
        self.connect(self.table,
                SIGNAL("itemDoubleClicked(QTableWidgetItem*)"),
                self.editEdit)
        QShortcut(QKeySequence("Return"), self.table, self.editEdit)

        settings = QSettings()
        size = settings.value("MainWindow/Size",
                              QVariant(QSize(800, 600))).toSize()
        self.resize(size)
        position = settings.value("MainWindow/Position",
                                  QVariant(QPoint(0, 0))).toPoint()
        self.move(position)
        self.restoreState(
                settings.value("MainWindow/State").toByteArray())
        
        self.setWindowTitle("OpenHTS")
        QTimer.singleShot(0, self.loadInitialFile)
        
    def createAction(self, text, slot=None, icon=None, shortcut=None, 
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action
        
    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)
        
    def closeEvent(self, event):
        if self.okToContinue():
            settings = QSettings()
            settings.setValue("LastFile",
                    QVariant(self.hts.filename()))
            settings.setValue("MainWindow/Size", QVariant(self.size()))
            settings.setValue("MainWindow/Position",
                    QVariant(self.pos()))
            settings.setValue("MainWindow/State",
                    QVariant(self.saveState()))
        else:
            event.ignore()
    
    def okToContinue(self):
        if self.hts.isDirty():
            reply = QMessageBox.question(self,
                            "OpenHTS - Unsaved Changes",
                            "Save unsaved changes?",
                            QMessageBox.Yes|QMessageBox.No|
                            QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                self.fileSave()
        return True
    
    def loadInitialFile(self):
        settings = QSettings()
        fname = settings.value("LastFile").toString()
        if fname and QFile.exists(fname):
            ok, msg = self.hts.load(fname)
            self.statusBar().showMessage(msg, 5000)
        self.updateTable()
    
    def updateTable(self, current=None):
        self.table.clear()
        self.table.setRowCount(len(self.hts))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Subject", "Day", "MHC(nM)",
                "SEM", "Time(min)", "Replicates"])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        
        selected = None
        
        for row, htsDP in enumerate(self.hts):
            item = QTableWidgetItem(htsDP.subject)
            if current is not None and current == id(htsDP):
                selected = item
            item.setData(Qt.UserRole, QVariant(long(id(htsDP))))
            self.table.setItem(row, 0, item)
            day = htsDP.day
            if day is not None:
                item = QTableWidgetItem("%s" % day)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 1, item)
            mhc = float(htsDP.mhc)
            if mhc is not None:
                item = QTableWidgetItem("%.10f" % mhc)
                item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                self.table.setItem(row, 2, item)
            sem = float(htsDP.sem)
            if sem is not None:
                item = QTableWidgetItem("%.10f" % sem)
                item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                self.table.setItem(row, 3, item)
            time= int(htsDP.time)
            if sem is not None:
                item = QTableWidgetItem("%d" % time)
                item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                self.table.setItem(row, 4, item)
            replicates= int(htsDP.replicates)
            if sem is not None:
                item = QTableWidgetItem("%d" % replicates)
                item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                self.table.setItem(row, 5, item)
        self.table.resizeColumnsToContents()
        if selected is not None:
            selected.setSelected(True)
            self.table.setCurrentItem(selected)
            self.table.scrollToItem(selected)
    
         
    
    def fileNew(self):
        if not self.okToContinue():
            return
        self.hts.clear()
        self.statusBar().clearMessage()
        self.updateTable()

    
    def fileOpen(self):
        if not self.okToContinue():
            return
        path = QFileInfo(self.hts.filename()).path() \
                if not self.hts.filename().isEmpty() else "."
        fname = QFileDialog.getOpenFileName(self,
                    "OpenHTS - Load HTS Data", path,
                    "HTS data files (%s)" % \
                    self.hts.formats())
        if not fname.isEmpty():
            ok, msg = self.hts.load(fname)
            self.statusBar().showMessage(msg, 5000)
            self.updateTable()
    
    def fileSave(self):
        pass
    
    def fileSaveAs(self):
        pass
    
    def fileImportDOM(self):
        pass
    
    def fileImportSAX(self):
        pass
    
    def fileImport(self, format):
        pass
    
    def fileExportXml(self):
        fname = self.hts.filename()
        if fname.isEmpty():
            fname = "."
        else:
            i = fname.lastIndexOf(".")
            if i > 0:
                fname = fname.left(i)
            fname += ".xml"
        fname = QFileDialog.getSaveFileName(self,
                    "OpenHTS - Export HTS Data", fname,
                    "OpenHTS XML files (*.xml)")
        if not fname.isEmpty():
            if not fname.contains("."):
                fname += ".xml"
            ok, msg = self.hts.exportXml(fname)
            self.statusBar().showMessage(msg, 5000)

    
    def editAdd(self):
        form = addedithtsdlg.AddEditHTSDlg(self.hts, None,
                                               self)
        if form.exec_():
            self.updateTable(id(form.htsDP))
    
    def editEdit(self):
        htsDP = self.currenthtsDP()
        if htsDP is not None:
            form = addedithtsdlg.AddEditHTSDlg(self.hts,
                                                   htsDP, self)
            if form.exec_():
                self.updateTable(id(htsDP))
    
    def editRemove(self):
        htsDP = self.currenthtsDP()
        if htsDP is not None:
            
            if QMessageBox.question(self,
                        "OpenHTS - Delete HTS data point",
                        "Delete data for subject %s, day %s on time %s?" % (htsDP.subject, htsDP.day, htsDP.time),
                        QMessageBox.Yes|QMessageBox.No) == \
                    QMessageBox.Yes:
                self.hts.delete(htsDP)
                self.updateTable()
    
    def currenthtsDP(self):
        row = self.table.currentRow()
        if row > -1:
            item = self.table.item(row, 0)
            id = item.data(Qt.UserRole).toLongLong()[0]
            return self.hts.htsDPFromId(id)
        return None
    
    def helpAbout(self):
        QMessageBox.about(self, "OpenHTS - About",
                """<b>OpenHTS</b> v %s
                <p>Copyright &copy; 2010 Abhishek Tiwari. 
                All rights reserved.
                <p>An open source hormone time series analysis package in Python. 
                under the terms of the GNU General Public License.
                <p>Python %s - Qt %s - PyQt %s on %s""" % (
                __version__, platform.python_version(),
                QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))
    def helpHelp(self):
        form = helpform.HelpForm("index.html", self)
        form.show()
        
    
    def toolPulse(self):
        pass
    
    def toolEntropy(self):
        pass
    
    def toolModel(self):
        pass
    
    
def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Abhishek Tiwari")
    app.setOrganizationDomain("abhishek-tiwari.com")
    app.setApplicationName("OpenHTS")
    app.setWindowIcon(QIcon(":/icon.png"))
    form = MainWindow()
    form.show()
    app.exec_()


main()

        