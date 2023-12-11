from modules.ui import view_usage
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = view_usage.Usage_Window()
    ui.show()#open usage page
    app.exec_()



if __name__=="__main__":
    main()

print(".")