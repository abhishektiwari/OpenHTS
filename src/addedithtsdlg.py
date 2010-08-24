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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import HTSdata
import ui_addedithtsdlg


class AddEditHTSDlg(QDialog,
        ui_addedithtsdlg.Ui_AddEditHTSDialog):

    def __init__(self, HTS, htsDP=None, parent=None):
        super(AddEditHTSDlg, self).__init__(parent)
        self.setupUi(self)

        self.hts = HTS
        self.htsDP = htsDP

        if htsDP is not None:
            self.subjectlineEdit.setText(htsDP.subject)
            self.daylineEdit.setText(htsDP.day)
            self.timelineEdit.setText(htsDP.time)
            self.mhclineEdit.setText(htsDP.mhc)
            self.semlineEdit.setText(htsDP.sem)
            self.replineEdit.setText(htsDP.replicates)
            
            self.buttonBox.button(QDialogButtonBox.Ok).setText(
                    "&Accept")
            self.setWindowTitle("OpenHTS - Edit HTS")
        self.on_subjectlineEdit_textEdited(QString())


    @pyqtSignature("QString")
    def on_subjectlineEdit_textEdited(self, text):
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(
                not self.subjectlineEdit.text().isEmpty())


    def accept(self):
        subject = self.subjectlineEdit.text()
        day = self.daylineEdit.text()
        mhc= self.mhclineEdit.text()
        sem= self.semlineEdit.text()
        time= self.timelineEdit.text()
        replicates=self.replineEdit.text()
        
        if self.htsDP is None:
            self.htsDP = HTSdata.HTSO(subject, day, mhc, 
                                      sem, time, replicates)
            self.hts.add(self.htsDP)
        else:
            self.hts.updateHTS(self.htsDP, subject, day, mhc,
                                sem, time, replicates)
        QDialog.accept(self)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = AddEditHTSDlg(0)
    form.show()
    app.exec_()
