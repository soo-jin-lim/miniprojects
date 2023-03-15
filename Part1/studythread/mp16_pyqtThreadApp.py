# 스레드 미사용 앱
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * # QIcon은 여기있습
from PyQt5.QtCore import * # Qt.white...
import time

MAX = 10000

class BackgroundWorker(QThread): # PyQt5 스레드를 위한 클래스 존재
    procchanged = pyqtSignal(int) #커스텀 시그널 (마우스 클릭같은 시그널을 따로만드는 것)

    def __init__(self,count=0,  parent= None) -> None:
        super().__init__()
        self.parent = parent
        self.working =True # 스레드 동작여부
        self.count=count

    def run(self): #thread.start () --> run() 대신 실행
        while self.working:
            if self.count <= MAX:
                self.procchanged.emit(self.count) # 시그널을 내보냄
                self.count += 1 # 값 증가만 // 업무 프로세스 동작하는 위치
                time.sleep(0.001) # 0.000001 세밀하게 주면 GUI 처리를 못함
            else:
                self.working = False # 멈춤

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyThread/threadApp.ui', self)
        self.setWindowTitle('노쓰레드앱 v0.4')
        self.pgbTask.setValue(0)

        self.btnStart.clicked.connect(self.btnStartClicked)

        # 쓰레드 생성
        self.worker = BackgroundWorker(parent=self, count = 0)
        # 백그라운드 워커에 있는 시그널을 접근 슬롯함수
        self.worker.procchanged.connect(self.procUpdate)
        self.pgbTask.setRange(0,MAX)

   # @pyqtSlot(int) 데코레이션
    def procUpdate(self, count):
        self.txbLog.append(f'스레드 출력 > {count} ')
        self.pgbTask.setValue(count)
        print(f'스레드 출력 > {count}')
   
    #@pyqtslot()
    def btnStartClicked(self):
        self.worker.start() # 스레드 클래스 run() 실행
        self.worker.working = True
        self.worker.count = 0



if __name__ == '__main__' :    
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())