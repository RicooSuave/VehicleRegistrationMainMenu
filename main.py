from PyQt5.QtWidgets import *
from PyQt5 import uic
class TestGui(QMainWindow):

    def __init__(self):
        super(TestGui, self).__init__()
        uic.loadUi("testgui.ui", self)
        self.show()

        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(lambda: self.sayit(self.textEdit.toPlainText()))
        self.actionClose.triggered.connect(exit)

    def login(self):
        if self.lineEdit_2.text() == "admin" and self.lineEdit.text() == "pass":
            self.textEdit.setEnabled(True)
            self.pushButton_2.setEnabled(True)
        else:
            message = QMessageBox()
            message.setText("Invalid Login")
            message.exec_()
    def sayit(self,msg):
        message = QMessageBox()
        message.setText(msg)
        message.exec()


def main():
    app = QApplication([])
    window = TestGui()
    app.exec_()



if __name__ == '__main__':
    main()
