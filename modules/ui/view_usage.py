from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
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

class CustomTitleBar(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CustomTitleBar, self).__init__(parent)
        self.setFixedHeight(38)  # Title bar height
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 0)  # Margin: top, left, bottom, right
        self.layout.setSpacing(0)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)  # Center items in the title bar

        # App Icon
        self.iconLabel = QtWidgets.QLabel(self)
        icon = QtGui.QPixmap('./logo_Bokgumagic.png').scaled(24, 24, QtCore.Qt.KeepAspectRatio)
        self.iconLabel.setPixmap(icon)
        self.layout.addWidget(self.iconLabel, alignment=QtCore.Qt.AlignLeft)

        # Title Label
        self.titleLabel = QtWidgets.QLabel(" Bokgumagic_v2.0                                                                                                                                                                                                                                              ", self)
        self.titleLabel.setFont(QtGui.QFont("맑은 고딕", 12))
        self.layout.addWidget(self.titleLabel, alignment=QtCore.Qt.AlignLeft)
        
        # Spacing between title and buttons
        self.layout.addStretch()

        # Minimize Button
        self.minimizeButton = QtWidgets.QPushButton("__", self)
        self.minimizeButton.setFixedSize(45, 30)
        self.layout.addWidget(self.minimizeButton, alignment=QtCore.Qt.AlignRight)

        # Maximize/Restore Button
        self.maximizeButton = QtWidgets.QPushButton("□", self)
        self.maximizeButton.setFixedSize(45, 30)
        self.layout.addWidget(self.maximizeButton, alignment=QtCore.Qt.AlignRight)

        # Close Button
        self.closeButton = QtWidgets.QPushButton("X", self)
        self.closeButton.setFixedSize(45, 30)
        self.layout.addWidget(self.closeButton, alignment=QtCore.Qt.AlignRight)

        # Set the background color for the title bar and buttons
        self.setStyleSheet("""
            CustomTitleBar, QLabel, QPushButton {
                background-color: rgb(224, 255, 255);
                border: none;
            }
            QPushButton:hover {
                background-color: rgb(200, 240, 240);
            }
            QPushButton:pressed {
                background-color: rgb(180, 230, 230);
            }
        """)

        # Connect button signals to their respective slots
        self.minimizeButton.clicked.connect(parent.showMinimized)
        self.maximizeButton.clicked.connect(self.toggleMaximizeRestore)
        self.closeButton.clicked.connect(parent.close)

    def toggleMaximizeRestore(self):
        # Toggle maximize/restore on button click
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximizeButton.setText("□")
        else:
            self.parent().showMaximized()
            self.maximizeButton.setText("❐")

