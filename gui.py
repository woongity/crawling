import sys
import StoreFarmCrawling
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QInputDialog


class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        email = QLineEdit(self)
        email.move(20, 50)

        password = QLineEdit(self)
        password.move(20, 100)

        log_in_btn=QPushButton('로그인',self)
        try:
            log_in_btn.clicked.connect(self.log_in)
        except:
            print("로그인에 실패하였습니다")

        self.setWindowTitle('QLineEdit')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def log_in(self,email,password):

