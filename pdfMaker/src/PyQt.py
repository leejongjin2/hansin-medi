import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QUrl
# from Server import start_server
from Server import SingletonServer

form_class = uic.loadUiType("/home/hwi/github/hansin-medi/pdfMaker/src/ui/main.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        # button
        self.btn_inference.clicked.connect(self.inference)
        self.btn_print.clicked.connect(self.printPDF)
        self.isServer = False
    
    def inference(self):
        print('get user info',self.get_userInfo())
        print('inference..')
        if (self.start_Axcare()):
            self.webView.load(QUrl.fromLocalFile('/home/hwi/github/hansin-medi/pdfMaker/src/result.html'))
        
    # print pdf        
    def printPDF(self):
        print('pressed print button')
        SingletonServer().start_server()
        
    def get_userInfo(self):
        name = self.intxt_name.toPlainText()
        birth = self.intxt_birth.toPlainText()
        examDate = self.intxt_examDate.toPlainText()
        
        return name, birth, examDate

    def start_Axcare(self):
        return True

if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()
    
