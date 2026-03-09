# ROS2 stuff
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# State machine stuff
from transitions import Machine

class Drill(Node):
    def __init__(self):
        super().__init__("state_machine")

        # ROS publisher
        self.get_logger().info("State machine up and running")
        self.publisher_ = self.create_publisher(String, 'state', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.state_callback)

        # ROS subscriber
        self.subscription = self.create_subscription(
            String,
            'drill_commands',
            self.command_callback,
            10)

        # State machine
        self.states = ["IDLE","HOMING", "DRILL", "LIFT", "EMPTY", "WEIGH", "TRANSPORT" , "ERROR"]
        self.machine = Machine(model=self, states=self.states, initial="IDLE")
        
        # Auto transitions (sequential flow)
        self.machine.add_transitions([
            ["auto_home", "IDLE", "HOMING"],
            ["auto_drill", "HOMING", "DRILL"],
            ["auto_lift", "DRILL", "LIFT"],
            ["auto_empty", "LIFT", "EMPTY"],
            ["auto_weigh", "EMPTY", "WEIGH"],
            ["auto_transport", "WEIGH", "TRANSPORT"],
            ])

        # Manual transitions (go back home from anywhere, then to target state)
        self.machine.add_transitions([
            ["manuel_back", "*", "IDLE"]      # Emergency stop - go back to IDLE
            ])

        # Error state (accessible from anywhere)
        self.machine.add_transition("error", "*", "ERROR")

    def command_callback(self, msg):
        """Handle commands from GUI"""
        command = msg.data
        self.get_logger().info(f'Received command: {command}')
        if command == "RESET":
            self.manuel_back()  # Go back to IDLE

        elif command == "AUTO":
            self.auto_home()

        elif command == "ESTOP":
            self.error()

    def state_callback(self):
        msg = String()
        if self.state == "IDLE":
             msg.data = "IDLE"
             self.publisher_.publish(msg)

        elif self.state == "HOMING":
            msg.data = "HOMING"
            self.publisher_.publish(msg)
        
        elif self.state == "DRILL":
            msg.data = "DRILL"
            self.publisher_.publish(msg)

        elif self.state == "LIFT":
            msg.data = "LIFT"
            self.publisher_.publish(msg)

        elif self.state == "WEIGH":
            msg.data = "WEIGH"
            self.publisher_.publish(msg)
            
        elif self.state == "EMPTY":
            msg.data = "EMPTY"
            self.publisher_.publish(msg)

        elif self.state == "TRANSPORT":
            msg.data = "TRANSPORT"
            self.publisher_.publish(msg)

        elif self.state == "ERROR":
            msg.data = "ERROR"
            self.publisher_.publish(msg)
            
def main(args=None):
    rclpy.init(args=args) # Initialize the ROS client library
    node = Drill() # Create an instance of the node
    rclpy.spin(node) # Keep the node running until it is shutdown
    node.destroy_node() # Clean up the node before it is destroyed
    rclpy.shutdown() # Shutdown the ROS client library

if __name__ == "__main__":
    main()