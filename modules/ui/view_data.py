from PyQt5 import QtCore, QtGui, QtWidgets
import os
from PyQt5.QtWidgets import*
from modules.ui.view_clipboard import ClipboardView
from modules.ui.TableView import TableView
from modules.ui.view_cache import CacheView
from modules.ui.view_package import PackageCacheView,SharedPrefsView
from modules.ui.view_dialog import InputDialog #1204 joys
from modules.data_processing.report import WriteReport #1207 joys
from modules.ui import ProcessBar
from modules.ui.FinishWidget import FinishWidget
from modules.ui.Image import deviceImage
from modules.ui.osWidget import osWidget
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,QSize,QEvent
class ViewData(QMainWindow):
        def __init__(self,parent,android_version,modelname):
                super().__init__()
                self.parent=parent
                self.wiping_aplication=parent.duplicated_application
                self.android_version=android_version
                self.modelname=modelname
                self.setupUi()
        def setupUi(self):
                parent_geometry = self.parent.geometry()
                self.setGeometry(parent_geometry)

                self.setObjectName("self")
                self.viewDataCheck=False
                self.centralwidget = QtWidgets.QWidget(self)
                self.centralwidget.setStyleSheet("background-color:rgb(235,235,235);")
                self.centralwidget.setObjectName("centralwidget")
                #Bokgumagik_logo
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("./resource/logo_Bokgumagic.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.setWindowIcon(icon)
                self.setStyleSheet('''
                                QTabBar::tab:selected { 
                                background: rgb(100, 204, 197); 
                                }
                                QTabBar::tab {
                                background: lightgray; 
                                color:white;
                                } 
                                QTabWidget{background-color:white;}
                                ''')
                # # 기본 제목 표시줄 숨기기
                # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
                # # 사용자 지정 제목 표시줄 추가
                # self.customTitleBar = CustomTitleBar(self)
                # self.setMenuWidget(self.customTitleBar)

                #전체화면 layout
                self.centralLayout = QtWidgets.QVBoxLayout(self.centralwidget)
                self.centralLayout.setContentsMargins(5, 5, 5, 5)
                self.centralLayout.setSpacing(5)
                self.centralLayout.setObjectName("centralLayout")
                #Menubar
                self.MenuLayout=QtWidgets.QHBoxLayout()
                self.logo=QtWidgets.QLabel()
                logo=QPixmap('./resource/logo2.png')
                self.logo.setPixmap(logo.scaled(
            QSize(self.logo.width(), self.logo.height()-100), Qt.KeepAspectRatio))


                self.MenuLayout.addWidget(self.logo)
                self.reportButton = QtWidgets.QPushButton()#reportButton
                self.reportButton.setText('보고서 작성')
                font = QtGui.QFont()
                font.setFamily("맑은 고딕")
                font.setPointSize(15)
                font.setBold(True)
                font.setWeight(75)
                self.reportButton.setFont(font)
                self.reportButton.setStyleSheet('''QPushButton{background-color:rgb(100, 204, 197);
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
                self.reportButton.setObjectName("reportButton")
                self.reportButton.clicked.connect(lambda:self.dialog_exec())

                spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.MenuLayout.addItem(spacerItem)
                self.MenuLayout.addWidget(self.reportButton)
                
                self.MenuLayout.setStretch(0,4)
                self.MenuLayout.setStretch(1,10)
                self.MenuLayout.setStretch(2,2)
                self.MenuLayout.setContentsMargins(30,10,30,30)
                self.centralLayout.addLayout(self.MenuLayout)

                self.horizontalLayout=QtWidgets.QHBoxLayout()
                #sidebar layout
                self.SideLayout = QtWidgets.QVBoxLayout()
                self.SideLayout.setSpacing(0)
                self.SideLayout.setObjectName("SideLayout")


                #sidebar header
                self.SideBar=QtWidgets.QWidget()
                effect = QGraphicsDropShadowEffect()
                effect.setOffset(0, 0)
                effect.setBlurRadius(15)
                self.SideBar.setGraphicsEffect(effect)
                self.SideBarLayout=QtWidgets.QVBoxLayout(self.SideBar)
                self.SideBarLayout.setContentsMargins(0,0,0,0)
                self.SideBarLayout.setSpacing(5)
                self.SideLabel = QtWidgets.QLabel()
                self.SideLabel.setText('잔여 데이터')

                font = QtGui.QFont()
                font.setFamily("맑은 고딕")
                font.setPointSize(15)
                font.setBold(True)
                font.setWeight(75)
                self.SideLabel.setFont(font)

                self.SideLabel.setStyleSheet("background-color:rgb(100, 204, 197);\n"
        "color:white;"
        "border:1px solid rgb(100,204.197);\n"
        "padding:2px 2px 2px 5px;")#sidebar header style
                self.SideLabel.setObjectName("SideLabel")
                self.SideBarLayout.addWidget(self.SideLabel)
                #sidebar buttons
                self.SideButton = QtWidgets.QListWidget(self.centralwidget)
                font = QtGui.QFont()
                font.setFamily("Segoe UI Semibold")
                font.setPointSize(13)
                font.setBold(True)
                font.setWeight(75)
                self.SideButton.setFont(font)

                #sidebar style
                self.SideButton.setStyleSheet('''
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

                self.SideButton.setMidLineWidth(0)
                self.SideButton.setObjectName("SideButton")
                item = QtWidgets.QListWidgetItem('Gallery Cache')
                self.SideButton.addItem(item)
                item = QtWidgets.QListWidgetItem('Clipboard')
                self.SideButton.addItem(item)
                item = QtWidgets.QListWidgetItem('Contacts')
                self.SideButton.addItem(item)
                item = QtWidgets.QListWidgetItem('PackageFile(Cache)')
                self.SideButton.addItem(item)
                item = QtWidgets.QListWidgetItem('PackageFile(Shared Prefs)')
                self.SideButton.addItem(item)
                self.SideBarLayout.addWidget(self.SideButton)

                self.SideBarLayout.setStretch(0,1)
                self.SideBarLayout.setStretch(1,7)
                self.SideLayout.addWidget(self.SideBar)

                self.SideButton.clicked.connect(self.selected_Sidebar)

                #osWidget
                self.osWidget=osWidget(500,550)
                self.osWidget.deviceImageWidget.update_modelname(self.modelname)
                self.SideLayout.addWidget(self.osWidget)
                self.osWidget.versionLabel.setText(f'Android Version {self.android_version}')
                self.osWidget.nameLabel.setText(self.modelname)



        
                self.SideLayout.setStretch(0,5)
                self.SideLayout.setStretch(1,3)
                self.SideLayout.setContentsMargins(0,0,10,10)
                self.SideLayout.setSpacing(30)
                self.horizontalLayout.addLayout(self.SideLayout)

                self.viewData = QtWidgets.QWidget()#오른쪽 data 출력 부분
                effect = QGraphicsDropShadowEffect()
                effect.setOffset(0, 0)
                effect.setBlurRadius(15)
                self.viewData.setGraphicsEffect(effect)
                self.viewData.setStyleSheet('''
                        border:1px solid rgb(217,217,217);
                        ''')
                self.viewData.setObjectName("viewData")
                self.viewDataLayout = QtWidgets.QVBoxLayout(self.viewData)
                self.viewDataLayout.setObjectName("viewDataLayout")
                self.viewDataLabel = QtWidgets.QLabel('View Details')#viewData header
                font = QtGui.QFont()
                font.setFamily("맑은 고딕")
                font.setPointSize(15)
                font.setBold(True)
                font.setWeight(75)
                self.viewDataLabel.setFont(font)
                self.viewDataLabel.setStyleSheet("background-color:rgb(69, 71, 75);\n"
        "border:1px solid rgb(217,217,217);\n"
        "padding:9px;\n"
        "margin:0px;"
        "color:white;")
                self.viewDataLabel.setObjectName("viewDataLabel")
                self.viewDataLayout.addWidget(self.viewDataLabel)
                self.viewWidget=QtWidgets.QWidget(self.viewData)
                self.viewWidget.setStyleSheet('background-color:white;')
                self.viewDataLayout.addWidget(self.viewWidget)
                self.viewDataLayout.setStretch(0,1)
                self.viewDataLayout.setStretch(1,17)

                self.viewDataLayout.setContentsMargins(10,10,10,10)
                self.viewDataLayout.setSpacing(0)
                self.horizontalLayout.addWidget(self.viewData)
                self.horizontalLayout.setStretch(0, 5)
                self.horizontalLayout.setStretch(1, 17)
                self.horizontalLayout.setSpacing(30)
                self.horizontalLayout.setContentsMargins(30,10,30,30)

                self.centralLayout.addLayout(self.horizontalLayout)
                self.centralLayout.setStretch(0,1)
                self.centralLayout.setStretch(1,17)

                self.setCentralWidget(self.centralwidget)
                self.statusbar = QtWidgets.QStatusBar(self)
                self.statusbar.setObjectName("statusbar")
                self.setStatusBar(self.statusbar)

                self.retranslateUi()
                QtCore.QMetaObject.connectSlotsByName(self)

        def retranslateUi(self):
                _translate = QtCore.QCoreApplication.translate
                self.setWindowTitle(_translate("self", "BokguMagic_v2.0"))
                # self.reportButton.setText(_translate("self", "보고서 작성"))
                

        def dialog_exec(self): #report progressbar 출력
                self.dialog=InputDialog(self)
                if self.dialog.exec_() == QtWidgets.QDialog.Accepted:
                        date = self.dialog.getDate()
                        name = self.dialog.getName()
                thread=WriteReport(date,name,self.wiping_aplication)
                widgetTitle='보고서 작성 중 ....'

                self.ProgressWindow=ProcessBar.Process(self,thread,self.Window_finished,widgetTitle)
                

        def selected_Sidebar(self):
                selected_item=self.SideButton.currentItem()
                self.viewDataLayout.removeWidget(self.viewWidget)
                self.viewWidget.setParent(None)
                if selected_item.text()=='Gallery Cache':
                        self.viewDataCheck=True
                        self.viewWidget=QtWidgets.QWidget(self.viewData)
                        CacheView(self.viewWidget,'gallery3d_cache')
                elif selected_item.text()=='Clipboard':
                        self.viewDataCheck=True
                        self.viewWidget=QtWidgets.QTabWidget(self.viewData)
                        font = QtGui.QFont()
                        font.setFamily("맑은 고딕")
                        font.setPointSize(13)
                        font.setBold(True)
                        font.setWeight(75)
                        self.viewWidget.setFont(font)
                        ClipboardView(self)
                elif selected_item.text()=='Contacts':
                        self.viewDataCheck=True
                        self.viewWidget=QtWidgets.QWidget(self.viewData)
                        self.viewWidget.setStyleSheet('background-color:rgb(255,255,255);')
                        TableView(self.viewWidget,'./result/contacts.csv')
                elif selected_item.text()=='PackageFile(Cache)':
                        self.viewDataCheck=True
                        self.viewWidget=QtWidgets.QTabWidget(self.viewData)
                        font = QtGui.QFont()
                        font.setFamily("맑은 고딕")
                        font.setPointSize(13)
                        font.setBold(True)
                        font.setWeight(75)
                        self.viewWidget.setFont(font)
                        PackageCacheView(self)
                elif selected_item.text()=='PackageFile(Shared Prefs)':
                        self.viewDataCheck=True
                        self.viewWidget=QtWidgets.QTabWidget(self.viewData)
                        font = QtGui.QFont()
                        font.setFamily("맑은 고딕")
                        font.setPointSize(13)
                        font.setBold(True)
                        font.setWeight(75)
                        self.viewWidget.setFont(font)
                        SharedPrefsView(self)
                # self.viewDataLayout.setContentsMargins(10, 10, 10, 10)
                self.viewWidget.setStyleSheet('border:none;background-color:white;margin:0px;')
                self.viewDataLayout.addWidget(self.viewWidget)
                self.viewDataLayout.setStretch(0, 1)
                self.viewDataLayout.setStretch(1, 17)
        def Window_finished(self):
                self.finishWidget=FinishWidget(self)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWin = ViewData(None)
    mainWin.show()
    sys.exit(app.exec_())
