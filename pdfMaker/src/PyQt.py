import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QUrl
from PdfServer import start_server
# from PyQt5.QtWebEngineWidgets import *
# from PyQt5 import *
# from PyQt5 import QtWebEngineWidgets


#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("/home/hwi/github/hansin-medi/pdfMaker/src/ui/main.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        # button
        self.btn_inference.clicked.connect(self.inference)
        self.btn_print.clicked.connect(self.print)
    
    
    def inference(self):
        print('get user info',self.get_userInfo())
        print('inference..')
        if (self.startAxcare()):
            self.webView.load(QUrl.fromLocalFile('/home/hwi/github/hansin-medi/pdfMaker/src/result.html'))    
        
    
    def print(self):
        # call pdf
        print('pressed print button')
        start_server()
        
    def get_userInfo(self):
        name = self.intxt_name.toPlainText()
        birth = self.intxt_birth.toPlainText()
        examDate = self.intxt_examDate.toPlainText()
        
        return name, birth, examDate

    def startAxcare(self):
        return True

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
    
