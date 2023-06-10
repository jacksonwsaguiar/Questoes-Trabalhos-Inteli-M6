#! usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class RobotNode(Node):

    def __init__(self):
        super().__init__("robot_node")
        self.path_size = 0
        self.cmd_vel_pub_ = self.create_publisher(Twist, "/cmd_vel", 10)
        self.timer = self.create_timer(1, self.send_comand)
        self.send_comand()
        self.get_logger().info("Robot node working on")

    def send_comand(self):
        msg = Twist()
        msg.linear.x = 5.0
        #msg.angular.z = 5.0
        self.cmd_vel_pub_.publish(msg)
        msg.linear.x = 0.0
        self.cmd_vel_pub_.publish(msg)

    def send_to_room(self):
        return

    def save_path(self):
        return


def main(args=None):
    rclpy.init(args=args)
    node = RobotNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
