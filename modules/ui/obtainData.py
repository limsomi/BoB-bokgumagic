import sys
from PyQt5.QtWidgets import QApplication,QLabel, QWidget, QVBoxLayout, QPushButton, QProgressBar,QDesktopWidget
from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from modules.data_processing.usage import Usage_Thread

class ViewProgress(QWidget):
    def __init__(self):
        self.initUI()
    def initUI(self):

        self.progress=QProgressBar(self)
        self.progress.setGeometry(10,10,280,20)
        self.listWidget = QListWidget(self)

        # Add items with icons
        self.addItemWithIcon("Gallery Cache", "resource/gallery.png")
        self.addItemWithIcon("Clipboard", "resource/clipboard.png")
        self.addItemWithIcon("Contacts", "resource/contacts.png")
        self.addItemWithIcon("Package File (Cache)", "resource/package.png")
        self.addItemWithIcon("Package File (Shared Prefs)", "resource/package.png")


        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.progress)
        layout.addWidget(self.listWidget)
        self.setLayout(layout)
    def addItemWithIcon(self, text, icon_path):
        item = QListWidgetItem(text, self.listWidget)
        icon = QIcon(QPixmap(icon_path))
        item.setIcon(icon)