from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from modules.ui.HTMLwidget import HTMLwidget

import pandas as pd
import os
from modules.ui.TableView import TableView
from modules.ui.view_cache import CacheView
def ClipboardView(widget):

    tab_1 = QtWidgets.QWidget()#clipboard
    tab_1.setStyleSheet('''background-color:rgb(255,255,255);''')
    tab_1.setObjectName("tab_1")
    if os.path.exists('./result/clipboard/clipboard.csv'):
        TableView(tab_1,'./result/clipboard/clipboard.csv')
    else:
        clipboardLayout = QtWidgets.QVBoxLayout(tab_1)
        clipboardLayout.setObjectName("htmlLayout")
        clipboardData=open('./result/clipboard/clipboard.txt','r')
        clipboardCountLabel = QtWidgets.QLabel(tab_1)
        clipboardCountLabel.setObjectName("htmlCountLabel")
        clipboardCountLabel.setText(f"발견된 clipboard 흔적 개수: {len(clipboardData.readlines())}")
        clipboardCountLabel.setStyleSheet("background-color:rgb(255,255,255);\n"
    "border:none;\n"
    "border-bottom:1px solid rgb(177,177,177);"
    "padding:9px\n")
        
        font = QtGui.QFont()
        font.setFamily("맑은 고딕 Semilight")
        font.setPointSize(11)
        clipboardCountLabel.setFont(font)

        clipboardLayout.addWidget(clipboardCountLabel)
        clipboardScrollArea = QtWidgets.QScrollArea(tab_1)#스크롤 위젯 생성(내용이 넘어가면 자동으로 스크롤 생성해줌)
        clipboardScrollArea.setWidgetResizable(True)
        clipboardScrollArea.setObjectName("clipboardScrollArea")
        clipboardScrollArea.setStyleSheet('border:none;')

        clipboardScrollContents = QtWidgets.QWidget()
        clipboardScrollContents.setGeometry(QtCore.QRect(0, 0, 1036, 631))
        clipboardScrollContents.setObjectName("clipboardScrollContents")

        clipboardBoxLayout = QtWidgets.QVBoxLayout(clipboardScrollContents)
        clipboardBoxLayout.setObjectName("clipboardBoxLayout")
        with open('./result/clipboard/clipboard.txt','r',encoding='utf-8') as file:
            clipboardWidget=HTMLwidget(' ',file.read())
        clipboardBoxLayout.addWidget(clipboardWidget)


        clipboardScrollArea.setWidget(clipboardScrollContents)
        clipboardLayout.addWidget(clipboardScrollArea)
        clipboardLayout.setStretch(0, 1)
        clipboardLayout.setStretch(1, 15)

    widget.viewWidget.addTab(tab_1, "Clipboard")

    tab_2 = QtWidgets.QWidget()#image
    tab_2.setStyleSheet('''background-color:rgb(255,255,255);
                        margin:10px;
                        margin-top:0px;''')
    tab_2.setObjectName("tab_2")
    CacheView(tab_2,'clipboard/image')
    widget.viewWidget.addTab(tab_2, "Image")


    tab_3 = QtWidgets.QWidget()#html
    tab_3.setStyleSheet('''background-color:rgb(255,255,255);''')
    tab_3.setObjectName("tab_3")
    htmlLayout = QtWidgets.QVBoxLayout(tab_3)
    htmlLayout.setObjectName("htmlLayout")
    html_list=os.listdir('./result/clipboard/html')
    htmlCountLabel = QtWidgets.QLabel(tab_3)
    htmlCountLabel.setObjectName("htmlCountLabel")
    htmlCountLabel.setText(f"발견된 html 흔적 개수: {len(html_list)}")
    htmlCountLabel.setStyleSheet("background-color:rgb(255,255,255);\n"
"border:none;\n"
"border-bottom:1px solid rgb(177,177,177);"
"padding:9px\n")
    
    font = QtGui.QFont()
    font.setFamily("맑은 고딕 Semilight")
    font.setPointSize(11)
    htmlCountLabel.setFont(font)

    htmlLayout.addWidget(htmlCountLabel)
    htmlScrollArea = QtWidgets.QScrollArea(tab_3)#스크롤 위젯 생성(내용이 넘어가면 자동으로 스크롤 생성해줌)
    htmlScrollArea.setWidgetResizable(True)
    htmlScrollArea.setObjectName("htmlScrollArea")
    htmlScrollArea.setStyleSheet('border:none;')

    htmlScrollContents = QtWidgets.QWidget()
    htmlScrollContents.setGeometry(QtCore.QRect(0, 0, 1036, 631))
    htmlScrollContents.setObjectName("htmlScrollContents")

    htmlBoxLayout = QtWidgets.QVBoxLayout(htmlScrollContents)
    htmlBoxLayout.setObjectName("htmlBoxLayout")
    for file_name in html_list:
        file_path=os.path.join('./result/clipboard/html',file_name)
        html_date=file_name.split(".")[0]
        with open(file_path,'r',encoding='utf-8') as file:
                html_clipboardData=file.read()
                html_widget=HTMLwidget(html_date,html_clipboardData)
                htmlBoxLayout.addWidget(html_widget)

    htmlScrollArea.setWidget(htmlScrollContents)
    htmlLayout.addWidget(htmlScrollArea)
    htmlLayout.setStretch(0, 1)
    htmlLayout.setStretch(1, 15)
    widget.viewWidget.addTab(tab_3, "HTML")