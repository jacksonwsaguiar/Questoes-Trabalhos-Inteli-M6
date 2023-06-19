import rclpy
import cv2
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ultralytics import YOLO


INPUT = "/home/jacksonaguiar/Questoes-Trabalhos-Inteli-M6/ponderada3/workspace/src/cv_controller/cv_controller/resources/test.mp4"
OUTPUT = "/home/jacksonaguiar/Questoes-Trabalhos-Inteli-M6/ponderada3/workspace/src/cv_controller/cv_controller/output/out.avi"
MODEL_PATH = "/home/jacksonaguiar/Questoes-Trabalhos-Inteli-M6/ponderada3/workspace/src/cv_controller/cv_controller/model/best.pt"


class CVNode(Node):

    def __init__(self):
        super().__init__("computer_vision_node")
        self.timer = self.create_timer(0.1, self.callback)
        self.cap = cv2.VideoCapture(INPUT)

        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # float `width`
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        self.output = cv2.VideoWriter(
            OUTPUT, cv2.VideoWriter_fourcc(*'DIVX'), 24, (width, height))
        
    def callback(self):
        if not self.cap.isOpened():
            self.get_logger().error("Cannot load video. restarting...")
            self.cap = cv2.VideoCapture(INPUT)

        ret, frame = self.cap.read()
        if ret:

            model = YOLO(MODEL_PATH)

            self.get_logger().info("Predicting...")

            res = model.predict(frame, conf=0.65)
            res_plotted = res[0].plot()

            self.output.write(res_plotted)

        else:
            self.output.release()
            self.get_logger().info("Finish prediction.")
            self.get_logger().info("Video proccessed saved in output...")
            exit()


def main(args=None):
    rclpy.init(args=args)
    node = CVNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
