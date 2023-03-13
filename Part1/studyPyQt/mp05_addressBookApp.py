# 주소록 GUI 프로그램 - MySQL 연동
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
import pymysql

class qtApp(QMainWindow) :
    conn = None
    curIdx = 0 # 현재데이터 PK

    def __init__(self) :
        super().__init__()
        uic.loadUi('./studyPyQt/addressBook.ui',self)
        # self.setWindowIcon(QIcon('./studyPyQt/newspaper.png'))
        self.setWindowIcon(QIcon('./studyPyQt/adress-book.png'))
        self.setWindowTitle('주소록 v0.5')

        self.initDB() #DB 초기화

        self.btnNew.clicked.connect(self.btnNewClicked)
        self.btnSave.clicked.connect(self.btnSaveClicked)
        self.tblAddress.doubleClicked.connect(self.tblAddressDoubleClicked)
        self.btnDel.cliced.connect(self.btnDelClicked)

    def btnDelClicked(self):
            pass

    def btnNewClicked(self): # 신규버튼 누르면
        #라인 에디트 내용 삭제 후 이름에 포커스
        self.txtName.setText('')
        self.txtPhone.setText('')
        self.txtEmail.setText('')
        self.txtAddress.setText('')
        self.txtName.setFocus()
        self.curIdx = 0 #0은 진짜 신규

    def tblAddressDoubleClicked(self):
        rowIndex = self.tblAddress.currentRow()
        self.txtName.setText(self.tblAddress.item(rowIndex, 1). text())
        self.txtPhone.setText(self.tblAddress.item(rowIndex, 2). text())
        self.txtEmail.setText(self.tblAddress.item(rowIndex, 3). text())
        self.txtAddress.setText(self.tblAddress.item(rowIndex, 4). text())
        self.curIdx = int(self.tblAddress.item(rowIndex, 0).text())
        print(self.curIdx)

    def btnSaveClicked(self): # 저장
        fullName = self.txtName.text()
        phoneNum = self.txtPhone.text()
        email = self.txtEmail.text()
        address = self.txtAddress.text()
    
        print(fullName, phoneNum, email, address)
        # 이름과 전화번호를 입력하지 않으면 알람
        if fullName == '' or phoneNum == '':
            QMessageBox.warning(self, '주의', '이름과 핸드폰을 입력하세요')
            return # 진행불가
        else:
            self.conn = pymysql.connect(host='localhost', user='root', password='12345', db= 'miniproject', charset='utf8')
            if self.curIdx == 0: # 신규
            # 네게 변수값 받아서 INSERT 쿼리문 만들기
                query = '''insert into addressbook (fullname, PhoneNum, Email, Address)
			    values(%s,%s,%s,%s) '''

            else:
                query ='''UPDate addressbook
                            set fullName = %s
                             ,phoneNum = %s
                             ,Email = %s
                            , address = %s
                             where Idx = %s'''
                
            cur = self.conn.cursor()
            if self.curIdx == 0:
                cur.execute(query,(fullName, phoneNum, email, address))
            else:
                cur.execute(query,(fullName, phoneNum, email, address, self.curIdx))

            self.conn.commit()
            self.conn.close()
            
            #저장 성공 메세
            if self.curIdx == 0:
                QMessageBox.about(self, '성공', '저장 성공했습니다!')
            else: 
                QMessageBox.about(self,'성공','변경 성공했습니다!')

            self.initDB()#QTableWidget 새 데이터가 출력되도록
            self.btnNewClicked()  # 입력창에 내용들이 없어져야함

    def initDB(self): 
        self.conn = pymysql.connect(host='localhost', user='root', password='12345', db='miniproject', charset='utf8')
        cur= self.conn.cursor()
        query =     '''select Idx
                    ,FullName
                    ,PhoneNum
                    ,Email
                    ,Address
                 from Addressbook
                    '''
        cur.execute(query)
        rows = cur.fetchall()

        #print(rows)
        self.makeTable(rows)
        self.conn.close() # 프로그램 종료할 때


    def makeTable(self, rows):
        self.tblAddress.setColumnCount(5) #0. 열갯수
        self.tblAddress.setRowCount(len(rows))
        self.tblAddress.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tblAddress.setHorizontalHeaderLabels(['번호','이름','핸드폰' ,'이메일','주소'])
        self.tblAddress.setColumnWidth(0,0)
        self.tblAddress.setColumnWidth(1,70)
        self.tblAddress.setColumnWidth(2,105)
        self.tblAddress.setColumnWidth(3,175)
        self.tblAddress.setColumnWidth(4,200)
        self.tblAddress.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for i, row in enumerate(rows):
            idx = row[0]
            fullName =row[1]
            PhoneNum = row[2]
            email = row[3]
            address = row[4]

            self.tblAddress.setItem(i, 0, QTableWidgetItem(str(idx)))
            self.tblAddress.setItem(i, 1, QTableWidgetItem(fullName))
            self.tblAddress.setItem(i, 2, QTableWidgetItem(PhoneNum))
            self.tblAddress.setItem(i, 3, QTableWidgetItem(email))
            self.tblAddress.setItem(i, 4, QTableWidgetItem(address))

        self.stbCurrent.showMessage(f'전체 주소록:{len(rows)}개')

        
if __name__ == '__main__' :    
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())