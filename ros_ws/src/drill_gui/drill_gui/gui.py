from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QComboBox
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QSplitter, QStackedWidget, QLineEdit, QDialog, QDialogButtonBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import PyQt6.QtWidgets as QtW
import sys

#----------------------------------
#These are the GUI buildinng classes
class Buttons(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.buttonHome = QPushButton("Home drill")
        self.buttonAuto = QPushButton("Auto Drilling")


        # Set colors of the buttons
        self.buttonHome.setStyleSheet("background-color: black; color : white")
        self.buttonAuto.setStyleSheet("background-color: green; color : white")
        

        # Set the size of the buttons
        self.buttonHome.setFixedHeight(50) 
        self.buttonAuto.setFixedHeight(50)
        

        # Set the font size of the buttons
        self.buttonHome.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.buttonAuto.setFont(QFont("Arial", 20, QFont.Weight.Bold))

        # Connect buttons to functions (slots)
        self.buttonHome.clicked.connect(self.home)
        self.buttonAuto.clicked.connect(self.auto)
        
        layout.addWidget(self.buttonHome)
        layout.addWidget(self.buttonAuto)

        self.setLayout(layout)

    def home(self):
        """Home button callback"""
        print("Home button clicked")
    
    def auto(self):
        """Auto button callback"""
        print("Auto button clicked")

    def setFunctionHome(self, function):
        self.buttonHome.clicked.connect(function)

    def setFunctionAuto(self, function):
        self.buttonAuto.clicked.connect(function)



#----------------------------------
#Main class, this is what will be shown
class MainWindow(QWidget):
    app = QApplication(sys.argv)
    def __init__(self, title = "Drill GUI by Hammer"):
        super().__init__()
        self.initUI()
        self.setMinimumSize(730,420)
        self.setWindowTitle(title)

    def initUI(self):
        layout = QVBoxLayout()

        #Create instances of classes
        self.Buttons = Buttons()

        #Add stuff to our main widget
        layout.addWidget(self.Buttons)

        self.setLayout(layout)        

        

    def runUI(self):
        self.show()
        self.app.exec()


#----------------------------------
# for testing gui appearance:
if __name__ == '__main__':
    window = MainWindow()
    window.runUI() 