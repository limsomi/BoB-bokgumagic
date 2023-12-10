from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout,QHBoxLayout
from PyQt5.QtCore import Qt,QSize
from PyQt5 import QtGui,QtWidgets

class HTMLwidget(QWidget):#html object
    def __init__(self, html_date, html_data):
        super().__init__()

        # 이미지 로드
        self.html_date = html_date
        self.html_data = html_data
        

        # 위젯 초기화
        self.init_ui()

    def init_ui(self):
        self.html_browser=QtWidgets.QTextBrowser()
        self.html_browser.setStyleSheet('''background-color:rgb(242,242,242);
                                        border:none''')
        self.html_label=QLabel(self.html_date)#html clipboard 시간
        font = QtGui.QFont()
        font.setFamily("맑은 고딕 Semilight")
        font.setPointSize(11)
        self.html_label.setFont(font)
        self.html_browser.setText(self.html_data)

        layout=QVBoxLayout(self)
        layout.addWidget(self.html_label)
        layout.addWidget(self.html_browser)
        self.setLayout(layout)
    
