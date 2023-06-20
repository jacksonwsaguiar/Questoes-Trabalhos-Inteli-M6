
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import requests

class ImageSubscriberNode(Node):

    def __init__(self):
        super().__init__("image_subscriber")
        self.sub = self.create_subscription(Image, "images", self.callback, 10)
        self.bridge = CvBridge()

    def callback(self, data):
        self.get_logger().info('Receiving image frame')
        current_frame = self.bridge.imgmsg_to_cv2(data)

        _, img_encoded = cv2.imencode('.jpg', current_frame)
        frame_data = img_encoded.tobytes()

        headers = {"Content-type": 'form/octet-stream'}
        
        url = "http://localhost:8080/upload"

        response = requests.post(url, data = frame_data, headers=headers)

        if response.ok:
            print('Frame sent successfully!')
        else:
            print('Failed to send frame. Status code:', response.status_code)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
        return
    
def main(args=None):
  
  rclpy.init(args=args)
  image_subscriber = ImageSubscriberNode()
  rclpy.spin(image_subscriber)
  image_subscriber.destroy_node()
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()