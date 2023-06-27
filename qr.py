import rospy
from pyzbar import pyzbar
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import rospy
from clover import srv
from std_srvs.srv import Trigger

bridge = CvBridge()

rospy.init_node('barcode_test')
image_pub = rospy.Publisher('~debug', Image)

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

# Image subscriber callback function
def image_callback(data):
    cv_image = bridge.imgmsg_to_cv2(data, 'bgr8')  # OpenCV image
    barcodes = pyzbar.decode(cv_image)
    for barcode in barcodes:
        b_data = barcode.data.decode("utf-8")
       # b_type = barcode.type
        (x, y, w, h) = barcode.rect
        xc = x + w/2
        yc = y + h/2
        print("{}".format(b_data))
        image_pub.publish(bridge.cv2_to_imgmsg(cv_image, 'bgr8'))
    if b_data == ("{}".format(b_data)):
      land()
image_sub = rospy.Subscriber('main_camera/image_raw', Image, image_callback, queue_size=1)

navigate(x=0, y=0, z=1.5, speed=0.5, frame_id='body', auto_arm=True)
rospy.sleep(15)