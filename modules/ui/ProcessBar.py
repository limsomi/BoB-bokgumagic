import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QProgressBar,QDesktopWidget
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
        self.progress = QProgressBar(self)
        self.progress.setGeometry(10, 10, 280, 20)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.progress)


        self.setLayout(vbox)

        self.setGeometry(0, 0, 500, 200)
        self.setWindowTitle(self.label)
        self.show()
        self.centerOnParent()
    def startWorker(self):
        self.worker.progress_signal.connect(self.updateProgress)
        self.worker.result_signal.connect(self.proccess_function)
        self.worker.finished_signal.connect(self.threadFinished)
        self.worker.start()

    def updateProgress(self, value):
        self.progress.setValue(value)

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
