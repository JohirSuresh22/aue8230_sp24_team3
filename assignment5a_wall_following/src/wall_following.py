#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class WallFollower:
    def __init__(self):
        rospy.init_node('wall_follower')
        self.move = Twist()
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.sub = rospy.Subscriber("/scan", LaserScan, self.wallfollow)
    
    def PID(self, error, error_prev, Kp=0.9, Kd=1):
      
        return Kp * error + Kd*(error-error_prev)
    
    def wallfollow(self, data):
        lidar_scan = list(data.ranges[0:359])
        scan = [x for x in lidar_scan if x < 3]     # Filtering garbage values
        
        right = sum(scan[-90:-16])/len(scan[-90:-16])   # Average range
        left = sum(scan[16:90])/len(scan[16:90])        # Average range
         
        linear_vel = 0.4
        angular_vel = 0
        
        error = left - right
        error_prev = error
        
        self.move.linear.x = linear_vel
        self.move.angular.z = angular_vel + self.PID(error, error_prev) # Yaw PD control
        print("Angular Velocity is %s" % self.move.angular.z)
        
    def run(self):
        while not rospy.is_shutdown():
            self.pub.publish(self.move)
    
if __name__ == "__main__":
    wall_follower = WallFollower()
    wall_follower.run()