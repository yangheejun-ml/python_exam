from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import win32gui
import win32ui
import win32con
import cv2
import numpy as np
import time
import colorsys

LABEL_LIST = ["현재색(F5)", "보색", "저장A(F2)", "저장B(F3)", "A+B 혼합", "3x3평균", "HSV"]

def captureWindow(x=0, y=0, width=0, height=0):
    hwin = win32gui.GetDesktopWindow()
    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (x, y), win32con.SRCCOPY)
    sigIntArray = bmp.GetBitmapBits(True)
    img = np.fromstring(sigIntArray, dtype="uint8")
    img.shape = (height, width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    

class MyPicker(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.zoom = 1
        self.pause = False
        self.saveBGR = [(-1, -1, -1), (-1, -1, -1)]
        self.title = "파이피커"
        self.setWindowTitle(self.title)
        self.setFixedSize(300, 500)
        self.main_widget = QtWidgets.QWidget()
        self.createWidgets()
        self.setCentralWidget(self.main_widget)

        self.worker = Worker()
        self.worker.sig_update.connect(self.updateWindow)
        self.worker.start()
        self.show()
    
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F2:
            self.saveBGR[0] = self.currentBGR
        elif e.key() == QtCore.Qt.Key_F3:
            self.saveBGR[1] = self.currentBGR
        elif e.key() == QtCore.Qt.Key_F5:
            self.pause = not self.pause
        elif e.key() == QtCore.Qt.Key_F7:
            self.zoom += 1
        elif e.key() == QtCore.Qt.Key_F8:
            self.zoom -= 1
            if self.zoom < 1: self.zoom = 1

    @QtCore.pyqtSlot(tuple)
    def updateWindow(self, pt):
        x, y = pt
        print(x, y)

        if self.pause:
            return True

        width = self.viewer.width()
        height = self.viewer.height()
        
        center_x = int(width / 2)
        center_y = int(height / 2)

        x -= center_x
        y -= center_y

        if x < 0: x = 0
        if y < 0: y = 0
        
        display = []
        capture = captureWindow(x=x, y=y, width=width, height=height)

        if self.zoom > 1:
            print(self.zoom)
            zoom_image = self.resize(capture, width=self.zoom * capture.shape[1])
            if zoom_image is not None:
                center = int(zoom_image.shape[0] / 2), int(zoom_image.shape[1] / 2)
                # 이미지 크롭 [y1:y2, x1:x2]
                capture = zoom_image[center[0] - center_y:center[0] + center_y, center[1] - center_x:center[1] + center_x]

        capture = cv2.cvtColor(capture, cv2.COLOR_RGB2BGR)
        bgr = capture[center_y, center_x]
        self.currentBGR = (bgr[0], bgr[1], bgr[2])

        hsv = colorsys.rgb_to_hsv(bgr[2]/255, bgr[1]/255, bgr[0]/255)
        hsv_angle = (int(hsv[0] * 360), int(hsv[1] * 100), int(hsv[2] * 100))

        bgr_inverse = self.get_inverse_color(bgr)

        out_code, text_color, bg_color = self.get_code(bgr)
        out_inverse, text_color_inverse, bg_color_inverse = self.get_code(bgr_inverse)

        out_hsv = "{}˚ {}% {}%".format(hsv_angle[0], hsv_angle[1], hsv_angle[2])

        aR = aG = aB = 0
        for i in range(center_y - 1, center_y + 2):
            for j in range(center_x - 1, center_x + 2):
                p = capture[i, j]
                aR += p[2]
                aG += p[1]
                aB += p[0]
        aR = abs(int(aR / 9))
        aG = abs(int(aG / 9))
        aB = abs(int(aB / 9))

        out_3x3, text_color_3x3, bg_color_3x3 = self.get_code((aB, aG, aR))

        out_save1 = out_save2 = out_mix = ""
        text_color_save1 = text_color_save2 = text_color_mix = "#000000"
        bg_color_save1 = bg_color_save2 = bg_color_mix = "#FFFFFF"

        if self.saveBGR[0][0] >= 0:
            out_save1, text_color_save1, bg_color_save1 = self.get_code(self.saveBGR[0])
        if self.saveBGR[1][0] >= 0:
            out_save2, text_color_save2, bg_color_save2 = self.get_code(self.saveBGR[1])
        
        if self.saveBGR[0][0] >= 0 and self.saveBGR[1][0] >= 0:
            nR = self.saveBGR[0][2] + (int((self.saveBGR[1][2] - self.saveBGR[0][2]) / 2) * 1)
            nG = self.saveBGR[0][1] + (int((self.saveBGR[1][1] - self.saveBGR[0][1]) / 2) * 1)
            nB = self.saveBGR[0][0] + (int((self.saveBGR[1][0] - self.saveBGR[0][0]) / 2) * 1)
            out_mix, text_color_mix, bg_color_mix = self.get_code((nB, nG, nR))

        display.append((out_code, text_color, bg_color))
        display.append((out_inverse, text_color_inverse, bg_color_inverse))
        display.append((out_save1, text_color_save1, bg_color_save1))
        display.append((out_save2, text_color_save2, bg_color_save2))
        display.append((out_mix, text_color_mix, bg_color_mix))
        display.append((out_3x3, text_color_3x3, bg_color_3x3))
        display.append((out_hsv, "#FFFFFF", "#000000"))

        for i, c in enumerate(self.colors):
            text, text_color, bgcolor = display[i]
            style = "background-color:" + bgcolor + "; color:" + text_color
            c.setText(text)
            c.setStyleSheet(style)

        step = int(width / 10)
        cv2.line(capture, (center_x - step, center_y), (center_x + step, center_y), (255, 255, 255), 1)
        cv2.line(capture, (center_x, center_y - step), (center_x, center_y + step), (255, 255, 255), 1)

        qImage = QtGui.QImage(capture.data, width, height, 3 * width, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImage)
        self.viewer.setPixmap(pixmap)

    def resize(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        if width is None and height is None:
            return None
        dim = None
        (h, w) = image.shape[:2]
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))
        
        resized = cv2.resize(image, dim, interpolation=inter)
        return resized

    def get_code(self, bgr):
        inverse = self.get_inverse_color(bgr)
        current_text = self.comboBox.currentText()
        out_text = ""
        if current_text == "HTML":
            out_text = "#%02x%02x%02x" %(bgr[2], bgr[1], bgr[0])
        elif current_text == "RGB":
            out_text = "{},{},{}".format(bgr[2], bgr[1], bgr[0])
        
        bg_color = "#%02x%02x%02x" %(bgr[2], bgr[1], bgr[0])
        text_color = "#%02x%02x%02x" %(inverse[2], inverse[1], inverse[0])
        return (out_text, text_color, bg_color)

    def get_inverse_color(self, bgr):
        return (abs(255-bgr[0]), abs(255-bgr[1]), abs(255-bgr[2]))

    def createWidgets(self):
        self.labelStyle = "padding:1px; font-size:13px; font-family:맑은 고딕;"
        self.editStyle = "padding:1px; font-size:13px; font-family:맑은 고딕; border:1px solid #000000"

        vbox = QtWidgets.QVBoxLayout()
        self.viewer = QtWidgets.QLabel()
        self.viewer.setBaseSize(300, 300)
        self.viewer.setText("이미지창")
        self.viewer.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        vbox.addWidget(self.viewer)

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(3)

        self.labels = []
        self.colors = []

        for i, l in enumerate(LABEL_LIST):
            label = QtWidgets.QLabel(l)
            label.setStyleSheet(self.labelStyle)
            label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

            color = QtWidgets.QLineEdit()
            color.setStyleSheet(self.editStyle)
            color.setReadOnly(True)

            grid.addWidget(label, i + 1, 0)
            grid.addWidget(color, i + 1, 1)

            self.labels.append(label)
            self.colors.append(color)

        label = QtWidgets.QLabel("코드형식")
        label.setStyleSheet(self.labelStyle)
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.addItem("HTML")
        self.comboBox.addItem("RGB")
        self.comboBox.setStyleSheet("padding:3px;")
        grid.addWidget(label, len(LABEL_LIST) + 1, 0)
        grid.addWidget(self.comboBox, len(LABEL_LIST) + 1, 1)

        vbox.addLayout(grid)
        self.main_widget.setLayout(vbox)

class Worker(QtCore.QThread):
    sig_update = QtCore.pyqtSignal(tuple)

    def __init__(self):
        super(Worker, self).__init__()
    
    def run(self):
        while True:
            pt = win32gui.GetCursorPos()
            self.sig_update.emit(pt)
            time.sleep(0.1)

app = QtWidgets.QApplication([])
picker = MyPicker()
app.exec_()