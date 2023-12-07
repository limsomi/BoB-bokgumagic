from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import *
import pandas as pd
import csv
class Usage_Window(object):
    def __init__(self,android_version,modelname, wipng_application):
        self.wiping_application=wipng_application
        self.android_version=android_version
        self.modelname=modelname
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 1000)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color:rgb(235, 235, 235);\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color:rgb(235, 235, 235);")
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.siderlayout = QtWidgets.QVBoxLayout()
        self.siderlayout.setSpacing(0)
        self.siderlayout.setObjectName("siderlayout")
        self.os_information_header = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕 Semilight")
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.os_information_header.setFont(font)
        self.os_information_header.setStyleSheet("background-color:rgb(242, 242, 242);\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-color:rgb(177,177,177);")
        self.os_information_header.setObjectName("os_information_header")
        self.siderlayout.addWidget(self.os_information_header)
        self.OSinformation_listView = QtWidgets.QListView(self.centralwidget)
        self.OSinformation_listView.setStyleSheet("background-color:rgb(255,255,255);")
        self.OSinformation_listView.setObjectName("OSinformation_listView")
        self.siderlayout.addWidget(self.OSinformation_listView)
        self.extract_button = QtWidgets.QWidget(self.centralwidget)
        self.extract_button.setStyleSheet("background-color:rgb(242, 242, 242);\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-color:rgb(177,177,177);")
        self.extract_button.setObjectName("extract_button")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.extract_button)
        self.verticalLayout.setObjectName("verticalLayout")
        self.message = QtWidgets.QLabel(self.extract_button)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.message.setFont(font)
        self.message.setStyleSheet("border: none;")
        self.message.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.message.setObjectName("message")
        self.verticalLayout.addWidget(self.message)
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setObjectName("button_layout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.button_layout.addItem(spacerItem)
        self.startButton = QtWidgets.QPushButton(self.extract_button)
        self.startButton.setStyleSheet("background-color:rgb(217,217,217);")
        self.startButton.setObjectName("startButton")
        self.button_layout.addWidget(self.startButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.button_layout.addItem(spacerItem1)
        self.button_layout.setStretch(0, 2)
        self.button_layout.setStretch(1, 3)
        self.button_layout.setStretch(2, 2)
        self.verticalLayout.addLayout(self.button_layout)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.siderlayout.addWidget(self.extract_button)
        self.siderlayout.setStretch(1, 5)
        self.siderlayout.setStretch(2, 2)
        self.horizontalLayout.addLayout(self.siderlayout)
        self.right_layout = QtWidgets.QVBoxLayout()
        self.right_layout.setContentsMargins(1, 1, 1, 1)
        self.right_layout.setSpacing(1)
        self.right_layout.setObjectName("right_layout")
        self.application_data = QtWidgets.QWidget(self.centralwidget)
        self.application_data.setObjectName("application_data")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.application_data)
        self.verticalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_3.setSpacing(1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.application_header = QtWidgets.QLabel(self.application_data)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕 Semilight")
        self.application_header.setFont(font)
        self.application_header.setStyleSheet("background-color:rgb(242, 242, 242);\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-color:rgb(177,177,177);")
        self.application_header.setObjectName("application_header")
        self.verticalLayout_3.addWidget(self.application_header)
        self.application_table = QtWidgets.QTableView(self.application_data)
        self.application_table.setStyleSheet("background-color:rgb(255,255,255);")
        self.application_table.setObjectName("application_table")
        self.application_table.horizontalHeader().setVisible(False)
        self.application_table.horizontalHeader().setCascadingSectionResizes(False)
        self.application_table.horizontalHeader().setStretchLastSection(True)
        self.application_table.clicked.connect(self.setTableUsageData)

        self.verticalLayout_3.addWidget(self.application_table)
        self.verticalLayout_3.setStretch(1, 4)
        self.right_layout.addWidget(self.application_data)
        self.view_data = QtWidgets.QWidget(self.centralwidget)
        self.view_data.setObjectName("view_data")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.view_data)
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_2.setSpacing(1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.view_header = QtWidgets.QLabel(self.view_data)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕 Semilight")
        self.view_header.setFont(font)
        self.view_header.setStyleSheet("background-color:rgb(242, 242, 242);\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-color:rgb(177,177,177);\n"
"")
        self.view_header.setObjectName("view_header")
        self.verticalLayout_2.addWidget(self.view_header)
        self.view_scroll = QtWidgets.QWidget(self.view_data)
        self.view_scroll.setObjectName("view_scroll")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.view_scroll)
        self.horizontalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.view = QtWidgets.QWidget(self.view_scroll)
        self.view.setObjectName("view")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.view)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.PackageLabel = QtWidgets.QLabel(self.view)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.PackageLabel.setFont(font)
        self.PackageLabel.setStyleSheet("background-color:rgb(255,255,255);\n"
"")
        self.PackageLabel.setObjectName("PackageLabel")
        self.verticalLayout_4.addWidget(self.PackageLabel)
        self.PackageList = QtWidgets.QListView(self.view)
        self.PackageList.setStyleSheet("background-color:rgb(255,255,255);")
        self.PackageList.setObjectName("listView")
        self.verticalLayout_4.addWidget(self.PackageList)
        self.EventLogLabel = QtWidgets.QLabel(self.view)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.EventLogLabel.setFont(font)
        self.EventLogLabel.setStyleSheet("background-color:rgb(255,255,255);")
        self.EventLogLabel.setObjectName("EventLogLabel")
        self.EventLogTable = QtWidgets.QTableView(self.view)
        self.EventLogTable.setStyleSheet("background-color:rgb(255,255,255);")
        self.EventLogTable.setObjectName("tableView")
        self.EventLogTable.horizontalHeader().setCascadingSectionResizes(False)
        self.EventLogTable.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_4.addWidget(self.EventLogLabel)
        self.verticalLayout_4.addWidget(self.EventLogTable)
        self.verticalLayout_4.setStretch(1, 3)
        self.verticalLayout_4.setStretch(3, 3)
        self.horizontalLayout_2.addWidget(self.view)
        self.verticalScrollBar = QtWidgets.QScrollBar(self.view_scroll)
        self.verticalScrollBar.setStyleSheet("background-color:rgb(242,242,242);\n"
"border:1px, solid;")
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.horizontalLayout_2.addWidget(self.verticalScrollBar)
        self.verticalLayout_2.addWidget(self.view_scroll)
        self.verticalLayout_2.setStretch(1, 4)
        self.right_layout.addWidget(self.view_data)
        self.right_layout.setStretch(0, 1)
        self.right_layout.setStretch(1, 1)
        self.horizontalLayout.addLayout(self.right_layout)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Second_page"))
        self.os_information_header.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">OS 정보</span></p></body></html>"))
        self.message.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; vertical-align:super;\">[잔여데이터 분석]</span></p><p align=\"center\"><span style=\" font-weight:600; vertical-align:super;\">갤러리 캐시, 클립보드, 연락처</span></p><p align=\"center\"><span style=\" font-weight:600; vertical-align:super;\">패키지 파일 캐시</span></p><p align=\"center\"><span style=\" font-weight:600; vertical-align:super;\">보고서 추출 및 분석</span></p></body></html>"))
        self.startButton.setText(_translate("MainWindow", "시  작"))
        self.application_header.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">발견된 File Wiping App</span></p></body></html>"))
        self.view_header.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">View Details</span></p></body></html>"))
        self.PackageLabel.setText(_translate("MainWindow", " Package"))
        self.EventLogLabel.setText(_translate("MainWindow", " EventLog"))
        self.setTableApplicationData()

        list=[f"안드로이드 버전: {self.android_version}",f"모델명: {self.modelname}"]
        model=QStandardItemModel()
        for x in list:
            model.appendRow(QStandardItem(x))
        self.OSinformation_listView.setModel(model)

    def setTableApplicationData(self):
        # wiping_aplication=['com.projectstar.ishredder.android.standard','com.cbinnovations.androideraser',
        #                   'com.palmtronix.shreddit.v1','com.zerdava.fileshredder','com.vb2labs.android.sdelete',
        #                   'com.projectstar.ishredder.android.standard','com.palmtronix.shreddit.v1','com.shredder.fileshredder.securewipe',
        #                   'com.projectstar.ishredder.android.standard']
        application_model=QStandardItemModel()
        for application_name in self.wiping_application:
           application_model.appendRow(QStandardItem(application_name))
        self.application_table.setModel(application_model)

    def setTableUsageData(self,index):
        ind=index.row()
        packages=pd.read_csv('./result/Package.csv')
        row=packages.iloc[ind]
        UsagePackage_model=QStandardItemModel()

        for column_name, value in row.items():
            UsagePackage_model.appendRow(QStandardItem(f"{column_name}: {value}"))
        self.PackageList.setModel(UsagePackage_model)

        event_log=pd.read_csv('./result/EventLog.csv')


        event_log['group'] = (event_log['package'] != event_log['package'].shift(1)).cumsum()

        eventlog_grouped = event_log.groupby('group')
        group = eventlog_grouped.get_group(ind+1)
        
        header=event_log.columns.tolist()
        event_log_model = QStandardItemModel()
        event_log_model.setHorizontalHeaderLabels(header)

        for row_num, row_data in enumerate(group.itertuples(index=False, name=None)):
            event_log_model.appendRow([QStandardItem(str(item)) for item in row_data])

        self.EventLogTable.setModel(event_log_model)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Usage_Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
