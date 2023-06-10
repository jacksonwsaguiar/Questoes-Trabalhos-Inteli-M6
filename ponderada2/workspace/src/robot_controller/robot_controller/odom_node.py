#! usr/bin/env python3
import rclpy
import time
from rclpy.node import Node
from geometry_msgs.msg import Twist


class RobotNode(Node):

    def __init__(self):
        super().__init__("robot_node")
        self.msg = Twist()
        self.cmd_vel_pub_ = self.create_publisher(Twist, "/cmd_vel", 10)
        self.timer = self.create_timer(1, self.execute)
        self.get_logger().info("Robot node working on")


    def execute(self):
        self.send_to_trash()
        exit()

    def send_comand(self):
        self.cmd_vel_pub_.publish(self.msg)

    def move_front(self, sleep = 1.0):
        self.msg.linear.x = 0.5
        self.send_comand()
        time.sleep(sleep)
        self.stop_move()
        self.send_comand()
        time.sleep(1)

    def stop_move(self):
        self.msg.linear.x = 0.0
        self.msg.angular.z = 0.0

    def turn_right(self, sleep=1.0):
        self.msg.angular.z = -0.25
        self.send_comand()
        time.sleep(sleep)
        self.stop_move()
        self.send_comand()
        time.sleep(1)

    def turn_left(self, sleep=1.0):
        self.msg.angular.z = 0.25
        self.send_comand()
        time.sleep(sleep)
        self.stop_move()
        self.send_comand()
        time.sleep(1)


    def send_to_trash(self):
        self.get_logger().info("Heading to trash...")
       
        self.move_front(6)

        self.turn_right(7.5)
      
        self.move_front(1.8)
     
        self.turn_left(7.5)

        self.move_front(1.6)
      
        self.turn_left(7.5)

        self.move_front(4)

        self.turn_right(7.5)

        self.move_front(5)
        
        self.turn_left(7.5)
        
        self.move_front(10)

        self.turn_left(7.5)
        
        self.move_front(4)

        self.turn_left(7.5)

        self.move_front(4.7)

        self.get_logger().info("Arrived at trash...")

    def save_path(self):
        return


def main(args=None):
    rclpy.init(args=args)
    node = RobotNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
