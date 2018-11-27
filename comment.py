from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QMutex
from PyQt5.QtCore import QWaitCondition
from selenium import webdriver

Chromdriver_Path = './chromedriver\chromedriver.exe'

class comment(QThread) :
    
    # 사용자 정의 시그널
    cnt_value = pyqtSignal(int)

    def __init__(self, gallery_id, subject_no, id, pw, comment):
        QThread.__init__(self)
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self.cnt = 0
        self._status = True

        self.gallery_id = gallery_id
        self.subject_no = subject_no
        self.id = id
        self.pw = pw
        self.comment = comment

    def __del__(self):
        self.wait()

    def run(self):
        while True :
            self.mutex.lock()
            print(self.cnt)
            if self.cnt == 100 :
                self.cnt = 0
                self.cnt_value.emit(self.cnt)
                chrome_driver.close()
                chrome_driver.quit()
                break

            elif self.cnt == 60 :
                button_tag = chrome_driver.find_elements_by_tag_name('button')
                # 댓글 등록 버튼 찾기
                for m, n in enumerate(button_tag):
                    if button_tag[m].text == '등록':
                        button_tag[m].click()  # 클릭
                        break
                self.cnt += 40
                self.cnt_value.emit(self.cnt)

            elif self.cnt == 50 :
                chrome_driver.find_element_by_id('memo_' + self.subject_no).send_keys(self.comment)
                self.cnt += 10
                self.cnt_value.emit(self.cnt)

            elif self.cnt == 40 :
                chrome_driver.find_element_by_name('password').send_keys(self.pw)
                self.cnt += 10
                self.cnt_value.emit(self.cnt)

            elif self.cnt == 30 :
                chrome_driver.find_element_by_name('name').send_keys(self.id)
                self.cnt += 10
                self.cnt_value.emit(self.cnt)

            elif self.cnt == 20 :
                target_url = 'http://gall.dcinside.com/board/view/?id=' + self.gallery_id + '&no=' + self.subject_no
                print(target_url)
                chrome_driver.get(target_url)
                self.cnt += 10
                self.cnt_value.emit(self.cnt)

            elif self.cnt == 10 :
                chrome_driver = webdriver.Chrome(Chromdriver_Path, chrome_options=options)
                #chrome_driver = webdriver.Chrome(Chromdriver_Path)     # 헤드리스 모드 비사용시
                self.cnt += 10
                self.cnt_value.emit(self.cnt)

            elif self.cnt == 0 :
                # 크롬 웹드라이버 헤드리스 모드 사용을 위한 옵션
                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                options.add_argument('window-size=1920x1080')
                options.add_argument("disable-gpu")
                self.cnt += 10
                self.cnt_value.emit(self.cnt)

            self.msleep(100)
            self.mutex.unlock()





