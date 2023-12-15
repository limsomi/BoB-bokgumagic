import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar,QDesktopWidget
from PyQt5 import QtCore, QtGui, QtWidgets
import os
class smallWindow(QWidget):
    def __init__(self,parent,windowTitle,label):
        super().__init__()
        self.parent=parent
        self.initUI(windowTitle,label)
    def initUI(self,windowTitle,label):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./resource/logo_Bokgumagic.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.setGeometry(0, 0, 500, 200)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setStyleSheet("padding:2px;\n"
"margin:10px;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem)
        self.checkButton = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(13)
        self.checkButton.setFont(font)
        self.checkButton.setStyleSheet("padding:10px;")
        self.checkButton.setObjectName("checkButton")
        self.checkButton.clicked.connect(self.check)
        self.horizontalLayout.addWidget(self.checkButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayout.setStretch(0,4)
        self.horizontalLayout.setStretch(1,3)
        self.horizontalLayout.setStretch(2,4)

        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.verticalLayout.setStretch(0, 4)
        self.verticalLayout.setStretch(1, 3)


        self.setWindowTitle(windowTitle)
        self.label.setText(label)
        self.checkButton.setText('확인')
        self.centerOnParent()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.show()
        

    def check(self):
        self.close()
    def centerOnParent(self):
        parent_screen = QApplication.desktop().screenGeometry(self.parent)
        child_frame = self.frameGeometry()
        child_frame.moveCenter(parent_screen.center())
        self.move(child_frame.topLeft())

