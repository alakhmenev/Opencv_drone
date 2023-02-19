import math
from clover import srv
from std_srvs.srv import Trigger
import rospy
import cv2 as cv
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)
bridge = CvBridge()


image_pub = rospy.Publisher('~debug', Image)


def col(data):
    im = bridge.imgmsg_to_cv2(data, 'bgr8')
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    #print(hsv)
    red_min=(0,100,0)
    red_max=(50,255,50)
    thresh=cv.inRange(im,red_min,red_max)
    moments=cv.moments(thresh,1)
    dM01=moments['m01']
    dM10=moments['m10']
    dArea=moments['m00']
    print(dArea)
    if dArea>1:
        x=int(dM10/dArea)
        y=int(dM01/dArea)
        cv.circle(im, (x,y), 10, (0,0,255), -1)
 
        image_pub.publish(bridge.cv2_to_imgmsg(im, 'bgr8'))

def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=0.5, frame_id='aruco_map', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)

navigate_wait(z=1, frame_id='body', auto_arm=True)
navigate_wait(x=1, y=1, z=1)
image_sub = rospy.Subscriber('main_camera/image_raw', Image, col, queue_size=1)
rospy.sleep(10)

land()
