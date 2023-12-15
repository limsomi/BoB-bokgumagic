import sys
from PyQt5.QtWidgets import QApplication,QLabel, QWidget, QVBoxLayout, QPushButton, QProgressBar,QDesktopWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from modules.data_processing.usage import Usage_Thread

class Process(QWidget):
    def __init__(self,parent,thread,function,label):
        super().__init__()
        self.parent=parent
        self.label=label
        self.proccess_function=function
        self.worker=thread
        self.initUI()
        self.startWorker()
    def initUI(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./resource/logo_Bokgumagic.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.progressLabel=QLabel(self)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setWeight(45)
        font.setPointSize(15)
        self.progressLabel.setFont(font)
        self.progress = QProgressBar(self)
        self.progress.setGeometry(10, 10, 280, 20)
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.progressLabel)
        vbox.addWidget(self.progress)
        spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        vbox.addItem(spacerItem)
        vbox.setStretch(0,4)
        vbox.setStretch(1,2)
        vbox.setStretch(2,2)


        self.setLayout(vbox)

        self.setGeometry(0, 0, 600,300)
        self.setWindowTitle(self.label)
        self.show()
        self.centerOnParent()
    def startWorker(self):
        self.worker.progress_signal.connect(self.updateProgress)
        self.worker.result_signal.connect(self.proccess_function)
        self.worker.finished_signal.connect(self.threadFinished)
        self.worker.start()

    def updateProgress(self, value,string):
        self.progress.setValue(value)
        self.progressLabel.setText(string)
        self.progressLabel.setAlignment(QtCore.Qt.AlignCenter)
    def threadFinished(self):
        self.close()

    def centerOnParent(self):
        parent_screen = QApplication.desktop().screenGeometry(self.parent)
        child_frame = self.frameGeometry()
        child_frame.moveCenter(parent_screen.center())
        self.move(child_frame.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Process = Process()
    sys.exit(app.exec_())
