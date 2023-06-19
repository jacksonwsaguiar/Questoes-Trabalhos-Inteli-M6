import rclpy
import cv2
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ultralytics import YOLO
INPUT = "./assets/test.mp4"


class CVNode(Node):

    def __init__(self):
        super().__init__("computer_vision_webcam")
        self.publisher_ = self.create_publisher(Image, 'video_frames', 10)
        self.timer = self.create_timer(0.1, self.callback)
        self.cap = cv2.VideoCapture(INPUT)
        self.cv_bridge = CvBridge()
        self.counter = 0

    def callback(self):
        if not self.cap.isOpened():
            self.get_logger().error("Cannot load video. restarting...")
            self.cap = cv2.VideoCapture(INPUT)

        ret, frame = self.cap.read()
        if ret:
            self.publisher_.publish(
                self.cv_bridge.cv2_to_imgmsg(frame))  # encodeing mode is also bgr8

            # model = YOLO("./model/best.pt")
        
            # self.get_logger().error("Predicting...")
            
            # res = model.predict(frame, conf=0.6)
            # res_plotted = res[0].plot()

            cv2.imshow("Crack detection", self.cv_bridge.cv2_to_imgmsg(frame))
            cv2.waitKey(1)
        else:
            self.get_logger().error("Can't receive frame. Exiting ...")
            exit()

        self.get_logger().info("Publishing video frame [#%04d]" % self.counter)
        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = CVNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
