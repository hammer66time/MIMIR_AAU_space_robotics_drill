from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QComboBox
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QSplitter, QStackedWidget, QLineEdit, QDialog, QDialogButtonBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import PyQt6.QtWidgets as QtW
import sys

class MainWindow(QWidget):
    app = QApplication(sys.argv)
    def __init__(self, title = "Drill GUI by Hammer"):
        super().__init__()
        self.initUI()
        self.setMinimumSize(730,420)
        self.setWindowTitle(title)

    def initUI(self):
        layout = QVBoxLayout()

        self.buttonHome = QPushButton("Home drill")

        layout.addWidget(self.buttonHome)
        self.setLayout(layout)

    def runUI(self):
        self.show()
        self.app.exec()
    
# Run the GUI

window = MainWindow()
window.runUI() 