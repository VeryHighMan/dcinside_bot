import sys
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

PhantomJS_Path = './phantomjs/bin\phantomjs'


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("댓글 작성기 v0.2")
        self.setGeometry(300, 50, 1100, 700)

        self.url = 'http://gall.dcinside.com/board/lists'
        self.url_m = 'http://gall.dcinside.com/mgallery/board/lists'

        #마이너 갤

        self.gallery_id = 'baseball_new7'

        self.btn_refresh = QPushButton("새로고침", self)
        self.btn_refresh.setGeometry(800, 0, 300, 30)
        self.btn_refresh.clicked.connect(self.btn_refresh_clicked)

        btn_setId = QPushButton("갤러리 설정", self)
        btn_setId.move(900, 50)
        btn_setId.clicked.connect(self.btn_setId_clicked)

        btn_setId_yagall = QPushButton("국내야구 갤러리", self) # baseball_new7
        btn_setId_yagall.move(800, 100)
        btn_setId_yagall.clicked.connect(self.setId_yegall)

        btn_setId_aoegame = QPushButton("중세게임 갤러리", self) # aoegame
        btn_setId_aoegame.move(900, 100)
        btn_setId_aoegame.clicked.connect(self.setId_aoegame)

        btn_setId_comic = QPushButton("만화 갤러리", self) # comic_new1
        btn_setId_comic.move(1000, 100)
        btn_setId_comic.clicked.connect(self.setId_comic)

        btn_setId_football = QPushButton("해외축구 갤러리", self)  # football_new6
        btn_setId_football.move(800, 130)
        btn_setId_football.clicked.connect(self.setId_football)

        btn_setId_cat = QPushButton("야옹이 갤러리", self)  # cat
        btn_setId_cat.move(900, 130)
        btn_setId_cat.clicked.connect(self.setId_cat)

        btn_setId_dog = QPushButton("멍멍이 갤러리", self)  # dog
        btn_setId_dog.move(1000, 130)
        btn_setId_dog.clicked.connect(self.setId_dog)

        btn_setId_etcpro = QPushButton("기타프로그램 갤러리", self)  # etc_program2
        btn_setId_etcpro.move(800, 160)
        btn_setId_etcpro.clicked.connect(self.setId_etcpro)

        btn_setId_game = QPushButton("게임 갤러리", self)  # game1
        btn_setId_game.move(920, 160)
        btn_setId_game.clicked.connect(self.setId_game)

        btn_setId_fantasy = QPushButton("판타지 갤러리", self)  # fantasy_new
        btn_setId_fantasy.move(1000, 160)
        btn_setId_fantasy.clicked.connect(self.setId_fantasy)

        self.tedit_galleryId = QTextEdit(self.gallery_id, self)
        self.tedit_galleryId.setGeometry(800, 50, 100, 30)
        self.tedit_galleryId.setEnabled(True)

        self.label_comment = QLabel('닉네임 입력', self)
        self.label_comment.setGeometry(800, 250, 100, 30)

        self.tedit_nick = QTextEdit('', self)
        self.tedit_nick.setGeometry(800, 280, 100, 30)

        self.label_pw = QLabel('비밀번호 입력', self)
        self.label_pw.setGeometry(950, 250, 100, 30)

        self.tedit_pw = QTextEdit('', self)
        self.tedit_pw.setGeometry(950, 280, 100, 30)

        self.label_comment = QLabel('댓글 입력', self)
        self.label_comment.setGeometry(800, 310, 100, 30)

        self.tedit_comment = QTextEdit('', self)
        self.tedit_comment.setGeometry(800, 340, 250, 50)

        self.tableWidget = QTableWidget(self)
        self.initUI()

    def btn_refresh_clicked(self):
        self.refresh(self.url)

    def btn_setId_clicked(self) :
        self.setId()

    def btn_cell_clicked(self) :
        button = qApp.focusWidget()
        # or button = self.sender()
        index = self.tableWidget.indexAt(button.pos())

        if index.isValid():
            #클릭한 버튼 행, 열, 해당 글 번호
            #print(index.row(), index.column(), self.tableWidget.item(index.row(), 0).text())
            self.target_no = self.tableWidget.item(index.row(), 0).text()
            #print(self.target_no)
            write_comment(self.gallery_id, self.target_no, self.tedit_nick.toPlainText(), self.tedit_pw.toPlainText(), self.tedit_comment.toPlainText())

    def initUI(self):
        soup_data = getData(self.url, self.gallery_id)

        subject_no = soup_data.find_all("td", {"class": "t_notice"}) # 글 번호
        td = soup_data.find_all("td", {"class": "t_subject"}) # 글 제목
        subject_writer = soup_data.find_all("td", {"class": "t_writer user_layer"}) # 글 작성자
        subject_date = soup_data.find_all("td", {"class": "t_date"}) # 글 작성 일자

        subject_no_list = []  # 글 번호 리스트
        subject_list = []  # 글 제목 리스트
        subject_writer_list = [] # 글 작성자 리스트
        subject_date_list = [] # 글 작성 일자 리스트

        for m in subject_no :
            subject_no_list.append(m.string)

        for m in td :
            subject_list.append(m.a.string)

        for m in subject_writer :
            # len(m)이 3인경우만 유저가 쓴 글
            if len(m) == 3 :
                if m['ip'] != '': # 유동닉
                    subject_writer_list.append(m['user_name'])
                    #print(m['ip'], '유동닉')
                elif m['ip'] == '' : # 고정닉1
                    subject_writer_list.append(m['user_name'])
                    #print(m['ip'], '고정닉')
            else :
                subject_writer_list.append(m['user_name'])

        for m in subject_date :
            subject_date_list.append(m.string)

        #self.setGeometry(800, 200, 400, 300)
        self.tableWidget.resize(800, 700)
        self.tableWidget.setRowCount(len(subject_no_list))
        self.tableWidget.setColumnCount(5)

        for index, item in enumerate(subject_no_list) :
            self.tableWidget.setItem(index, 0, QTableWidgetItem(subject_no_list[index]))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(subject_list[index]))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(subject_writer_list[index]))
            self.tableWidget.setItem(index, 3, QTableWidgetItem(subject_date_list[index]))

            #공지 제외하고 댓글 작성 버튼 생성
            if subject_no_list[index] != '공지' :
                self.btn_cell = QPushButton('댓글 작성')
                self.btn_cell.clicked.connect(self.btn_cell_clicked)
                self.tableWidget.setCellWidget(index, 4, self.btn_cell)
            else :
                self.tableWidget.setCellWidget(index, 4, None)

        self.tableWidget.resizeColumnsToContents() # 전체 컬럼 너비 자동 지정
        self.tableWidget.setColumnWidth(1, 400) # 글 제목 너비 조절
        self.tableWidget.horizontalHeader().setStretchLastSection(True) # 마지막 컬럼을 table width 에 맞춤

    def refresh(self, url):
        soup_data = getData(url, self.gallery_id)

        subject_no = soup_data.find_all("td", {"class": "t_notice"}) # 글 번호
        td = soup_data.find_all("td", {"class": "t_subject"}) # 글 제목
        subject_writer = soup_data.find_all("td", {"class": "t_writer user_layer"}) # 글 작성자
        subject_date = soup_data.find_all("td", {"class": "t_date"}) # 글 작성 일자

        subject_no_list = []  # 글 번호 리스트
        subject_list = []  # 글 제목 리스트
        subject_writer_list = [] # 글 작성자 리스트
        subject_date_list = [] # 글 작성 일자 리스트

        for m in subject_no :
            subject_no_list.append(m.string)

        for m in td :
            subject_list.append(m.a.string)

        for m in subject_writer :
            # len(m)이 3인경우만 유저가 쓴 글
            if len(m) == 3 :
                if m['ip'] != '': # 유동닉
                    subject_writer_list.append(m['user_name'])
                    #print(m['ip'], '유동닉')
                elif m['ip'] == '' : # 고정닉
                    subject_writer_list.append(m['user_name'])
                    #print(m['ip'], '고정닉')
            else :
                subject_writer_list.append(m['user_name'])

        for m in subject_date :
            subject_date_list.append(m.string)

        for index, item in enumerate(subject_no_list) :
            self.tableWidget.setItem(index, 0, QTableWidgetItem(subject_no_list[index]))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(subject_list[index]))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(subject_writer_list[index]))
            self.tableWidget.setItem(index, 3, QTableWidgetItem(subject_date_list[index]))

            #공지 제외하고 댓글 작성 버튼 생성
            if subject_no_list[index] != '공지' :
                self.btn_cell = QPushButton('댓글 작성')
                self.btn_cell.clicked.connect(self.btn_cell_clicked)
                self.tableWidget.setCellWidget(index, 4, self.btn_cell)
            else :
                self.tableWidget.setCellWidget(index, 4, None)

        self.tableWidget.horizontalHeader().setStretchLastSection(True) # 마지막 컬럼을 table width 에 맞춤

    def setId(self) :
        self.gallery_id = self.tedit_galleryId.toPlainText()
        self.refresh(self.url)

    def setId_yegall(self) :
        self.tedit_galleryId.setText('baseball_new7')
        self.gallery_id = 'baseball_new7'
        self.refresh(self.url)

    def setId_comic(self) :
        self.tedit_galleryId.setText('comic_new1')
        self.gallery_id = 'comic_new1'
        self.refresh(self.url)

    def setId_aoegame(self) :
        self.tedit_galleryId.setText('aoegame')
        self.gallery_id = 'aoegame'
        self.refresh(self.url_m)

    def setId_football(self) :
        self.tedit_galleryId.setText('football_new6')
        self.gallery_id = 'football_new6'
        self.refresh(self.url)

    def setId_cat(self) :
        self.tedit_galleryId.setText('cat')
        self.gallery_id = 'cat'
        self.refresh(self.url)

    def setId_dog(self) :
        self.tedit_galleryId.setText('dog')
        self.gallery_id = 'dog'
        self.refresh(self.url)

    def setId_etcpro(self) :
        self.tedit_galleryId.setText('etc_program2')
        self.gallery_id = 'etc_program2'
        self.refresh(self.url)

    def setId_game(self) :
        self.tedit_galleryId.setText('game1')
        self.gallery_id = 'game1'
        self.refresh(self.url)

    def setId_fantasy(self) :
        self.tedit_galleryId.setText('fantasy_new')
        self.gallery_id = 'fantasy_new'
        self.refresh(self.url)

def getData(url, gallery_id):

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
        }

    payload = {'id': gallery_id, 'page': '1'}
    r = requests.get(url, params=payload, headers=hdr)
    soup = BeautifulSoup(r.text, "lxml")

    return soup;

def write_comment(gallery_id, subject_no, id, pw, comment):
    driver = webdriver.PhantomJS(PhantomJS_Path)
    target_url = 'http://gall.dcinside.com/board/view/?id=' + gallery_id + '&no=' + subject_no
    print(target_url)

    driver.get(target_url)
    driver.find_element_by_name('name').send_keys(id)
    driver.find_element_by_name('password').send_keys(pw)
    driver.find_element_by_id('memo').send_keys(comment)
    #  등록버튼 클릭
    driver.find_element_by_id('re_write').click()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    #getData()
    app.exec_()
