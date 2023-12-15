#1204 joys
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
from PyQt5.QtWidgets import QApplication
class InputDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent=parent
        self.setWindowTitle("User Information")
        self.setGeometry(0, 0, 500, 200)
        layout = QtWidgets.QFormLayout(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./resource/logo_Bokgumagic.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        # 오늘 날짜를 기본값으로 설정
        self.dateEdit = QtWidgets.QDateEdit(self)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDate(datetime.today())
        layout.addRow("Date:", self.dateEdit)

        # 사용자 이름 입력
        self.nameEdit = QtWidgets.QLineEdit(self)
        layout.addRow("Name:", self.nameEdit)

        # 확인 및 취소 버튼
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self
        )
        layout.addRow(buttons)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.centerOnParent()
    def getDate(self):
        return self.dateEdit.date().toString("yyyy-MM-dd")

    def getName(self):
        return self.nameEdit.text()
    
    def centerOnParent(self):
        parent_screen = QApplication.desktop().screenGeometry(self.parent)
        child_frame = self.frameGeometry()
        child_frame.moveCenter(parent_screen.center())
        self.move(child_frame.topLeft())
