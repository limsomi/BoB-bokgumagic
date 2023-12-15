from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout,QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,QSize,QEvent
from PyQt5 import QtCore, QtGui, QtWidgets
from modules.ui.Image import deviceImage
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
class osWidget(QWidget):
    def __init__(self,width,height):
            super().__init__()
            self.setUi(width,height)
    def setUi(self,width,height):

        self.osWidgetLayout = QtWidgets.QVBoxLayout(self)#os 정보 layout
        self.osWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.osWidgetLayout.setSpacing(0)
    

        self.versionLabel=QtWidgets.QLabel()
        self.nameLabel=QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Text Semibold")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.versionLabel.setFont(font)
        ont = QtGui.QFont()
        font.setFamily("Segoe UI Variable Text Semibold")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.nameLabel.setFont(font)
        self.versionLabel.setStyleSheet('padding:15px 15px 7px 15px;')
        self.nameLabel.setStyleSheet('padding:8px 15px 15px 15px;')

        self.osWidgetLayout.addWidget(self.versionLabel)
        self.osWidgetLayout.addWidget(self.nameLabel)

        self.deviceImageWidget=deviceImage(width,height)

        self.osWidgetLayout.addWidget(self.deviceImageWidget)

        self.osWidgetLayout.setStretch(0,1)
        self.osWidgetLayout.setStretch(1,1)
        self.osWidgetLayout.setStretch(2,6)
        self.setLayout(self.osWidgetLayout)
