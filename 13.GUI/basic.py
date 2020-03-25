from PyQt5 import QtWidgets
import sys

class MyWindows(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("파이썬GUI")
        self.resize(400, 300)
        self.show()

app = QtWidgets.QApplication([])
win = MyWindows()
sys.exit(app.exec_())
