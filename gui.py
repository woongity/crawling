import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QInputDialog


class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.id=QLineEdit(self)
        self.id.move(30, 35)
        self.pass_word = QLineEdit(self)
        self.pass_word.move(30, 70)

        self.log_in_btn=QPushButton('로그인',self)

        self.log_in_btn.clicked.connect(self.showDialog)
        self.log_in_btn.move(200,35)
        self.log_in_btn.frameSize()
        self.setWindowTitle('Input dialog')
        self.setGeometry(300, 300, 300, 200)
        self.show()


    def showDialog(self):

        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')

        if ok:
            self.le.setText(str(text))
