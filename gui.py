import sys
import StoreFarmCrawling
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QInputDialog


class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 이메일은 보이도록 설정
        self.email_input = QLineEdit(self)
        self.email_input.move(20, 50)

        # 비번은 안보이도록 설정
        self.password_input = QLineEdit(self)
        self.password_input.move(20, 100)

        self.log_in_btn = QPushButton('로그인', self)

        self.log_in_btn.setToolTip("로그인을 하려면 클릭하세요")

        self.log_in_btn.move(200, 100)
        self.setWindowTitle('크롤링')
        self.setGeometry(300, 300, 300, 200)
        self.show()

        try:
            self.log_in_btn.clicked.connect(self.log_in)
        except Exception as ex:
            print("로그인에 실패하였습니다", ex)
            exit()
    #      TODO: 로그인 실패여부를 확인하는 함수를 만들어야한다
    def log_in(self):
        email = self.email_input.text()
        password = self.password_input.text()
        try:
            StoreFarmCrawling.start_core_service(email, password)
        except Exception as ex:
            print("말이 안됌", ex)
            exit()