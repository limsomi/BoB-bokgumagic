from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from modules.ui.Image import LoadImage 
from PyQt5.QtCore import Qt
import os

def CacheView(widget,file_path):#gallery cache, clipboard image,package file(cache)
        DataCountLabel = QtWidgets.QLabel(widget)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕 Semilight")
        font.setPointSize(11)
        DataCountLabel.setFont(font)
        DataCountLabel.setStyleSheet("background-color:rgb(255,255,255);\n"
"border:none;\n"
"border-bottom:1px solid rgb(177,177,177);"
"padding:9px\n")
        DataCountLabel.setObjectName("DataCountLabel")  

        DataWidget=QtWidgets.QWidget(widget)
        DataCount=LoadImage(DataWidget,file_path)

        DataCountLabel.setText(f'발견된 흔적 개수: {DataCount}')

        viewDataLayout=QtWidgets.QVBoxLayout(widget)
        viewDataLayout.addWidget(DataCountLabel)
        viewDataLayout.addWidget(DataWidget)
        viewDataLayout.setStretch(0,1)
        viewDataLayout.setStretch(1,15)
        viewDataLayout.setSpacing(1)