class Usage_Window(QMainWindow):
        def __init__(self):
                super().__init__()
                self.android_version=None
                self.modelname=None
                self.wiping_aplication=None
                self.duplicated_application=None
                self.setupUi()
        def setupUi(self):
                self.setObjectName("self")
                self.resize(1400, 800)
                #Bokgumagik_logo
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("./logo_Bokgumagic.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.setWindowIcon(icon)


                # 기본 제목 표시줄 숨기기
                self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
                # 사용자 지정 제목 표시줄 추가
                self.customTitleBar = CustomTitleBar(self)
                self.setMenuWidget(self.customTitleBar)

                self.centralwidget = QtWidgets.QWidget(self)
                self.centralwidget.setStyleSheet("background-color:rgb(235, 235, 235);")
                self.centralwidget.setObjectName("centralwidget")
                
                self.centralLayout = QtWidgets.QHBoxLayout(self.centralwidget)#usage 전체 페이지 layout
                self.centralLayout.setObjectName("centralLayout")

                self.SiderLayout = QtWidgets.QVBoxLayout()#side bar layout
                self.SiderLayout.setSpacing(0)
                self.SiderLayout.setObjectName("siderlayout")

                osWidget = QtWidgets.QWidget(self.centralwidget)#os 정보 header + os 정보 data
                osWidget.setObjectName("widget")

                self.osWidgetLayout = QtWidgets.QVBoxLayout(osWidget)#os 정보 layout
                self.osWidgetLayout.setContentsMargins(0, 0, 0, 0)
                self.osWidgetLayout.setSpacing(0)
                self.osWidgetLayout.setObjectName("extractButtonLayout_2")

                self.os_information_header = QtWidgets.QLabel(osWidget)
                self.os_information_header.setStyleSheet("background-color:rgb(242, 242, 242);\n"#os 정보 header style
                "border:1px solid rgb(217,217,217);\n"
                "padding:10px;")
                self.os_information_header.setObjectName("os_information_header")

                self.osWidgetLayout.addWidget(self.os_information_header)

                self.OSinformation_listView = QtWidgets.QListView(osWidget)#os 정보 데이터 widget
                self.OSinformation_listView.setObjectName("OSinformation_listView")
                font = QtGui.QFont()
                font.setFamily("맑은 고딕 Semilight")
                font.setPointSize(11)
                font.setBold(True)
                font.setWeight(75)
                self.OSinformation_listView.setFont(font)
                
                #OSinformation_listView의 style은 AnalyzeUsagesStats 함수에도 있음
                self.OSinformation_listView.setStyleSheet('''
                                QListView{
                                background-color:rgb(255,255,255);
                                border:1px solid rgb(217,217,217);
                                                          
                                }             ''')
                self.osWidgetLayout.addWidget(self.OSinformation_listView)
                self.osWidgetLayout.setStretch(0, 1)
                self.osWidgetLayout.setStretch(1, 13)

                self.SiderLayout.addWidget(osWidget)
                self.extractButton = QtWidgets.QWidget(self.centralwidget)#usagestats 분석, 잔여 데이터 분석 버튼 모음
                self.extractButton.setStyleSheet("background-color:rgb(242, 242, 242);\n"
                "border-style: solid;\n"
                "border-width: 1px;\n"
                "border-color:rgb(217,217,217);")
                self.extractButton.setObjectName("extractButton")

                self.extractButtonLayout = QtWidgets.QVBoxLayout(self.extractButton)#usagestats 분석, 잔여 데이터 분석 버튼 모음 layout
                self.extractButtonLayout.setSpacing(9)
                self.extractButtonLayout.setObjectName("extractButtonLayout")

                self.ViewDataButton = QtWidgets.QHBoxLayout()#잔여 데이터 분석 버튼 layout(이건 extract button 안에서 간격두기 위해 만들어둠)
                self.ViewDataButton.setObjectName("ViewDataButton")
                spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.ViewDataButton.addItem(spacerItem)

                self.V_Button = QtWidgets.QPushButton(self.extractButton)#잔여 데이터 분석 버튼
                font = QtGui.QFont()
                font.setFamily("맑은 고딕 Semilight")
                font.setPointSize(15)
                font.setBold(True)
                font.setWeight(75)
                self.V_Button.setFont(font)
                self.V_Button.setStyleSheet("background-color:rgb(217,217,217);\n"
                "padding:15px;")
                self.V_Button.setObjectName("V_Button")
                #잔여 데이터 분석 버튼 누르면 progressbar로 thread를 생성해 viewData_Thread(viewData.py) 실행 : progresssbar 디자인은 Progressbar 참고
                self.V_Button.clicked.connect(lambda:self.Progressbar_exec(viewData_Thread(self.android_version,self.modelname,self.wiping_aplication),self.viewData_exec,'잔여 데이터 분석 중....'))
                self.ViewDataButton.addWidget(self.V_Button)
                spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.ViewDataButton.addItem(spacerItem1)
                self.ViewDataButton.setStretch(0, 2)
                self.ViewDataButton.setStretch(1, 1)
                self.ViewDataButton.setStretch(2, 2)

                self.UsageButton = QtWidgets.QHBoxLayout()#usagestats 버튼 layout(이건 extract button 안에서 간격두기 위해 만들어둠)
                self.UsageButton.setObjectName("UsageButton")
                spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.UsageButton.addItem(spacerItem2)

                self.U_Button = QtWidgets.QPushButton(self.extractButton)#usagestats 버튼
                font = QtGui.QFont()
                font.setFamily("맑은 고딕 Semilight")
                font.setPointSize(15)
                font.setBold(True)
                font.setWeight(75)
                self.U_Button.setFont(font)
                self.U_Button.setStyleSheet("background-color:rgb(217,217,217);\n"
                "padding:15px;")
                self.U_Button.setObjectName("U_Button")
                #usagestats 버튼 누르면 progressbar가 뜨면서 Usage_Thread(usage.py) 실행
                self.U_Button.clicked.connect(lambda:self.Progressbar_exec(Usage_Thread(),self.AnalyzeUsagesStats,'UsageStats 분석 중....'))
                self.UsageButton.addWidget(self.U_Button)
                spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.UsageButton.addItem(spacerItem3)
                self.UsageButton.setStretch(0, 2)
                self.UsageButton.setStretch(1, 1)
                self.UsageButton.setStretch(2, 2)

                self.extractButtonLayout.addLayout(self.UsageButton)
                self.extractButtonLayout.addLayout(self.ViewDataButton)

                self.SiderLayout.addWidget(self.extractButton)
                self.SiderLayout.setStretch(0, 4)
                self.SiderLayout.setStretch(1, 2)
                self.SiderLayout.setContentsMargins(3, 3, 3, 3)

                self.centralLayout.addLayout(self.SiderLayout)

                #usagestats 정보 보여주는 오른쪽 widget layout
                self.rightLayout = QtWidgets.QVBoxLayout()
                self.rightLayout.setContentsMargins(0, 0, 0, 0)
                self.rightLayout.setObjectName("rightLayout")

                #발견된 File Wiping App widget
                self.applicationWidget = QtWidgets.QWidget(self.centralwidget)
                self.applicationWidget.setObjectName("applicationWidget")

                #발견된 File Wiping App layout
                self.applicationLayout = QtWidgets.QVBoxLayout(self.applicationWidget)
                self.applicationLayout.setSpacing(0)#이건 layout 안에 component 간격 조절
                self.applicationLayout.setObjectName("applicationLayout")
                self.application_header = QtWidgets.QLabel(self.applicationWidget)#file wiping app header
                self.application_header.setStyleSheet("background-color:rgb(242, 242, 242);\n"# 발견된 File Wiping app 정보 header style
                "border:1px solid rgb(217,217,217);\n"
                "padding:10px;")
                self.application_header.setObjectName("application_header")
                self.applicationLayout.addWidget(self.application_header)

                #applicationWidget의 file wipnig app 나열
                self.application_listView = QtWidgets.QListView(self.applicationWidget)
                #setTableApplicationData 에도 style 있음
                self.application_listView.setStyleSheet('''background-color:rgb(255, 255, 255);
                                                        border:1px solid rgb(217,217,217);''')#발견된 file wipng app 정보 데이터 부분 style
                self.application_listView.setObjectName("application_listView")
                self.application_listView.clicked.connect(self.setTableUsageData)# 클릭 시 package, eventlog 보여주기
                self.applicationLayout.addWidget(self.application_listView)
                self.applicationLayout.setStretch(0, 1)
                self.applicationLayout.setStretch(1, 15)
                self.rightLayout.addWidget(self.applicationWidget)
                #package, eventlog tabWidget
                self.UsageTab = QtWidgets.QTabWidget(self.centralwidget)
                font = QtGui.QFont()
                font.setFamily("맑은 고딕 Semilight")
                font.setPointSize(11)
                font.setBold(True)
                font.setWeight(75)
                self.UsageTab.setFont(font)
                self.UsageTab.setObjectName("UsageTab")

                self.Packages = QtWidgets.QWidget()#package tab
                self.Packages.setObjectName("Packages")
                self.Packages.setStyleSheet('''background-color:rgb(255,255,255);
                                            border:none;''')#package tab style
                #Package tab layout
                self.PackageLayout = QtWidgets.QGridLayout(self.Packages)
                self.PackageLayout.setObjectName("gridLayout")
                self.PackageList = QtWidgets.QListView(self.Packages)
                self.PackageList.setObjectName("PackageList")
                self.PackageLayout.addWidget(self.PackageList, 0, 0, 1, 1)
                self.UsageTab.addTab(self.Packages, "Packages")

                self.EventLog = QtWidgets.QWidget()#event log tab
                self.EventLog.setStyleSheet('''background-color:rgb(255,255,255);
                                            border:none;''')#eventlog tab style
                self.EventLog.setObjectName("EventLog")
                #eventlog tab layout
                self.EventLogTabLayout=QtWidgets.QGridLayout(self.EventLog)
                self.EventLogTable=QtWidgets.QTableView(self.EventLog)
                self.EventLogTabLayout.addWidget(self.EventLogTable, 0, 0, 1, 1)
                self.UsageTab.addTab(self.EventLog, "EventLog")


                self.rightLayout.addWidget(self.UsageTab)
                self.centralLayout.addLayout(self.rightLayout)
                self.centralLayout.setStretch(0, 5)
                self.centralLayout.setStretch(1, 17)
                self.setCentralWidget(self.centralwidget)
                self.statusbar = QtWidgets.QStatusBar(self)
                self.statusbar.setObjectName("statusbar")
                self.setStatusBar(self.statusbar)
                self.retranslateUi()
                self.UsageTab.setCurrentIndex(0)
                QtCore.QMetaObject.connectSlotsByName(self)

        def retranslateUi(self):
                _translate = QtCore.QCoreApplication.translate
                self.setWindowTitle(_translate("self", "Bokgumagic_v2.0"))
                self.os_information_header.setText(_translate("self", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">OS 정보</span></p></body></html>"))
                self.V_Button.setText(_translate("self", "잔여데이터 분석"))
                self.U_Button.setText(_translate("self", "UsageStats 분석"))
                self.application_header.setText(_translate("self", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">발견된 File Wiping App</span></p></body></html>"))
        
        def Progressbar_exec(self,thread,exec_function,widgetTitle):#progress bar 실행
                self.ProgressWindow=ProcessBar.Process(self,thread,exec_function,widgetTitle)#progressWindow 객체 생성

        def AnalyzeUsagesStats(self,android_version, modelname, wiping_check, wiping_application,duplicated_application):#usagestats listview,os 정보 띄우기
                self.android_version=android_version
                self.modelname=modelname
                self.wiping_aplication=wiping_application
                self.duplicated_application=duplicated_application

                list=[f"안드로이드 버전: {self.android_version}",f"모델명: {self.modelname}"]
                if wiping_check == False:
                        model = QStandardItemModel()

                        # 아이콘 크기 및 패딩 설정
                        icon_size = 256  # 아이콘의 크기를 256x256으로 설정
                        padding = 20  # 여백 크기를 20으로 설정

                        # QPixmap을 사용하여 아이콘의 크기 조절
                        icon_pixmap = QtGui.QPixmap("./logo_galaxy.png").scaled(icon_size, icon_size, QtCore.Qt.KeepAspectRatio)
                        icon_item = QStandardItem()
                        icon_item.setIcon(QtGui.QIcon(icon_pixmap))

                        # 아이콘이 포함된 행의 크기를 조절 (아이콘 크기 + 패딩)
                        icon_item.setSizeHint(QtCore.QSize(icon_size + padding * 2, icon_size + padding * 2))  # 여백을 추가하여 행의 높이와 너비 설정

                        model.appendRow(icon_item)

                        # QListView에 모델 설정
                        self.OSinformation_listView.setModel(model)
                        self.OSinformation_listView.setIconSize(QtCore.QSize(icon_size, icon_size))  # 아이콘 크기 설정

                         # QListView의 아이템 간격 설정
                        self.OSinformation_listView.setSpacing(padding)

                        # QListView의 여백 설정
                        self.OSinformation_listView.setContentsMargins(padding, padding, padding, padding)

                        # 여기에 추가적인 텍스트 아이템 설정
                        for text in list:
                                model.appendRow(QStandardItem(text))
        
                        self.OSinformation_listView.setModel(model)
                        self.OSinformation_listView.setIconSize(QtCore.QSize(icon_size, icon_size))  # 아이콘 크기 설정
                        self.setTableApplicationData()# application 정보 출력 함수
                else:
                        print("경고문")
                        exit(0)
                        # 표시창 띄우기(수정필요)
                
        def setTableApplicationData(self):
                application_model=QStandardItemModel()
                for application_name in self.duplicated_application:
                        application_model.appendRow(QStandardItem(application_name))
                self.application_listView.setModel(application_model)
                self.application_listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                #application_listView style
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

                # event_log['group'] = (event_log['package'] != event_log['package'].shift(1)).cumsum()
                # none=event_log['package'].isna()
                # event_log=event_log[~none]
                # event_log['new_group'] = (event_log['group'] != event_log['group'].shift(1)).cumsum()
                # event_log.to_csv('./result/EventLog.csv')
                eventlog_grouped = event_log.groupby('new_group')

                group = eventlog_grouped.get_group(ind+1)
                group = group.copy()
                group.drop(columns = ['package','type','group','new_group'],inplace=True)
                header=group.columns.tolist()
                event_log_model = QStandardItemModel()
                event_log_model.setHorizontalHeaderLabels(header)

                for row_num, row_data in enumerate(group.itertuples(index=False, name=None)):
                        event_log_model.appendRow([QStandardItem(str(item)) for item in row_data])

                self.EventLogTable.setModel(event_log_model)#eventlog table
                #eventlog table column 길이 조절
                self.EventLogTable.resizeColumnsToContents()
                self.EventLogTable.horizontalHeader().setCascadingSectionResizes(False)
                self.EventLogTable.horizontalHeader().setStretchLastSection(True)
                self.EventLogTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        def viewData_exec(self):#viewData 화면 띄우기
                self.SecondWindow = view_data.ViewData(self)
                self.SecondWindow.show()
                self.hide()#지금 페이지 숨기기
