import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
import pandas as pd
from PyqtDatabase import HanshinDatabase
import datetime

ui_generatePDF = uic.loadUiType(r"/home/autocare/바탕화면/new_train_percent_hanshin/Final_Hanshin/hansin-medi/pdfMaker/src/ui/editing.ui")[0]

class WindowClass(QMainWindow, ui_generatePDF) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)        
        self.database = HanshinDatabase()

        self.btn_edit.clicked.connect(self.edit)
    
    def edit(self):
        # tableWidget
        try:
            index_name, indexes = self.database.get_analysisIndexes()
            
            # TODO Table Widget -> uneditable
            self.tableWidget.setRowCount(len(indexes))
            self.tableWidget.setColumnCount(len(index_name))
            self.tableWidget.setHorizontalHeaderLabels(index_name)
            
            # insert Data
            for row, p in enumerate(indexes):
                for col in range(len(index_name)):
                    print(row, col)
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(indexes[row][col])))
            
            print()
        except:
            print('error! function edit Exception')

if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()
    
