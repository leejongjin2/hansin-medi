import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
import pandas as pd
from PyqtDatabase import HanshinDatabase
import datetime

ui_generatePDF = uic.loadUiType(r"/home/autocare/바탕화면/new_train_percent_hanshin/Final_Hanshin/hansin-medi/pdfMaker/src/ui/generatingPDF.ui")[0]

class WindowClass(QMainWindow, ui_generatePDF) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)        
        self.database = HanshinDatabase()
        self.btn_search.clicked.connect(self.search)
        self.btn_generatePDF.clicked.connect(self.printPDF)

    def search(self):
        try:
            # TODO If Patients == None
            index_name, patients = self.database.get_patientData(cht_no=self.line_chtNo.text(), bun_no=self.line_bunNo.text(), inspc_date=self.line_InspcDate.text(), name=self.line_name.text())
            if '선택' not in index_name:
                index_name.insert(0, '선택')
            self.draw_patientsTableWidget(index_name, patients)
            
            print()
        except ValueError:
            print("nothing inserted, plz insert !")

    # TODO Check time and refactoring(combine two for-loop)
    def draw_patientsTableWidget(self, index_name, patients):
        print(len(patients))
        start = datetime.datetime.now()
        
        # setting Table Widget
        # TODO Table Widget -> uneditable
        self.tableWidget.setRowCount(len(patients))
        self.tableWidget.setColumnCount(len(index_name))
        self.tableWidget.setHorizontalHeaderLabels(index_name)
        
        for idx, r in enumerate(patients):
            self.checkBoxList = []
            for i in range(len(patients)):
                ckbox = QCheckBox()
                self.checkBoxList.append(ckbox)
            
            for i in range(len(patients)):              
                cellWidget = QWidget()
                layoutCB = QHBoxLayout(cellWidget)
                layoutCB.addWidget(self.checkBoxList[i])
                layoutCB.setAlignment(QtCore.Qt.AlignCenter)            
                layoutCB.setContentsMargins(0,0,0,0)
                cellWidget.setLayout(layoutCB)

            self.tableWidget.setCellWidget(i,0,cellWidget)
        
        # insert Data in Table Widget
        for row, p in enumerate(patients):
            for col in range(len(index_name)-1):
                self.tableWidget.setItem(row, col+1, QTableWidgetItem(str(patients[row][col])))
        end = datetime.datetime.now()
        print(end-start)
   
    def printPDF(self):
        checkBox = list(map(QCheckBox.isChecked, self.checkBoxList))
        print(checkBox)
        
if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()
    
