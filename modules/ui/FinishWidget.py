import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar,QDesktopWidget
from PyQt5 import QtCore, QtGui, QtWidgets

class FinishWidget(QWidget):#보고서 작성 완료 창
    def __init__(self,parent):
        super().__init__()
        self.parent=parent
        self.initUI()
    def initUI(self):

        self.setGeometry(0, 0, 500, 200)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕 Semilight")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setStyleSheet("padding:2px;\n"
"margin:10px;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem)
        self.finishButton = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕 Semilight")
        font.setPointSize(11)
        self.finishButton.setFont(font)
        self.finishButton.setStyleSheet("padding:10px;")
        self.finishButton.setObjectName("finishButton")
        self.finishButton.clicked.connect(self.finish)
        self.horizontalLayout.addWidget(self.finishButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayout.setStretch(0,4)
        self.horizontalLayout.setStretch(1,3)
        self.horizontalLayout.setStretch(2,4)

        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.verticalLayout.setStretch(0, 4)
        self.verticalLayout.setStretch(1, 3)
        self.verticalLayout.setStretch(2, 2)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.show()
        
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "보고서 작성이 완료되었습니다"))
        self.finishButton.setText(_translate("Form", "확인"))
        self.centerOnParent()

    def finish(self):
        exit(0)
    def centerOnParent(self):
        parent_screen = QApplication.desktop().screenGeometry(self.parent)
        child_frame = self.frameGeometry()
        child_frame.moveCenter(parent_screen.center())
        self.move(child_frame.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    finish=FinishWidget()
    finish.show()
    sys.exit(app.exec_())
