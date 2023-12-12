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

class ViewData(QMainWindow):
        def __init__(self,parent):
                super().__init__()
                self.parent=parent
                self.wiping_aplication=parent.duplicated_application
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
                icon.addPixmap(QtGui.QPixmap("./logo_Bokgumagic.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.setWindowIcon(icon)

                # 기본 제목 표시줄 숨기기
                self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
                # 사용자 지정 제목 표시줄 추가
                self.customTitleBar = CustomTitleBar(self)
                self.setMenuWidget(self.customTitleBar)

                #전체화면 layout
                self.centralLayout = QtWidgets.QHBoxLayout(self.centralwidget)
                self.centralLayout.setContentsMargins(5, 5, 5, 5)
                self.centralLayout.setSpacing(5)
                self.centralLayout.setObjectName("centralLayout")
                #sidebar layout
                self.SideLayout = QtWidgets.QVBoxLayout()
                self.SideLayout.setSpacing(0)
                self.SideLayout.setObjectName("SideLayout")
                #sidebar header
                self.SideLabel = QtWidgets.QLabel(self.centralwidget)
                font = QtGui.QFont()
                font.setFamily("맑은 고딕 Semilight")
                font.setPointSize(13)
                font.setBold(True)
                font.setWeight(75)
                self.SideLabel.setFont(font)
                self.SideLabel.setStyleSheet("background-color:rgb(242,242,242);\n"
        "border:1px solid rgb(217,217,217);\n"
        "padding:2px 2px 2px 5px;")#sidebar header style
                self.SideLabel.setObjectName("SideLabel")
                self.SideLayout.addWidget(self.SideLabel)
                #sidebar buttons
                self.SideButton = QtWidgets.QListWidget(self.centralwidget)
                font = QtGui.QFont()
                font.setFamily("Segoe UI Semibold")
                font.setPointSize(11)
                font.setBold(True)
                font.setWeight(75)
                self.SideButton.setFont(font)
                #sidebar style
                self.SideButton.setStyleSheet("QListWidget {\n"
        "        background-color: rgb(255,255,255);\n"
        "           border:1px solid rgb(217,217,217);\n"
        "\n"
        "    }\n"
        "    QListWidget::item{\n"
        "        padding:15px;\n"
        "        border-bottom: 1px solid rgb(217,217,217);\n"
        "    }\n"
        "    QListWidget::item:hover{\n"
        "        background-color:rgb(195, 209, 227);\n"
        "    }\n"
        "    QListWidget::item:focus{\n"
        "        background-color:rgb(195, 209, 227);\n"
        "        color:black;\n"
        "    }")
                self.SideButton.setMidLineWidth(0)
                self.SideButton.setObjectName("SideButton")
                item = QtWidgets.QListWidgetItem()
                self.SideButton.addItem(item)
                item = QtWidgets.QListWidgetItem()
                self.SideButton.addItem(item)
                item = QtWidgets.QListWidgetItem()
                self.SideButton.addItem(item)
                item = QtWidgets.QListWidgetItem()
                self.SideButton.addItem(item)
                item = QtWidgets.QListWidgetItem()
                self.SideButton.addItem(item)
                self.SideLayout.addWidget(self.SideButton)

                self.SideButton.clicked.connect(self.selected_Sidebar)

                self.report = QtWidgets.QWidget(self.centralwidget)#sidebar report 부분
                self.report.setStyleSheet("background-color:rgb(242,242,242);\n"
        "border:1px solid rgb(217,217,217);")
                self.report.setObjectName("report")
                #sidber report 부분 layout(space 부분 포함)
                self.reportLayout = QtWidgets.QHBoxLayout(self.report)
                self.reportLayout.setSpacing(3)
                self.reportLayout.setObjectName("horizontalLayout_2")
                spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.reportLayout.addItem(spacerItem)

                self.reportButton = QtWidgets.QPushButton(self.report)#reportButton
                font = QtGui.QFont()
                font.setFamily("맑은 고딕 Semilight")
                font.setPointSize(18)
                font.setBold(True)
                font.setWeight(75)
                self.reportButton.setFont(font)
                #reportButton style
                self.reportButton.setStyleSheet("QPushButton{background-color:rgb(217,217,217);\n"
        "padding:15px 15px 15px 15px;}\n"
        "\n"
        "QPushButton:hover{background-color:rgb(195, 209, 227);}\n"
        "")
                self.reportButton.setObjectName("reportButton")
                self.reportButton.clicked.connect(lambda:self.dialog_exec())
                self.reportLayout.addWidget(self.reportButton)
                spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.reportLayout.addItem(spacerItem1)
                self.reportLayout.setStretch(0, 2)
                self.reportLayout.setStretch(1, 1)
                self.reportLayout.setStretch(2, 2)
                self.SideLayout.addWidget(self.report)
                self.SideLayout.setStretch(0, 1)
                self.SideLayout.setStretch(1, 10)
                self.SideLayout.setStretch(2, 5)
                self.SideLayout.setContentsMargins(10,10,10,10)
                self.centralLayout.addLayout(self.SideLayout)

                self.viewData = QtWidgets.QWidget(self.centralwidget)#오른쪽 data 출력 부분
                self.viewData.setStyleSheet("border:1px solid rgb(217,217,217);")
                self.viewData.setObjectName("viewData")
                self.viewDataLayout = QtWidgets.QVBoxLayout(self.viewData)
                self.viewDataLayout.setObjectName("viewDataLayout")

                self.viewDataLabel = QtWidgets.QLabel(self.viewData)#viewData header
                font = QtGui.QFont()
                font.setFamily("맑은 고딕 Semilight")
                font.setPointSize(13)
                font.setBold(True)
                font.setWeight(75)
                self.viewDataLabel.setFont(font)
                self.viewDataLabel.setStyleSheet("background-color:rgb(242,242,242);\n"
        "border:1px solid rgb(217,217,217);\n"
        "padding:9px;\n")
                self.viewDataLabel.setObjectName("viewDataLabel")
                self.viewDataLayout.addWidget(self.viewDataLabel)


                self.centralLayout.addWidget(self.viewData)
                self.centralLayout.setStretch(0, 5)
                self.centralLayout.setStretch(1, 17)
                self.setCentralWidget(self.centralwidget)
                self.statusbar = QtWidgets.QStatusBar(self)
                self.statusbar.setObjectName("statusbar")
                self.setStatusBar(self.statusbar)

                self.retranslateUi()
                QtCore.QMetaObject.connectSlotsByName(self)

        def retranslateUi(self):
                _translate = QtCore.QCoreApplication.translate
                self.setWindowTitle(_translate("self", "BokguMagic_v2.0"))
                self.SideLabel.setText(_translate("self", "잔여 데이터"))
                self.SideButton.setWhatsThis(_translate("self", "<html><head/><body><p><br/></p></body></html>"))
                __sortingEnabled = self.SideButton.isSortingEnabled()
                self.SideButton.setSortingEnabled(False)
                item = self.SideButton.item(0)
                item.setText(_translate("self", "Gallery Cache"))
                item = self.SideButton.item(1)
                item.setText(_translate("self", "Clipboard"))
                item = self.SideButton.item(2)
                item.setText(_translate("self", "Contacts"))
                item = self.SideButton.item(3)
                item.setText(_translate("self", "Package File (Cache)"))
                item = self.SideButton.item(4)
                item.setText(_translate("self", "Package file (Shared_Prefs)"))
                self.SideButton.setSortingEnabled(__sortingEnabled)
                self.reportButton.setText(_translate("self", "보고서 작성"))
                self.viewDataLabel.setText(_translate("self", "View Details"))
                self.SideButton.clicked.connect(self.selected_Sidebar)

        def dialog_exec(self): #report progressbar 출력
                self.dialog=InputDialog(self)
                if self.dialog.exec_() == QtWidgets.QDialog.Accepted:
                        date = self.dialog.getDate()
                        name = self.dialog.getName()
                thread=WriteReport(date,name,self.wiping_aplication)
                widgetTitle='보고서 작성 중 ....'

                self.ProgressWindow=ProcessBar.Process(self,thread,self.Window_finished,widgetTitle)
                

        def selected_Sidebar(self):
                #각 버튼에 따라 데이터 보여줌
                #viewData는 viewWidget, viewLabel으로 이루어져 있음(viewWidget이 데이터 보여주는 부분)
                selected_item=self.SideButton.currentItem()
                if self.viewDataCheck==True and self.viewDataLayout.indexOf(self.viewWidget)!=-1:
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
                        font.setFamily("맑은 고딕 Semilight")
                        font.setPointSize(11)
                        font.setBold(True)
                        font.setWeight(75)
                        self.viewWidget.setFont(font)
                        ClipboardView(self)
                        self.viewWidget.setStyleSheet('''
                                QTabWidget::pane {
                                border: 1px solid lightgray;
                                top:-1px; 
                                background: rgb(245, 245, 245);; 
                                } 
                                QTabBar::tab {
                                background: rgb(230, 230, 230); 
                                border: 1px solid lightgray; 
                                padding: 15px;
                                } 

                                QTabBar::tab:selected { 
                                background: red; 
                                margin-bottom: -1px; 
                                }
                        ''')
                elif selected_item.text()=='Contacts':
                        self.viewDataCheck=True
                        self.viewWidget=QtWidgets.QWidget(self.viewData)
                        self.viewWidget.setStyleSheet('background-color:rgb(255,255,255);')
                        TableView(self.viewWidget,'./result/contacts.csv')
                elif selected_item.text()=='Package File (Cache)':
                        self.viewDataCheck=True
                        self.viewWidget=QtWidgets.QTabWidget(self.viewData)
                        # self.viewWidget.setStyleSheet('background-color:rgb(255,255,255);')
                        font = QtGui.QFont()
                        font.setFamily("맑은 고딕 Semilight")
                        font.setPointSize(11)
                        font.setBold(True)
                        font.setWeight(75)
                        self.viewWidget.setFont(font)
                        PackageCacheView(self)
                elif selected_item.text()=='Package file (Shared_Prefs)':
                        self.viewDataCheck=True
                        self.viewWidget=QtWidgets.QTabWidget(self.viewData)
                        font = QtGui.QFont()
                        font.setFamily("맑은 고딕 Semilight")
                        font.setPointSize(11)
                        font.setBold(True)
                        font.setWeight(75)
                        self.viewWidget.setFont(font)
                        SharedPrefsView(self)
                self.viewDataLayout.setContentsMargins(10, 10, 10, 10)
                self.viewWidget.setStyleSheet('border:none;')
                self.viewDataLayout.setSpacing(1)
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
