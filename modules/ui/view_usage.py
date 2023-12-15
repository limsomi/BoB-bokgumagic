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
from modules.ui.Image import deviceImage
from modules.ui.osWidget import osWidget
from modules.ui.WindowWidget import smallWindow
from modules.data_processing import adb_extract
import os


class Usage_Window(QMainWindow):
        def __init__(self):
                super().__init__()
                self.android_version=None
                self.modelname=None
                self.wiping_aplication=None
                self.duplicated_application=None
                self.usageCheck=False
                self.setupUi()
        def setupUi(self):
                self.setObjectName("self")
                self.resize(1800, 1400)
                #Bokgumagik_logo
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("./resource/logo_Bokgumagic.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.setWindowIcon(icon)



                # # 기본 제목 표시줄 숨기기
                # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
                # # 사용자 지정 제목 표시줄 추가
                # self.customTitleBar = CustomTitleBar(self)
                # self.setMenuWidget(self.customTitleBar)

                self.centralwidget = QtWidgets.QWidget(self)
                self.centralwidget.setStyleSheet("background-color:rgb(242, 242, 242);")
                self.centralwidget.setObjectName("centralwidget")
                
                self.centralLayout = QtWidgets.QHBoxLayout(self.centralwidget)#usage 전체 페이지 layout
                self.centralLayout.setObjectName("centralLayout")

                self.SideLayout = QtWidgets.QVBoxLayout()#side bar layout
                self.SideLayout.setSpacing(0)
                self.SideLayout.setObjectName("SideLayout")
                self.SideLayout.setContentsMargins(0,0,0,0)
                self.logoWidget=deviceImage(250,200)
                self.logoWidget.update_Image('./resource/logo.png')
                self.SideLayout.addWidget(self.logoWidget)

                self.extractButtonLayout = QtWidgets.QHBoxLayout()#usagestats 분석, 잔여 데이터 분석 버튼 모음 layout
                self.extractButtonLayout.setSpacing(10)
                self.extractButtonLayout.setObjectName("extractButtonLayout")
                self.extractButtonLayout.setContentsMargins(0,0,0,0)
                spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.extractButtonLayout.addItem(spacerItem)

                self.V_Button = QtWidgets.QPushButton("잔여 데이터 분석")#잔여 데이터 분석 버튼
                font = QtGui.QFont()
                font.setFamily("맑은 고딕")
                font.setPointSize(15)
                font.setBold(True)
                font.setWeight(75)
                self.V_Button.setFont(font)
                self.V_Button.setStyleSheet('''QPushButton{background-color:rgb(100, 204, 197);
                                            color:white;
                                            padding:15px;
                                            border:2px solid rgb(100, 204, 197);
                                            border-radius:10px;}
                                        QPushButton:hover{
                                            background-color:rgb(69,71,75);
                                            border:2px solid rgb(69,71,75);
                                            color:white;
                                            padding:15px;
                                        }
                                        ''')   
                self.V_Button.setObjectName("V_Button")
                #잔여 데이터 분석 버튼 누르면 progressbar로 thread를 생성해 viewData_Thread(viewData.py) 실행 : progresssbar 디자인은 Progressbar 참고
                self.V_Button.clicked.connect(lambda:self.Progressbar_exec(viewData_Thread(self.android_version,self.modelname,self.wiping_aplication),self.viewData_exec,'잔여 데이터 분석 중....'))


                self.U_Button = QtWidgets.QPushButton('File Wiping 실행 흔적 분석')#usagestats 버튼
                font = QtGui.QFont()
                font.setFamily("맑은 고딕")
                font.setPointSize(15)
                font.setBold(True)
                font.setWeight(75)
                self.U_Button.setFont(font)
                self.U_Button.setStyleSheet('''QPushButton{background-color:rgb(100, 204, 197);
                                            color:white;
                                            padding:15px;
                                            border:2px solid rgb(100, 204, 197);
                                            border-radius:10px;}
                                        QPushButton:hover{
                                            background-color:rgb(69,71,75);
                                            border:2px solid rgb(69,71,75);
                                            color:white;
                                            padding:15px;
                                        }
                                        ''')     
                self.U_Button.setObjectName("U_Button")
                #usagestats 버튼 누르면 progressbar가 뜨면서 Usage_Thread(usage.py) 실행
                self.U_Button.clicked.connect(lambda:self.Progressbar_exec(Usage_Thread(),self.AnalyzeUsagesStats,'UsageStats 분석 중....'))
     

                self.extractButtonLayout.addWidget(self.U_Button)
                self.extractButtonLayout.addWidget(self.V_Button)
                self.extractButtonLayout.setStretch(0,5)
                self.extractButtonLayout.setStretch(1,2)
                self.extractButtonLayout.setStretch(2,2)

                self.osWidget=osWidget(500,700)
                self.osWidget.setStyleSheet('background-color:white;')
                self.setStyleSheet('background-color:white;')
                effect = QGraphicsDropShadowEffect()
                effect.setOffset(0, 0)
                effect.setBlurRadius(15)
                self.osWidget.setGraphicsEffect(effect)
                self.SideLayout.addWidget(self.osWidget)


                self.SideLayout.setStretch(0, 2)
                self.SideLayout.setStretch(1, 6)

                self.SideLayout.setSpacing(30)
                self.SideLayout.setContentsMargins(30, 15, 10, 15)
                
                self.centralLayout.addLayout(self.SideLayout)

                #usagestats 정보 보여주는 오른쪽 widget layout
                self.rightLayout = QtWidgets.QVBoxLayout()
                self.rightLayout.setContentsMargins(40, 10, 30, 15)
                self.rightLayout.setObjectName("rightLayout")
                self.rightLayout.setSpacing(30)
                self.rightLayout.addLayout(self.extractButtonLayout)
                #발견된 File Wiping App widget
                self.applicationWidget = QtWidgets.QWidget(self.centralwidget)
                self.applicationWidget.setObjectName("applicationWidget")
                #발견된 File Wiping App layout
                self.applicationLayout = QtWidgets.QVBoxLayout()
                self.applicationLayout.setContentsMargins(0,0,0,0)
                self.applicationLayout.setSpacing(0)#이건 layout 안에 component 간격 조절
                self.applicationLayout.setObjectName("applicationLayout")
                self.application_header = QtWidgets.QLabel('발견된 File Wiping Application')#file wiping app header
                font = QtGui.QFont()
                font.setFamily("맑은 고딕")
                font.setPointSize(15)
                font.setBold(True)
                font.setWeight(75)
                self.application_header.setFont(font)
                self.application_header.setStyleSheet("background-color:rgb(69,71,75);\n"# 발견된 File Wiping app 정보 header style
                "color:white;"
                "border:1px solid rgb(217,217,217);\n"
                "padding:10px;")
                self.application_header.setObjectName("application_header")
                self.applicationLayout.addWidget(self.application_header)

                self.application_listView = QtWidgets.QListView()
                self.application_listView.setStyleSheet('''background-color:rgb(255, 255, 255);
                                                        border:1px solid rgb(217,217,217);''')#발견된 file wipng app 정보 데이터 부분 style
                self.application_listView.setObjectName("application_listView")
                
                font = QtGui.QFont()
                font.setPointSize(15)
                self.application_listView.setFont(font)
                self.application_listView.clicked.connect(self.setTableUsageData)# 클릭 시 package, eventlog 보여주기
                self.applicationLayout.addWidget(self.application_listView)
                self.applicationLayout.setStretch(0, 1)
                self.applicationLayout.setStretch(1, 13)
                self.applicationWidget.setLayout(self.applicationLayout)

                effect = QGraphicsDropShadowEffect()
                effect.setOffset(0, 0)
                effect.setBlurRadius(15)
                self.applicationWidget.setGraphicsEffect(effect)


                self.rightLayout.addWidget(self.applicationWidget)
                #package, eventlog tabWidget
                self.UsageTab = QtWidgets.QTabWidget(self.centralwidget)

                effect = QGraphicsDropShadowEffect()
                effect.setOffset(0, 0)
                effect.setBlurRadius(15)
                self.UsageTab.setGraphicsEffect(effect)
                self.UsageTab.setStyleSheet('''
                                QTabBar::tab:selected { 
                                background: rgb(100, 204, 197); 
                                }
                                QTabBar::tab {
                                background: lightgray; 
                                color:white;
                                } 
                                ''')
                font = QtGui.QFont()
                font.setFamily("맑은 고딕")
                font.setPointSize(15)
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
                font = QtGui.QFont()
                font.setPointSize(15)
                self.PackageList.setFont(font)
                self.PackageLayout.addWidget(self.PackageList, 0, 0, 1, 1)
                self.UsageTab.addTab(self.Packages, "Packages")

                self.EventLog = QtWidgets.QWidget()#event log tab
                self.EventLog.setStyleSheet('''background-color:rgb(255,255,255);
                                            border:none;''')#eventlog tab style
                self.EventLog.setObjectName("EventLog")
                #eventlog tab layout
                self.EventLogTabLayout=QtWidgets.QGridLayout(self.EventLog)
                self.EventLogTable=QtWidgets.QTableView(self.EventLog)
                font = QtGui.QFont()
                font.setPointSize(13)
                self.EventLogTable.setFont(font)
                self.EventLogTable.horizontalHeader().setFont(font)  # 수평 헤더의 글꼴 크기 설정
                self.EventLogTabLayout.addWidget(self.EventLogTable, 0, 0, 1, 1)
                self.UsageTab.addTab(self.EventLog, "EventLog")


                self.rightLayout.addWidget(self.UsageTab)
                self.rightLayout.setStretch(0,1)
                self.rightLayout.setStretch(1,5)
                self.rightLayout.setStretch(2,5)
                self.centralLayout.addLayout(self.rightLayout)
                self.centralLayout.setStretch(0, 5)
                self.centralLayout.setStretch(1, 17)
                self.centralLayout.setSpacing(20)
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



        def Progressbar_exec(self,thread,exec_function,widgetTitle):#progress bar 실행
                if (widgetTitle=='UsageStats 분석 중....') and (adb_extract.get_device()==False):
                        self.smallWindow=smallWindow(self,'기기 연결 확인','기기 연결이 확인되지 않습니다.')
                elif (widgetTitle=='잔여 데이터 분석 중....') and self.usageCheck==False:
                        self.smallWindow=smallWindow(self,'UsageStats 추출 확인','File Wiping 흔적이 검사되지 않았습니다.')
                else:
                        self.ProgressWindow=ProcessBar.Process(self,thread,exec_function,widgetTitle)#progressWindow 객체 생성

        def AnalyzeUsagesStats(self,android_version, modelname, wiping_check, wiping_application,duplicated_application):#usagestats listview,os 정보 띄우기
                self.android_version=android_version
                self.modelname=modelname
                self.wiping_aplication=wiping_application
                self.duplicated_application=duplicated_application
                self.usageCheck=True
                if wiping_check == False:
                        self.osWidget.versionLabel.setText(f'Android Version {self.android_version}')
                        self.osWidget.nameLabel.setText(self.modelname)
                        deviceImageList=os.listdir('resource')
                        if any(self.modelname in filename for filename in deviceImageList):
                                self.osWidget.deviceImageWidget.update_modelname(self.modelname)
        
                        self.setTableApplicationData()# application 정보 출력 함수
                else:
                        self.smallWindow=smallWindow(self,'File Wiping 앱 실행 흔적 분석','File Wiping 앱 실행이 확인되지 않습니다. ')
 
                        
                
        def setTableApplicationData(self):
                application_model=QStandardItemModel()
                for application_name in self.duplicated_application:
                        application_model.appendRow(QStandardItem(application_name))
                self.application_listView.setModel(application_model)
                self.application_listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                #application_listView style
                self.application_listView.setStyleSheet('''
                                        QListView::item{
                                        padding:20px;
                                        border-bottom: 1px solid rgb(217,217,217);
                                        }
                                        QListView::item:hover{
                                        background-color:rgb(217, 217, 217);
                                        }
                                        QListView::item:focus{
                                        background-color:rgb(217,217,217);
                                        color:black;
                                        }
                                        QListView{
                                        background-color:rgb(255,255,255);
                                        border:1px solid rgb(217,217,217);
                                        }''')


        def setTableUsageData(self,index):
                ind=index.row()
                packages=pd.read_csv('./result/Package.csv')
                row=packages.iloc[ind]
                UsagePackage_model=QStandardItemModel()

                for column_name, value in row.items():
                        UsagePackage_model.appendRow(QStandardItem(f"{column_name}: {value}"))
                self.PackageList.setModel(UsagePackage_model)
                self.PackageList.setSpacing(10)
                

                self.PackageList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                event_log=pd.read_csv('./result/EventLog.csv')


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
                for col in range(self.EventLogTable.model().columnCount()):
                        max_width = 0

                        # Find the maximum content width in the column
                        for row in range(self.EventLogTable.model().rowCount()):
                                index = self.EventLogTable.model().index(row, col)
                                item_data = self.EventLogTable.model().data(index)
                                if item_data is not None:
                                        max_width = max(max_width, self.EventLogTable.fontMetrics().width(str(item_data)))

                        # Set the column width with a slight padding (e.g., 10 pixels)
                        self.EventLogTable.setColumnWidth(col, max_width + 30)
                self.EventLogTable.horizontalHeader().setCascadingSectionResizes(False)
                self.EventLogTable.horizontalHeader().setStretchLastSection(True)
                self.EventLogTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                self.EventLogTable.verticalHeader().setVisible(False)
                self.EventLogTable.setStyleSheet("""                                                 
                QTableView::item {
                        border: 1px solid black;  /* Set the border for each cell */
                }

                QHeaderView::section {
                        background-color:rgb(69,71,75);
                        color:white;
                        border: 1px solid black;  /* Set the border for header sections */
                }
                """)
        def viewData_exec(self):#viewData 화면 띄우기
                self.SecondWindow = view_data.ViewData(self,self.android_version,self.modelname)
                self.SecondWindow.show()
                self.hide()#지금 페이지 숨기기
