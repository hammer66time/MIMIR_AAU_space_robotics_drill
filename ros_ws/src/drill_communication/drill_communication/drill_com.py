import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import serial

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        # Create a publisher on the 'nano' topic
        self.publisher_ = self.create_publisher(String, 'nano', 10)
        timer_period = 0.5 # seconds
        self.timer = self.create_timer(timer_period, self.com_callback)
        self.i = 0

        self.ser = serial.Serial('/dev/ttyUSB0', 115200)

    def com_callback(self):
        while True:
            line = self.ser.readline().decode().strip()
            
            # eksempel: send kommando
            self.ser.write(b'LED_ON\n')
           
            #---------------------------------------
            #ROS2 message for publishing
            msg = String()
            msg.data = line
            self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args) # Initialize the ROS client library
    node = MinimalPublisher() # Create an instance of the node
    rclpy.spin(node) # Keep the node running until it is shutdown
    node.destroy_node() # Clean up the node before it is destroyed
    
    rclpy.shutdown() # Shutdown the ROS client library

if __name__ == "__main__":
    main()