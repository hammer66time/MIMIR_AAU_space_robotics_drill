import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import serial

class NanoComs(Node):
    def __init__(self):
        super().__init__('nano_communication')
        # Create a publisher on the 'nano' topicself.state = "IDLE"
        self.publisher_ = self.create_publisher(String, 'nano', 10)

        # Subscribe to GUI commands
        self.subscription = self.create_subscription(
            String,
            'state',
            self.command_callback,
            10)
        
        timer_period = 0.1 # seconds
        self.timer = self.create_timer(timer_period, self.com_callback)


        #-----------------------------------------------
        #Serial communication:
        try:
            self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.01)
            self.get_logger().info('Arduino Nano connected successfully')
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to connect to Arduino Nano: {e}')
            self.ser = None

    def command_callback(self, msg):
        #Handle commands from state machine
        self.state = msg.data
        #self.get_logger().info(f'Received command: {self.state}')
        # Send command to Arduino Nano
        if self.ser is not None:
            try:
                self.ser.write(f'{self.state}\n'.encode())
            except serial.SerialException as e:
                self.get_logger().error(f'Failed to send command: {e}')
        else:
            self.get_logger().warning('Cannot send command - Arduino not connected')

    def com_callback(self):
        if self.ser is None:
            return
        
        try:
            # Check if data is available
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode().strip()
                
                if line:  # Only publish if line is not empty
                    #---------------------------------------
                    #ROS2 message for publishing
                    msg = String()
                    msg.data = line
                    self.publisher_.publish(msg)
                    #self.get_logger().info(f'Received from Arduino: {line}')
        except serial.SerialException as e:
            self.get_logger().error(f'Serial communication error: {e}')
        except UnicodeDecodeError as e:
            self.get_logger().warning(f'Failed to decode data: {e}')

def main(args=None):
    rclpy.init(args=args) # Initialize the ROS client library
    node = NanoComs() # Create an instance of the node
    rclpy.spin(node) # Keep the node running until it is shutdown
    node.destroy_node() # Clean up the node before it is destroyed
    
    rclpy.shutdown() # Shutdown the ROS client library

if __name__ == "__main__":
    main()