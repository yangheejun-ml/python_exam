from PyQt5.QtWidgets import QMainWindow, QApplication, QToolButton, QSizePolicy, QLineEdit, QGridLayout, QLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

operator = ["+", "-", "*", "/", "="]

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "계산기"
        self.setWindowTitle(self.title)

        self.left = 100
        self.top = 200
        self.width = 300
        self.height = 200
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyCalculator()
        self.setCentralWidget(self.table_widget)

        self.show()

class Button(QToolButton):
    def __init__(self, text):
        super().__init__()
        buttonStyle = '''
        QToolButton:hover {border:1px solid #0078d7; background-color:#e5f1fb;}
        QToolButton:pressed {background-color:#a7c8e3}
        QToolButton {font-size:11pt; font-family:나눔고딕; border:1px solid #d6d7d8; background-color:#f0f1f1}
        '''
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)
        self.setStyleSheet(buttonStyle)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 30)
        size.setWidth(max(size.width(), size.height()))
        return size

class MyCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.waitingForOperand = True
        self.input_history = ""
        self.input_temporary = ""
        
        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(15)
        self.display.setStyleSheet("border:0px; font-size:20pt; font-family:나눔고딕;font-weight:bold; padding:10px")

        gridLayout = QGridLayout()
        gridLayout.setSizeConstraint(QLayout.SetFixedSize)

        self.clearButton = self.createButton("CE", self.clear)
        self.clearAllButton = self.createButton("C", self.clearAll)
        self.backButton = self.createButton("Back", self.backDelete)
        self.divButton = self.createButton("/", self.clickButtons)
        self.multiplyButton = self.createButton("*", self.clickButtons)
        self.minusButton = self.createButton("-", self.clickButtons)
        self.plusButton = self.createButton("+", self.clickButtons)
        self.equalButton = self.createButton("=", self.clickButtons)
        self.dotButton = self.createButton(".", self.clickButtons)
        self.reverseButton = self.createButton("R", self.reverse)

        gridLayout.addWidget(self.clearButton, 0, 0, 1, 1)
        gridLayout.addWidget(self.clearAllButton, 0, 1, 1, 1)
        gridLayout.addWidget(self.backButton, 0, 2, 1, 1)
        gridLayout.addWidget(self.divButton, 0, 3, 1, 1)
        gridLayout.addWidget(self.multiplyButton, 1, 3, 1, 1)
        gridLayout.addWidget(self.minusButton, 2, 3, 1, 1)
        gridLayout.addWidget(self.plusButton, 3, 3, 1, 1)
        gridLayout.addWidget(self.equalButton, 4, 3, 1, 1)
        gridLayout.addWidget(self.reverseButton, 4, 0, 1, 1)
        gridLayout.addWidget(self.dotButton, 4, 2, 1, 1)

        self.digitButtons = []
        for i in range(10):
            self.digitButtons.append(self.createButton(str(i), self.clickButtons))
        
        gridLayout.addWidget(self.digitButtons[0], 4, 1, 1, 1)

        for i in range(1, 10):
            row = int(((9 - i) / 3) + 1)
            col = ((i - 1) % 3)
            gridLayout.addWidget(self.digitButtons[i], row, col, 1, 1)

        layout = QVBoxLayout()
        layout.addWidget(self.display)
        layout.addLayout(gridLayout)
        self.setLayout(layout)
        self.setWindowTitle("계산기")
        self.setGeometry(300, 300, 300, 400)
    def clear(self):
        if self.waitingForOperand:
            return
        self.display.setText('0')
        self.input_temporary = ""
        self.waitingForOperand = True
    def clearAll(self):
        self.display.setText('0')
        self.input_temporary = ""
        self.input_history = ""
        self.waitingForOperand = True
    def backDelete(self):
        if self.waitingForOperand:
            return
        text = self.display.text()[:-1]
        self.input_temporary = text
        if not text:
            text = "0"
            self.input_temporary = ""
            self.waitingForOperand = True
        self.display.setText(text)
    def reverse(self):
        text = self.display.text()
        value = float(text)
        if value > 0.0:
            text = "-" + text
        elif value < 0.0:
            text = text[1:]
        self.display.setText(text)
        self.input_temporary = text

    def clickButtons(self):
        clickedButton = self.sender()
        digitValue = clickedButton.text()
        print(digitValue)
        self.processKeyValue(digitValue)

    def processKeyValue(self, digitValue):
        if digitValue == "=":
            if self.calculator():
                self.waitingForOperand = True
            pass
        elif digitValue == "+" or digitValue == "-" or digitValue == "*" or digitValue == "/":
            if self.waitingForOperand:
                self.replaceLastOperator(digitValue)
            else:
                self.inputHistory(digitValue)
                self.calculator()
            self.waitingForOperand = True
        elif digitValue == ".":
            if self.waitingForOperand:
                self.display.setText("0")
            if "." not in self.display.text():
                self.display.setText(self.display.text() + ".")
                self.inputHistory(str("."))
            self.waitingForOperand = False
        else:
            keyvalue = ord(digitValue)
            if keyvalue >= 48 and keyvalue <= 57:
                if self.display.text() == "0" and digitValue == "0.0":
                    return
                if self.waitingForOperand:
                    self.display.clear()
                    self.waitingForOperand = False
                self.display.setText(self.display.text() + digitValue)
                self.inputHistory(str(digitValue))

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Backspace:
            self.backDelete()
        elif e.key() == Qt.Key_Enter:
            self.processKeyValue("=")
        elif e.key() >= 47 and e.key() <= 57:
            self.processKeyValue(chr(e.key()))
        elif e.key() == 42 or e.key() == 43 or e.key() == 45 or e.key() == 46:
            self.processKeyValue(chr(e.key()))

    def string_calculator(self, user_input, show_history=False):
        string_list = []
        lop = 0

        if user_input[-1] not in operator:
            user_input += "="

        for i, s in enumerate(user_input):
            if s in operator:
                if user_input[lop:i].strip() != "":
                    string_list.append(user_input[lop:i])
                    string_list.append(s)
                    lop = i + 1

        string_list = string_list[:-1]
        pos = 0
        while True:
            if pos + 1 > len(string_list):
                break
            if len(string_list) > pos + 1 and string_list[pos] in operator:
                temp = string_list[pos-1] + string_list[pos] + string_list[pos + 1]
                del string_list[0:3]
                string_list.insert(0, str(eval(temp)))
                pos = 0

                if show_history:
                    print(string_list)
            pos += 1

        if len(string_list) > 0:
            result = float(string_list[0])

        return round(result, 4)
        
    def calculator(self):
        operator_check = False
        for i in self.input_history:
            if i in operator:
                operator_check = True
                break
        if not operator_check:
            return False
        else:
            self.input_history += self.input_temporary
            self.input_temporary = ""
            self.display.setText(str(self.string_calculator(self.input_history)))
        return True

    def inputHistory(self, value):
        digitValue = str(value)
        if digitValue in operator:
            if self.input_history[-1:] in operator:
                self.input_history += self.input_temporary + digitValue
            else:
                self.input_history = self.input_temporary + digitValue
            self.input_temporary = ""
        else:
            self.input_temporary += str(digitValue)

    def replaceLastOperator(self, value):
        self.input_history = self.input_history[:-1] + str(value)
    def createButton(self, text, function):
        button = Button(text)
        button.clicked.connect(function)
        return button

app = QApplication([])
calc = App()
app.exec_()