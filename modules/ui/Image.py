import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout,QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,QSize
from PyQt5 import QtCore, QtGui, QtWidgets
import os
class ImageWidget(QWidget):#이미지를 보여줄 때 이미지,이미지 파일 이름 포함된 object
    def __init__(self, image_path, image_name,image_area):
        super().__init__()


        self.image_path = image_path
        self.image_name = image_name
        self.area=image_area
        self.load_image()

        self.init_ui()

    def load_image(self):
        self.image = QPixmap(self.image_path)

    def init_ui(self):

        self.image_label = QLabel(self)
        self.image_label.setPixmap(self.image.scaled(QSize(80, 80),Qt.IgnoreAspectRatio))
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet('''QLabel{border:none;}
                                        ''')
        self.image_label.setFocusPolicy(Qt.StrongFocus)

        self.name_label = QLabel(self.image_name, self)
        self.name_label.setAlignment(Qt.AlignCenter)    
        self.name_label.setStyleSheet('''QLabel{border:none;}
                                        ''')
        self.name_label.setFocusPolicy(Qt.StrongFocus)


        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)
        layout.addWidget(self.name_label)
        layout.setStretch(0,2)
        layout.setStretch(1,1)
        self.setLayout(layout)
        self.setFixedSize(150, 150)
        self.setWindowTitle('Image Viewer')
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:#object 클릭시 이미지를 확대하여 출력
            view_image=QPixmap(self.image_path)
            self.area.setPixmap(view_image.scaled(QSize(1000,1000),Qt.KeepAspectRatio))
            self.area.setAlignment(Qt.AlignCenter)
            self.setStyleSheet('''QWidget:focus{background-color:rgb(242,242,242);}''')


def LoadImage(viewData,folder_name):#gallery, clipboard, pacakge file (cache) 화면
    horizontalLayout = QtWidgets.QHBoxLayout(viewData)
    horizontalLayout.setContentsMargins(3, 3, 3, 3)
    horizontalLayout.setSpacing(6)
    horizontalLayout.setObjectName("horizontalLayout")


    scrollArea = QtWidgets.QScrollArea(viewData)
    scrollArea.setWidgetResizable(True)
    scrollArea.setObjectName("scrollArea")


    Data = QtWidgets.QWidget()#이미지 나열 부분(왼쪽)
    Data.setStyleSheet("background-color:rgb(255,255,255);\n"
                            "border:2px solid rgb(177, 177, 177);")
    Data.setObjectName("Data")
    scrollArea.setWidget(Data)
    horizontalLayout.addWidget(scrollArea)
    Magnify = QtWidgets.QLabel(viewData)#이미지 확대 부분(오르쪽)
    Magnify.setStyleSheet("background-color:rgb(255,255,255);\n"
                            "border:2px solid rgb(177, 177, 177);")
    Magnify.setObjectName("Magnify")
    horizontalLayout.addWidget(Magnify)
    horizontalLayout.setSpacing(10)
    horizontalLayout.setStretch(0, 3)
    horizontalLayout.setStretch(1, 6)

    row, col = 0, 0
    gridLayout=QtWidgets.QGridLayout(Data)
    CacheList=os.listdir(f'./result/{folder_name}')
    for file_name in CacheList:#이미지 나열
            file_path=os.path.join(f'./result/{folder_name}',file_name)
            image_widget=ImageWidget(file_path,file_name,Magnify)
            gridLayout.addWidget(image_widget,row,col)
            col += 1
            if col == 2: 
                    col = 0
                    row += 1
    for i in range(gridLayout.rowCount()):
        gridLayout.setRowStretch(i, 1)
    for i in range(gridLayout.columnCount()):
        gridLayout.setColumnStretch(i, 1)

    return len(CacheList)