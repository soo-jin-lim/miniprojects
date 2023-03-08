# QtDesigner 디자인 사용 
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import*
from naverApi import *
import webbrowser # 웹브라우저 모듈
import requests

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/NaverAPISearch.ui', self)
        self.setWindowIcon(QIcon('./studyPyQt/newspaper.png'))

        # 검색 버튼 클릭시그널 / 슬롯함수
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        # 검색어 입력 후 엔터를 치면 처리
        self.txtSearch.returnPressed.connect(self.txtSearchReturned)
        self.tblResult.doubleClicked.connect(self.tableResultDoubleCliked)

    def tableResultDoubleCliked(self):
        #row = self.tblResult.currentIndex().row()
        #column = self.tblResult.currentIndex().column()
        #print(row,column)
        selected = self.tblResult.currentRow()
        url = self.tblResult.item(selected, 5).text()
        webbrowser.open(url)

    def txtSearchReturned(self):
        self.btnSearchClicked()

    def btnSearchClicked(self):
        search = self.txtSearch.text()

        if search == '':
            QMessageBox.warning(self ,'경고', '영회명을를 입력하세요.')
            return
        else:
            api = NaverApi()    # NavereApi 클래스 객체 생성
            node ='Movie'        # movie로 변경하면 영화검색 
            #outputs = [ ]
            display = 100

            result= api.get_naver_search(node, search, 1, display)
            print(result) # 출력값이 많으면 불편 // 개발할때 확인용으로 사용
            # 테이블위젯에 출력 기능
            items = result['items']     # json 전체 결과 중 items 아래 배열만 추출 
            self.makeTable(items)       # 테이블 위젯에 데이터들을 할당함수

    # 테이블 위젯에 데이터 표시 -- 네이버 영화 결과에 맞워서 
    def makeTable(self, items)-> None:
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tblResult.setColumnCount(8)
        self.tblResult.setRowCount(len(items))    # 현재 100개 행 생성
        self.tblResult.setHorizontalHeaderLabels(['영화제목', '개봉연도','감독','배우진','평점','링크','포스터'])
        self.tblResult.setColumnWidth(0, 150)
        self.tblResult.setColumnWidth(1, 260)



        #컬럼 테이블 수정금지
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for i, post, in enumerate(items):    # 0, 뉴스 ...
            # 0부터 시작해서 ! : 뉴스 번호
            title = self.replaceHtmlTag(post['title']) # HTML 특수문자 변환
            pubDate = post['pubDate']
            director = post['director'] 
            actor= post['actor']    
            userRating = post['userRating']   
            link=post['link'] 
            #image = QImage(requests.get(post['image'],stream = True))

            self.tblResult.setItem(i, 0, QTableWidgetItem(title))
            self.tblResult.setItem(i, 1, QTableWidgetItem(pubDate))
            self.tblResult.setItem(i, 2, QTableWidgetItem(director))
            self.tblResult.setItem(i, 3, QTableWidgetItem(actor))
            self.tblResult.setItem(i, 4, QTableWidgetItem(userRating))
            self.tblResult.setItem(i, 5, QTableWidgetItem(link))



    def replaceHtmlTag(self, sentence) -> str:
        result = sentence.replace('&lt','<') .replace('&gt;', '>') .replace('</b>','') .replace('&apos',"'") .replace('&quot','"') 

        # 변환 안된 특수문자가 나타나면 여기 추가

        return result
        
if __name__ == '__main__' :
    app = QApplication(sys.argv)
    ex = qtApp()     
    ex.show()
    sys.exit(app.exec_())