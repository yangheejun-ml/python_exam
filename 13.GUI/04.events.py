from PyQt5 import QtWidgets

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("이벤트 테스트")
        self.statusBar = self.statusBar()
        self.setMouseTracking(True)
        self.setGeometry(300, 300, 300, 200)
        self.show()
    
    def keyPressEvent(self, e):
        output = "키 눌림 <key: {}>".format(e.key())
        self.statusBar.showMessage(output)
    
    def keyReleaseEvent(self, e):
        output = "키 띔 <key: {}>".format(e.key())
        self.statusBar.showMessage(output)
    
    def mouseDoubleClickEvent(self, e):
        button = e.button()
        x = e.x()
        y = e.y()
        gx = e.globalX()
        gy = e.globalY()
        output = "마우스 더블클릭 <버튼: {}, x={}, y={}, gx={}, gy={}>".format(button, x, y, gx, gy)
        self.statusBar.showMessage(output)
    
    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()
        gx = e.globalX()
        gy = e.globalY()
        output = "마우스 이동 <x={}, y={}, gx={}, gy={}>".format(x, y, gx, gy)
        self.statusBar.showMessage(output)

app = QtWidgets.QApplication([])
ex = MyApp()
app.exec_()