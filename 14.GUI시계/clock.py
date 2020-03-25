from PyQt5 import QtWidgets
from PyQt5 import QtCore

class MyClock(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.mouseClick = False

        self.setWindowTitle("시계")
        self.initWidgets()
        self.setFixedSize(250, 100)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.show()
    
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

    def mousePressEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.mouseClick = True
            self.oldPos = e.globalPos()
            print(self.oldPos)

    def mouseReleaseEvent(self, e):
        self.mouseClick = False

    def mouseMoveEvent(self, e):
        if self.mouseClick:
            delta = QtCore.QPoint(e.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = e.globalPos()
            print(self.oldPos)


    def initWidgets(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.lcd = QtWidgets.QLCDNumber()
        self.lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd.setDigitCount(8)
        self.lcd.setFrameStyle(QtWidgets.QFrame.NoFrame)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)

        self.show_time()

        self.layout.addWidget(self.lcd)
        self.setLayout(self.layout)
    
    def show_time(self):
        time = QtCore.QTime.currentTime()
        self.currentTime = time.toString("hh:mm:ss")
        self.lcd.display(self.currentTime)

app = QtWidgets.QApplication([])
win = MyClock()
app.exec_()