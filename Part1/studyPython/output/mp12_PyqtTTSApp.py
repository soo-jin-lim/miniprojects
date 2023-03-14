import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * # QIcon은 여기있습
from PyQt5.QtCore import * # Qt.white...

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPython/ttsApp.ui', self)
        self.setWindowTitle('텍스트 투 스피치 v0.3')

        self.btnQrgen.clicked.connect(self.btnQrGenClicked)
        self.txtdata.returnPressed.connect(self.btnQrGenClicked)

    def btnQrGenClicked(self):
        text = self.txtQrData.text()

        if text == '':
            QMessageBox.warning(self, '경고', '텍스트를 입력하세요')
        
            return
        
        tts = gTTS(text=text, lang='ko' )
        tts.save('./studyPython/output/hi.mp3')
        playsound('./studyPython/output/hi.mp3')

if __name__ == '__main__' :    
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())