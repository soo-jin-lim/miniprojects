# 스레드 미사용 앱
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * # QIcon은 여기있습
from PyQt5.QtCore import * # Qt.white...
import time

class BackgroundWorker(QThread): # PyQt5 스레드를 위한 클래스 존재
    procchanged = pyqtSignal(int)

    def __init__(self,count=0,  parent= None) -> None:
        super().__init__()
        self.parent = parent
        self.working =True
        self.count=count

    def run(self):
        while self.working:
            self.procchanged.emit(self.count)
            self.count += 1 # 값 증가만


class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyThread/threadApp.ui', self)
        self.setWindowTitle('노쓰레드앱 v0.4')
        self.pgbTask.setValue(0)

        self.btnStart.clicked.connect(self.btnStartClicked)

        # 쓰레드 초기화
        self.worker = BackgroundWorker(parent=self)
        # 백그라운드 워커에 있는 시그널을 접근 슬롯함수
        self.worker.procchanged.connect(self.procUpdate)

        self.pgbTask.setRange(0, 1000000)

    @pyqtSlot(int)
    def procUpdate(self, count):
        self.txbLog.append(f'스레드 출력 > {count} ')
        self.pgdTask.setValue(count)
        print(f'스레드 출력 > {count}')
   
    @pyqtslot()
    def btnStartClicked(self):
        self.worker.start()
        self.worker.working = True


if __name__ == '__main__' :    
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())