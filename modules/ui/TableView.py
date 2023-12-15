from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QWidget
from PyQt5.QtGui import QStandardItemModel,QStandardItem
import os
import pandas as pd
def TableView(widget,csv_path):#DataView에서 table module
    widgetLayout = QtWidgets.QVBoxLayout(widget)
    widgetLayout.setContentsMargins(3, 3, 3, 3)
    widgetLayout.setSpacing(1)
    widgetLayout.setObjectName("widgetLayout")

    DataCountLabel = QtWidgets.QLabel(widget)
    font = QtGui.QFont()
    font.setFamily("맑은 고딕")
    font.setPointSize(13)
    DataCountLabel.setFont(font)
    DataCountLabel.setStyleSheet("background-color:rgb(255,255,255);\n"
"border:none;\n"
"border-bottom:1px solid rgb(177,177,177);"
"padding:9px\n")
    DataCountLabel.setObjectName("DataCountLabel")  

    scrollArea = QtWidgets.QScrollArea(widget)
    scrollArea.setWidgetResizable(True)
    scrollArea.setObjectName("scrollArea")
    scrollArea.setStyleSheet('border:none;')
    scrollAreaWidgetContents = QtWidgets.QWidget()
    TextGridLayout = QtWidgets.QGridLayout(scrollAreaWidgetContents)
    # TextGridLayout.setContentsMargins(15, 15, 15, 15)
    # TextGridLayout.setSpacing(15)
    TextGridLayout.setObjectName("TextGridLayout")

    TextTable = QtWidgets.QTableView(scrollAreaWidgetContents)
    TextTable.setObjectName("TextTable")
    TextTable.setObjectName("TextTable")
    widgetLayout.addWidget(DataCountLabel)
    if os.path.exists(csv_path):
        df=pd.read_csv(csv_path)
        length=len(df)

        header=df.columns.tolist()
        df_model = QStandardItemModel()
        df_model.setHorizontalHeaderLabels(header)

        for index,row in df.iterrows():
            df_model.appendRow([QStandardItem(str(item)) for item in row])
        TextTable.setModel(df_model)

        TextTable.verticalHeader().setVisible(False)
        font = QtGui.QFont()
        font.setPointSize(13)
        TextTable.setFont(font)
        TextTable.horizontalHeader().setFont(font)
        TextTable.setStyleSheet("""                                                 
        QTableView::item {
                border: 1px solid black;  /* Set the border for each cell */
        }

        QHeaderView::section {
                background-color:rgb(69,71,75);
                color:white;
                border: 1px solid black;  /* Set the border for header sections */
        }
        """)
        TextTable.resizeColumnsToContents()
        TextTable.horizontalHeader().setCascadingSectionResizes(False)
        TextTable.horizontalHeader().setStretchLastSection(True)
        TextTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)


    else:
        length=0
    DataCountLabel.setText(f'발견된 흔적 개수: {length}')
    TextGridLayout.addWidget(TextTable, 0, 0, 1, 1)
    scrollArea.setWidget(scrollAreaWidgetContents)
    widgetLayout.addWidget(scrollArea)
    widgetLayout.setStretch(0, 1)
    widgetLayout.setStretch(1, 15)
    
