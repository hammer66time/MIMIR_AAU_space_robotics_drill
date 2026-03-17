from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout,
    QVBoxLayout, QHBoxLayout, QLabel, QFrame
)

from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import sys


# ----------------------------------
# Button Panel
class ButtonPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.buttonHome = QPushButton("HOME DRILL")
        self.buttonAuto = QPushButton("AUTO DRILL")
        self.buttonStop = QPushButton("EMERGENCY STOP")
        self.buttonWeight = QPushButton("WEIGH MATERIAL")

        buttons = [self.buttonHome, self.buttonAuto, self.buttonStop]

        for b in buttons:
            b.setMinimumHeight(60)
            b.setFont(QFont("Arial", 16, QFont.Weight.Bold))

        self.buttonHome.setStyleSheet("background-color: black; color: white")
        self.buttonAuto.setStyleSheet("background-color: green; color: white")
        self.buttonStop.setStyleSheet("background-color: red; color: white")

        layout.addWidget(self.buttonHome)
        layout.addWidget(self.buttonAuto)
        layout.addWidget(self.buttonStop)
        layout.addStretch()

        self.setLayout(layout)

        self.buttonHome.clicked.connect(self.home)
        self.buttonAuto.clicked.connect(self.auto)
        self.buttonStop.clicked.connect(self.stop)

    def home(self):
        pass

    def auto(self):
        pass

    def stop(self):
        pass

    def setFunctionHome(self, func):
        self.buttonHome.clicked.disconnect()
        self.buttonHome.clicked.connect(func)

    def setFunctionAuto(self, func):
        self.buttonAuto.clicked.disconnect()
        self.buttonAuto.clicked.connect(func)

    def setFunctionStop(self, func):
        self.buttonStop.clicked.disconnect()
        self.buttonStop.clicked.connect(func)

    # Backwards-compatible aliases used by caller code
    def setFunctionSTART(self, func):
        self.setFunctionAuto(func)

    def setFunctionSTOP(self, func):
        self.setFunctionStop(func)

    def setFunctionHOME(self, func):
        self.setFunctionHome(func)

    def setFunctionAUTO(self, func):
        self.setFunctionAuto(func)

# ----------------------------------
# Status Panel
class StatusPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QGridLayout()

        title = QLabel("Drill Status")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rpm = QLabel("RPM: 0")
        self.torque = QLabel("Torque: 0 Nm")
        self.temp = QLabel("Temperature: 0 C")
        self.status = QLabel("System: Idle")

        labels = [self.rpm, self.torque, self.temp, self.status]

        for l in labels:
            l.setFont(QFont("Arial", 14))
            l.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
            l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title, 0, 0, 1, 2)

        layout.addWidget(self.rpm, 1, 0)
        layout.addWidget(self.torque, 1, 1)
        layout.addWidget(self.temp, 2, 0)
        layout.addWidget(self.status, 2, 1)

        self.setLayout(layout)


# ----------------------------------
# Main Window
class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hammer Drill Control System")
        self.setMinimumSize(900, 500)

        mainLayout = QHBoxLayout()

        self.buttons = ButtonPanel()
        self.status = StatusPanel()

        mainLayout.addWidget(self.buttons, 1)
        mainLayout.addWidget(self.status, 2)

        self.setLayout(mainLayout)


# ----------------------------------
# Run program
if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()
    #window.show()

    #sys.exit(app.exec())