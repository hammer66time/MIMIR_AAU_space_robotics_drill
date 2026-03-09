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
        self.states = ["IDLE", "DRILL"]
        self.machine = Machine(model=self, states=self.states, initial="IDLE")
        self.machine.add_transition("start", "IDLE", "DRILL")
        self.machine.add_transition("stop", "DRILL", "IDLE")

    def command_callback(self, msg):
        """Handle commands from GUI"""
        command = msg.data
        self.get_logger().info(f'Received command: {command}')
        if command == "HOME":
            self.stop()  # Go back to IDLE
        elif command == "AUTO":
            self.start()  # Start drilling

    def state_callback(self):
        msg = String()
        if self.state == "IDLE":
             msg.data = "IDLE"
             self.publisher_.publish(msg)
             #self.get_logger().info('Publishing: "%s"' % msg.data)

        elif self.state == "DRILL":
            msg.data = "DRILL"
            self.publisher_.publish(msg)
            #self.get_logger().info('Publishing: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args) # Initialize the ROS client library
    node = Drill() # Create an instance of the node
    rclpy.spin(node) # Keep the node running until it is shutdown
    node.destroy_node() # Clean up the node before it is destroyed
    rclpy.shutdown() # Shutdown the ROS client library

if __name__ == "__main__":
    main()