import rclpy
from rclpy.node import Node
from std_msgs.msg import String
#Costum classes:
from drill_gui import gui

class GUI_node(Node):
    def __init__(self):
        super().__init__("GUI_node")
        # Create a publisher to send commands to the drill
        self.publisher_ = self.create_publisher(String, 'drill_commands', 10)
        self.get_logger().info('GUI Node started')

    def send_command(self, command: str):
        """Send a command via ROS2 topic"""
        msg = String()
        msg.data = command
        self.publisher_.publish(msg)
        self.get_logger().info(f'Sent command: {command}')

    def runGUI(self):
        # Run the GUI
        window = gui.MainWindow()
        # Connect buttons to ROS2 publish functions
        window.Buttons.setFunctionHome(lambda: self.send_command('HOME'))
        window.Buttons.setFunctionAuto(lambda: self.send_command('AUTO'))
        window.runUI() 


j
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
    

