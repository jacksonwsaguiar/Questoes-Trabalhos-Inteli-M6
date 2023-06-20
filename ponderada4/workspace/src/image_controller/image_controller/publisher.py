import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

INPUT = '/home/jacksonaguiar/Questoes-Trabalhos-Inteli-M6/ponderada4/workspace/src/image_controller/image_controller/resources/power_rangers_morph.mp4'


class ImagePublisherNode(Node):

    def __init__(self):
        super().__init__("image_publisher")

        self.pub = self.create_publisher(Image, "images", 10)
        self.timer = self.create_timer(1, self.callback)
        self.input = cv2.VideoCapture(INPUT)
        self.bridge = CvBridge()
        self.get_logger().info("Publisher image node working on")

    def callback(self):
        ret, frame = self.input.read()

        if not ret:
            self.get_logger().info("Video seems to be over. Restarting...")
            self.input = cv2.VideoCapture(INPUT)
            return

        self.pub.publish(self.bridge.cv2_to_imgmsg(frame))

        self.get_logger().info('Publishing video frame...')


def main(args=None):

    rclpy.init(args=args)
    image_publisher = ImagePublisherNode()
    rclpy.spin(image_publisher)
    image_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
