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
    
    def getAnalysisIndex(self):
        data = ['ALP', '알카라인포스타파제', '35.0', '130.0', 'U/L', 'ALT', '알라닌아미노전이효소', '4.0', '40.0', 'U/L', 'AST', '아세테이트아미노전이효소', '4.0', '40.0', 'U/L', 'BMI', '비만도', '18.5', '22.9', 'kg/m2', 'CA15-3', '종양표지자(CA15-3)', '0.0', '30.0', 'U/mL', 'CA19-9', '종양표지자(CA19-9)', '0.0', '34.0', 'U/mL', 'CEA', '종양표지자(CEA)', '0.0', '4.7', 'ng/mL', 'Cyfra21-1', '종양표지자(Cyfra21-1)', '0.0', '3.3', 'ng/mL', 'FreeT4', '갑상선기능검사(FreeT4)', '0.9', '1.7', 'ng/dL', 'HDL', '고밀도지단백콜레스테롤', '60.0', '999.0', 'mg/dL', 'LDL', '저밀도지단백콜레스테롤', '0.0', '129.0', 'mg/dL', 'TSH', '갑상선기능검사(TSH)', '0.3', '5.0', 'µIU/mL', 'γ-GTP', '감마글루타밀전이효소', '11.0', '63.0', 'U/L', '공복혈당', '공복혈당', '70.0', '99.0', 'mg/dL', '수축기혈압', '수축기혈압', '0.0', '119.0', 'mmHg', '알부민', '알부민', '3.5', '5.3', 'g/dL', '요단백', '요단백', '0.0', '5.0', 'mg/dL', '이완기혈압', '이완기혈압', '0.0', '79.0', 'mmHg', '중성지방', '중성지방', '0.0', '149.0', 'mg/dL', '총단백질', '총단백질', '6.5', '8.3', 'g/dL', '총콜레스테롤', '총콜레스테롤', '130.0', '199.0', 'mg/dL', '혈청크레아티닌', '혈청크레아티닌', '0.6', '1.5', 'mg/dL']
        result = []
        for idx, d in enumerate(data):
            if idx % 5 == 0:
                result.append(data[idx:idx+5])
        
        df = pd.DataFrame(result, columns=['name', 'kor_name', 'min', 'max', 'unit'])

        self.tableWidget.setRowCount(len(df.index))
        self.tableWidget.setColumnCount(len(df.columns))
        self.tableWidget.setHorizontalHeaderLabels(df.columns)
        # todo : insert data

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
            
            #################################################################
            # 여기가 오래걸려 (100개 이상일 때 문제 잇음~)
            for i in range(len(patients)):              
                cellWidget = QWidget()
                layoutCB = QHBoxLayout(cellWidget)
                layoutCB.addWidget(self.checkBoxList[i])
                layoutCB.setAlignment(QtCore.Qt.AlignCenter)            
                layoutCB.setContentsMargins(0,0,0,0)
                cellWidget.setLayout(layoutCB)

                #self.tableWidget.setCellWidget(i,0,self.checkBoxList[i])            
            self.tableWidget.setCellWidget(i,0,cellWidget)
            #################################################################
        
        # insert Data
        for row, p in enumerate(patients):
            for col in range(len(index_name)-1):
                print(row, col)
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
    