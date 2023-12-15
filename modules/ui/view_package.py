from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel,QStandardItem

import os
from modules.ui.view_cache import CacheView

def PackageCacheView(widget):#package file(cache)
    cacheFolder_list=os.listdir('./result/cache')
    for cacheFolder in cacheFolder_list:
        file_path=os.path.join('cache',cacheFolder)
        tab=QtWidgets.QWidget()
        tab.setStyleSheet('background-color:white;')
        CacheView(tab,file_path)
        widget.viewWidget.addTab(tab, cacheFolder)


def SharedPrefsView(widget):#package file(shared_prefs)
    sharedPrefs_list=os.listdir('./result/shared_prefs')
    for sharedPrefs in sharedPrefs_list:
        tab=QtWidgets.QWidget()
        tab.setStyleSheet('''background-color:white;''')
        tabLayout=QtWidgets.QVBoxLayout(tab)

        DataCountLabel=QtWidgets.QLabel(tab)
        scrollArea=QtWidgets.QScrollArea(tab)#내용이 화면 밖을 넘어가면 자동으로 scroll 생김


        scrollArea.setWidgetResizable(True)
        scrollAreaWidgetContents=QtWidgets.QWidget()
        scrollArea.setStyleSheet('border:none;')
        listLayout=QtWidgets.QGridLayout(scrollAreaWidgetContents)
        listLayout.setContentsMargins(15, 15, 15, 15)

        sharedPrefsList=QtWidgets.QListView(scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(15)
        sharedPrefsList.setFont(font)
        sharedPrefsList.setStyleSheet('''QListView{
                                      border:2px solid rgb(235,235,235);}
                                      QListView::item{
                                      border-bottom:2px solid rgb(235,235,235);
                                      padding:15px;
                                      }
                                      QListView::item:hover{
                                        background-color:rgb(242,242,242);
                                        color:balck;
                                      }
                                      QListView::item:focus{
                                      background-color:rgb(242,242,242);
                                      color:balck;
                                      border:none;
                                      }''')


        model=QStandardItemModel()

        file_path=os.path.join('./result/shared_prefs',sharedPrefs)
        with open(file_path,'r',encoding='utf-8') as file:
            wiping_data=file.read()
            data_list=wiping_data.split('\n\n')
        for data in data_list:
            model.appendRow(QStandardItem(data))
        sharedPrefsList.setModel(model)
        sharedPrefsList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        listLayout.addWidget(sharedPrefsList)
        DataCountLabel.setText(f'발견된 흔적 개수: {len(data_list)}')
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(13)
        DataCountLabel.setFont(font)
        DataCountLabel.setStyleSheet("background-color:rgb(255,255,255);\n"
"border:none;\n"
"border-bottom:1px solid rgb(177,177,177);"
"padding:9px\n")
        tabLayout.addWidget(DataCountLabel)
        scrollArea.setWidget(scrollAreaWidgetContents)
        tabLayout.addWidget(scrollArea)
        tabLayout.setStretch(0,1)
        tabLayout.setStretch(1,15)
        tab_name=sharedPrefs.split('.txt')[0]
        widget.viewWidget.addTab(tab, tab_name)
