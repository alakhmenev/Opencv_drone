#coding: Utf8
#!/usr/bin/env python
from math import isnan
from math import pi
import rospy
from clover import srv
from std_srvs.srv import Trigger
from clover.srv import SetLEDEffect
from mavros_msgs.srv import CommandBool


rospy.init_node('flight')
get_telemetry = rospy.ServiceProxy('get_telemetry',srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)
set_effect = rospy.ServiceProxy('led/set_effect', SetLEDEffect)
arming = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)

r=rospy.Rate(5)
navigate(x=0, y=0, z=1.5, speed=0.5, frame_id='body', auto_arm=True)
rospy.sleep(3)
z=1.5
while(True):
    navigate(x=0, y=0, z=1.5-z, speed=0.5, frame_id='navigate_target')
    z=1.5
    if isnan(get_telemetry(frame_id='aruco_72').z):
        rospy.sleep(0.2)
        pass


    z=get_telemetry(frame_id='aruco_72').z
    while (z >= 0.3):
        set_position(x=0, y=-0.15, z=z, yaw=pi*0.5, frame_id='aruco_72')
        z = z - 0.05
        r.sleep()

    if (z <= 0.3):
        navigate(x=0, y=0, z=-1, speed=2, frame_id='body')
        rospy.sleep(0.2)
        arming(False)
        break
