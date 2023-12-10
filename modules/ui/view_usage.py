from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import*
from PyQt5 import uic
import pandas as pd
from modules.data_processing import usage
from modules.data_processing import viewData
from modules.ui import view_data
from modules.ui import ProcessBar
from modules.data_processing.viewData import viewData_Thread
from modules.data_processing.usage import Usage_Thread
class Usage_Window(QMainWindow):
        def __init__(self):
                super().__init__()
                self.android_version=None
                self.modelname=None
                self.wiping_aplication=None
                self.setupUi()
        def setupUi(self):
                self.setObjectName("self")
                self.resize(1400, 800)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/icon/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.setWindowIcon(icon)
                self.setStyleSheet("background-color:rgb(235, 235, 235);\n"
                "")


                self.centralwidget = QtWidgets.QWidget(self)
                self.centralwidget.setStyleSheet("background-color:rgb(235, 235, 235);")
                self.centralwidget.setObjectName("centralwidget")
                self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
                self.horizontalLayout.setObjectName("horizontalLayout")
                self.SiderLayout = QtWidgets.QVBoxLayout()
                self.SiderLayout.setSpacing(0)
                self.SiderLayout.setObjectName("siderlayout")
                osWidget = QtWidgets.QWidget(self.centralwidget)
                osWidget.setObjectName("widget")
                self.osWidgetLayout = QtWidgets.QVBoxLayout(osWidget)
                self.osWidgetLayout.setContentsMargins(0, 0, 0, 0)
                self.osWidgetLayout.setSpacing(0)
                self.osWidgetLayout.setObjectName("verticalLayout_2")
                self.os_information_header = QtWidgets.QLabel(osWidget)
                self.os_information_header.setStyleSheet("background-color:rgb(242, 242, 242);\n"
                "border:1px solid rgb(217,217,217);\n"
                "padding:10px;")
                self.os_information_header.setObjectName("os_information_header")
                self.osWidgetLayout.addWidget(self.os_information_header)
                self.OSinformation_listView = QtWidgets.QListView(osWidget)
                self.OSinformation_listView.setObjectName("OSinformation_listView")
                font = QtGui.QFont()
                font.setFamily("맑은 고딕 Semilight")
                font.setPointSize(11)
                font.setBold(True)
                font.setWeight(75)
                self.OSinformation_listView.setFont(font)
                self.osWidgetLayout.addWidget(self.OSinformation_listView)
                self.osWidgetLayout.setStretch(0, 1)
                self.osWidgetLayout.setStretch(1, 13)
                self.SiderLayout.addWidget(osWidget)
                self.extract_button = QtWidgets.QWidget(self.centralwidget)
                self.extract_button.setStyleSheet("background-color:rgb(242, 242, 242);\n"
                "border-style: solid;\n"
                "border-width: 1px;\n"
                "border-color:rgb(217,217,217);")
                self.extract_button.setObjectName("extract_button")
                self.verticalLayout = QtWidgets.QVBoxLayout(self.extract_button)
                self.verticalLayout.setSpacing(9)
                self.verticalLayout.setObjectName("verticalLayout")
                self.ViewDataButton = QtWidgets.QHBoxLayout()
                self.ViewDataButton.setObjectName("ViewDataButton")
                spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.ViewDataButton.addItem(spacerItem)
                self.V_Button = QtWidgets.QPushButton(self.extract_button)
                font = QtGui.QFont()
                font.setFamily("맑은 고딕 Semilight")
                font.setPointSize(15)
                font.setBold(True)
                font.setWeight(75)
                self.V_Button.setFont(font)
                self.V_Button.setStyleSheet("background-color:rgb(217,217,217);\n"
                "padding:15px;")
                self.V_Button.setObjectName("V_Button")
                self.V_Button.clicked.connect(lambda:self.Progressbar_exec(viewData_Thread(self.android_version,self.modelname,self.wiping_aplication),self.viewData_exec,'잔여 데이터 분석 중....'))
                self.ViewDataButton.addWidget(self.V_Button)
                spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.ViewDataButton.addItem(spacerItem1)
                self.ViewDataButton.setStretch(0, 2)
                self.ViewDataButton.setStretch(1, 1)
                self.ViewDataButton.setStretch(2, 2)
                self.UsageButton = QtWidgets.QHBoxLayout()
                self.UsageButton.setObjectName("UsageButton")
                spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.UsageButton.addItem(spacerItem2)
                self.U_Button = QtWidgets.QPushButton(self.extract_button)
                font = QtGui.QFont()
                font.setFamily("맑은 고딕 Semilight")
                font.setPointSize(15)
                font.setBold(True)
                font.setWeight(75)
                self.U_Button.setFont(font)
                self.U_Button.setStyleSheet("background-color:rgb(217,217,217);\n"
                "padding:15px;")
                self.U_Button.setObjectName("U_Button")
                self.U_Button.clicked.connect(lambda:self.Progressbar_exec(Usage_Thread(),self.AnalyzeUsagesStats,'UsageStats 분석 중....'))
                self.UsageButton.addWidget(self.U_Button)
                spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.UsageButton.addItem(spacerItem3)
                self.UsageButton.setStretch(0, 2)
                self.UsageButton.setStretch(1, 1)
                self.UsageButton.setStretch(2, 2)
                self.verticalLayout.addLayout(self.UsageButton)
                self.verticalLayout.addLayout(self.ViewDataButton)
                self.SiderLayout.addWidget(self.extract_button)
                self.SiderLayout.setStretch(0, 4)
                self.SiderLayout.setStretch(1, 2)
                self.SiderLayout.setContentsMargins(3, 3, 3, 3)
                self.horizontalLayout.addLayout(self.SiderLayout)
                self.rightLayout = QtWidgets.QVBoxLayout()
                self.rightLayout.setContentsMargins(0, 0, 0, 0)
                self.rightLayout.setObjectName("rightLayout")
                self.applicationWidget = QtWidgets.QWidget(self.centralwidget)
                self.applicationWidget.setObjectName("applicationWidget")
                self.applicationLayout = QtWidgets.QVBoxLayout(self.applicationWidget)
                self.applicationLayout.setSpacing(0)
                self.applicationLayout.setObjectName("applicationLayout")
                self.application_header = QtWidgets.QLabel(self.applicationWidget)
                self.application_header.setStyleSheet("background-color:rgb(242, 242, 242);\n"
                "border:1px solid rgb(217,217,217);\n"
                "padding:10px;")
                self.application_header.setObjectName("application_header")
                self.applicationLayout.addWidget(self.application_header)
                self.application_listView = QtWidgets.QListView(self.applicationWidget)
                self.OSinformation_listView.setStyleSheet('''
                                QListView{
                                background-color:rgb(255,255,255);
                                border:1px solid rgb(217,217,217);
                                                          
                                }             ''')
                self.application_listView.setStyleSheet('''background-color:rgb(255, 255, 255);
                                                        border:1px solid rgb(217,217,217);''')
                self.application_listView.setObjectName("application_listView")
                self.application_listView.clicked.connect(self.setTableUsageData)
                self.applicationLayout.addWidget(self.application_listView)
                self.applicationLayout.setStretch(0, 1)
                self.applicationLayout.setStretch(1, 15)
                self.rightLayout.addWidget(self.applicationWidget)
                self.UsageTab = QtWidgets.QTabWidget(self.centralwidget)
                font = QtGui.QFont()
                font.setFamily("맑은 고딕 Semilight")
                font.setPointSize(11)
                font.setBold(True)
                font.setWeight(75)
                self.UsageTab.setFont(font)
                self.UsageTab.setObjectName("UsageTab")

                self.Packages = QtWidgets.QWidget()
                self.Packages.setObjectName("Packages")
                self.Packages.setStyleSheet('''background-color:rgb(255,255,255);
                                            border:none;''')
                self.gridLayout = QtWidgets.QGridLayout(self.Packages)
                self.gridLayout.setObjectName("gridLayout")
                self.PackageList = QtWidgets.QListView(self.Packages)
                self.PackageList.setObjectName("PackageList")
                self.gridLayout.addWidget(self.PackageList, 0, 0, 1, 1)
                self.UsageTab.addTab(self.Packages, "Packages")

                self.EventLog = QtWidgets.QWidget()
                self.EventLog.setStyleSheet('''background-color:rgb(255,255,255);
                                            border:none;''')
                self.EventLog.setObjectName("EventLog")
                self.EventLogTabLayout=QtWidgets.QGridLayout(self.EventLog)
                self.EventLogTable=QtWidgets.QTableView(self.EventLog)
                self.EventLogTabLayout.addWidget(self.EventLogTable, 0, 0, 1, 1)
                self.UsageTab.addTab(self.EventLog, "EventLog")


                self.rightLayout.addWidget(self.UsageTab)
                self.horizontalLayout.addLayout(self.rightLayout)
                self.horizontalLayout.setStretch(0, 5)
                self.horizontalLayout.setStretch(1, 17)
                self.setCentralWidget(self.centralwidget)
                self.statusbar = QtWidgets.QStatusBar(self)
                self.statusbar.setObjectName("statusbar")
                self.setStatusBar(self.statusbar)
                self.retranslateUi()
                self.UsageTab.setCurrentIndex(0)
                QtCore.QMetaObject.connectSlotsByName(self)

        def retranslateUi(self):
                _translate = QtCore.QCoreApplication.translate
                self.setWindowTitle(_translate("self", "Second_page"))
                self.os_information_header.setText(_translate("self", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">OS 정보</span></p></body></html>"))
                self.V_Button.setText(_translate("self", "잔여데이터 분석"))
                self.U_Button.setText(_translate("self", "UsageStats 분석"))
                self.application_header.setText(_translate("self", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">발견된 File Wiping App</span></p></body></html>"))
        def Progressbar_exec(self,thread,exec_function,widgetTitle):
                self.ProgressWindow=ProcessBar.Process(self,thread,exec_function,widgetTitle)
        def AnalyzeUsagesStats(self,android_version, modelname, wiping_check, wiping_application):
                self.android_version=android_version
                self.modelname=modelname
                self.wiping_aplication=wiping_application

                list=[f"안드로이드 버전: {self.android_version}",f"모델명: {self.modelname}"]
                if wiping_check==False:
                        model=QStandardItemModel()
                        for x in list:
                                model.appendRow(QStandardItem(x))
                        self.OSinformation_listView.setModel(model)
                        self.OSinformation_listView.setStyleSheet('''
                                                QListView{
                                                background-color:rgb(255,255,255);
                                                border:1px solid rgb(217,217,217);
                                                }
                                                QListView::item{
                                                background-color:white;
                                                padding:20px;
                                                }                 ''')
                        self.setTableApplicationData()
                else:
                        print("경고문")
                        exit(0)
                        # 표시창 띄우기(수정필요)
                
        def setTableApplicationData(self):
                application_model=QStandardItemModel()
                for application_name in self.wiping_aplication:
                        application_model.appendRow(QStandardItem(application_name))
                self.application_listView.setModel(application_model)
                self.application_listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                self.application_listView.setStyleSheet('''
                                        QListView::item{
                                        padding:15px;
                                        border-bottom: 1px solid rgb(217,217,217);
                                        }
                                        QListView::item:hover{
                                        background-color:rgb(242,242,242);
                                        }
                                        QListView::item:focus{
                                        background-color:rgb(242,242,242);
                                        color:black;
                                        }
                                        QListView{
                                        background-color:rgb(255,255,255);
                                        border:1px solid rgb(217,217,217);
                                        }''')
                font = QtGui.QFont()
                font.setPointSize(11)
                self.application_listView.setFont(font)

        def setTableUsageData(self,index):
                ind=index.row()
                packages=pd.read_csv('./result/Package.csv')
                row=packages.iloc[ind]
                UsagePackage_model=QStandardItemModel()

                for column_name, value in row.items():
                        UsagePackage_model.appendRow(QStandardItem(f"{column_name}: {value}"))
                self.PackageList.setModel(UsagePackage_model)
                self.PackageList.setSpacing(10)
                
                font = QtGui.QFont()
                font.setPointSize(11)
                self.PackageList.setFont(font)
                self.PackageList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                event_log=pd.read_csv('./result/EventLog.csv')


                event_log['group'] = (event_log['package'] != event_log['package'].shift(1)).cumsum()

                eventlog_grouped = event_log.groupby('group')
                group = eventlog_grouped.get_group(ind+1)
                group = group.copy()
                group.drop(columns = ['package','type','group'],inplace=True)
                header=group.columns.tolist()
                event_log_model = QStandardItemModel()
                event_log_model.setHorizontalHeaderLabels(header)

                for row_num, row_data in enumerate(group.itertuples(index=False, name=None)):
                        event_log_model.appendRow([QStandardItem(str(item)) for item in row_data])

                self.EventLogTable.setModel(event_log_model)
                self.EventLogTable.resizeColumnsToContents()
                self.EventLogTable.horizontalHeader().setCascadingSectionResizes(False)
                self.EventLogTable.horizontalHeader().setStretchLastSection(True)
                self.EventLogTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        def viewData_exec(self):
                self.SecondWindow = view_data.ViewData(self)
                self.SecondWindow.show()
                self.hide()
