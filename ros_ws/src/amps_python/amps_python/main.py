import rclpy
from rclpy.node import Node
#Costum classes:
import gui

class GUI_node(Node):
    def __init__(self):
        super().__init__("GUI_node")

    def runGUI(self):
        # Run the GUI
        window = gui.MainWindow()
        window.runUI() 



def main():
    rclpy.init()
    node = GUI_node()
    node.runGUI()
    # Note: rclpy.spin() would block the GUI, so we don't use it here
    # The GUI event loop will run instead
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    

