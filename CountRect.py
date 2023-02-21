# -*- coding: utf-8 -*-

import rospy
from clover import srv
from std_srvs.srv import Trigger
import math
import cv2 
import numpy as np
import matplotlib.pyplot as plt
import time
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import sys
import imutils


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

image_pub = rospy.Publisher('~RECOGNIZE', Image)


def nav(x=0, y=0, z=0, yaw=float('nan'), speed=0.5, frame_id='aruco_map', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)

def ima(data):
    global rgb, cnt, image, box, contours0, total, kernel, closed
    image = bridge.imgmsg_to_cv2(data, 'bgr8')  
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (11, 11), 0)
    canny = cv2.Canny(blur, 10, 250)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)
    #hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV )
    #thresh = cv2.inRange( hsv, hsv_min, hsv_max ) 
    #(cnt, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    total = 0
    for c in cnts:
        # аппроксимируем (сглаживаем) контур
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # если у контура 4 вершины, предполагаем, что это книга
        if len(approx) > 2:
            cv2.drawContours(image, [approx], -1, (0, 255, 0), 4)
            total += 1
    #contours0, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #cv2.drawContours(rgb, cnt, -1, (0, 255, 0), 2)
    #for cnt in contours0:
        #rect = cv2.minAreaRect(cnt) # пытаемся вписать прямоугольник
        #box = cv2.boxPoints(rect) # поиск четырех вершин прямоугольника
        #box = np.int0(box) # округление координат
        #cv2.drawContours(image,[box],0,(255,0,0),2) # рисуем прямоугольник

    image_pub.publish(bridge.cv2_to_imgmsg(image, 'bgr8'))

def rec():
    global image, kernel, closed
    cv2.imshow('contours', image)
    
    cv2.imshow('kernel', kernel)
    
    cv2.imshow('closed', closed)
    cv2.waitKey()
    cv2.destroyAllWindows()




image_sub = rospy.Subscriber('main_camera/image_raw', Image, ima)
 

nav(z=1, frame_id='body', auto_arm=True)
rec()
print("Я нашёл {0}" .format(total))
rospy.sleep(7)
land()