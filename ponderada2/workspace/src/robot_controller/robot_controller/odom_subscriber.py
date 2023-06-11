#! usr/bin/env python3
import rclpy
import time
from rclpy.node import Node
from nav_msgs.msg import Odometry


class PoseSubscriberNode(Node):

    def __init__(self):
        super().__init__("robot_node")
        self.pose_subscriber = self.create_subscription(Odometry, "/odom", self.callback, 10)
        self.get_logger().info("Robot Subscriber node working on - reading odom values:")

    def callback(self, msg: Odometry):
        self.get_logger().info(str(msg))
        time.sleep(2)
        return

 
def main(args=None):
    rclpy.init(args=args)
    node = PoseSubscriberNode()
    rclpy.spin(node)
    rclpy.shutdown()


# if __name__ == "__main__":
#     main()
