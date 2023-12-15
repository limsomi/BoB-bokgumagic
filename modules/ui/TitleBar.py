from PyQt5 import QtCore, QtGui, QtWidgets

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
        icon = QtGui.QPixmap('./resource/logo_Bokgumagic.png').scaled(24, 24, QtCore.Qt.KeepAspectRatio)
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