
from nav_msgs.msg import Odometry

from tf_transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2
from rclpy.node import Node
import rclpy

from collections import deque


class MovementsQueue():

    def __init__(self, *elements: Point):
        self._elements = deque(elements)

    def enqueue(self, element: Point):
        self._elements.append(element)

    def enqueuelist(self, items: list):
        for el in items:
            self.enqueue(el)

    def dequeue(self):
        return self._elements.popleft()

    def getfirstelement(self):
        return self._elements[0]


class RobotNode(Node):
    x = 0.0
    y = 0.0
    theta = 0.0

    def __init__(self):
        super().__init__("speed_controller")
        self.msg = Twist()

        trash_path = [Point(x=0.55, y=-0.50), Point(x=0.55, y=-1.30), Point(x=1.26, y=-1.30), Point(x=1.26, y=0.30), Point(
            x=1.30, y=0.30), Point(x=3.0, y=0.30), Point(x=3.0, y=4.70), Point(x=1.95, y=4.70), Point(x=1.95, y=2.44)]

        self.goals = MovementsQueue()
        self.goals.enqueuelist(trash_path)

        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.sub = self.create_subscription(
            Odometry, "/odom", self.callback, 10)
        
        self.timer = self.create_timer(0.05, self.send_comand)
        self.get_logger().info("Robot node working on")

    def callback(self, msg):

        rot_q = msg.pose.pose.orientation

        (roll, pitch, theta) = euler_from_quaternion(
            quaternion=[rot_q.x, rot_q.y, rot_q.z, rot_q.w])

        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        self.theta = theta

        self.print_coordinates()

    def print_coordinates(self):
        self.get_logger().info(
            f'\nx: {self.x}\ny: {self.y}\ntheta: {self.theta}')

    def arrived(self):
        self.msg.linear.x = 0.0
        self.msg.angular.z = 0.0
        self.get_logger().info("Arrived at final position")
      

    def send_comand(self):
        if (len(self.goals._elements) != 0):
            goal = self.goals.getfirstelement()

            inc_x = goal.x - self.x
            inc_y = goal.y - self.y

            angle_to_goal = atan2(inc_y, inc_x)

            if abs(self.x - goal.x) < 0.1 and abs(self.y - goal.y) < 0.1:
                self.goals.dequeue()

            if abs(angle_to_goal - self.theta) > 0.1:
                self.msg.linear.x = 0.0
                self.msg.angular.z = .3 if (
                    angle_to_goal - self.theta) > 0.0 else -0.3
            else:
                self.msg.linear.x = 0.5
                self.msg.angular.z = 0.0
        else:
            self.arrived()

        self.pub.publish(self.msg)


def main(args=None):
    rclpy.init(args=args)
    node = RobotNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
