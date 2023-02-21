# -*- coding: utf-8 -*-

#import rospy
#from clover import srv
#from std_srvs.srv import Trigger
import math
import cv2 
import numpy as np
import matplotlib.pyplot as plt
import time
#from sensor_msgs.msg import Image
#from cv_bridge import CvBridge


#rospy.init_node('flight')
'''
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)
bridge = CvBridge()
'''
#image_pub = rospy.Publisher('~RECOGNIZE', Image)


def nav(x=0, y=0, z=0, yaw=float('nan'), speed=0.5, frame_id='aruco_map', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)

def ima():
    #image = bridge.imgmsg_to_cv2(data, 'bgr8')  
    image = cv2.imread('\image\test.jpg')
    print(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (11, 11), 0)
    canny = cv2.Canny(blur, 30, 150, 3)
    dilated = cv2.dilate(canny, (1, 1), iterations=0)
    (cnt, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.drawContours(rgb, cnt, -1, (0, 255, 0), 2)
    plt.imshow(rgb)
    plt.show()
    print("coins in the image : ", len(cnt))
    
    #image_pub.publish(bridge.cv2_to_imgmsg(gray, 'bgr8'))

##image_sub = rospy.Subscriber('main_camera/image_raw', Image, ima)
 
ima()
time.sleep(2)
#nav(z=1, frame_id='body', auto_arm=True)

