#Victor Ruest
#ros package shell. going to adapt for fsm_node

import rclpy
from rclpy.node import Node
import cv2
from sensor_msgs.msg import Image, LaserScan
from cv_bridge import CvBridge
import numpy as np
import math

class LidarOffice(Node):
    def __init__(self):
        super().__init__('lidar_office')
        self.subscription = self.create_subscription(LaserScan, 'scan',
            self.listener_callback, 10)
        self.subscription # prevent unused variable warning
        self.publisher = self.create_publisher(Image, 'lidar_image', 10)
        self.bridge = CvBridge()

    def listener_callback(self, msg):
        #create image for every scan
        output_image = np.zeros([600, 600], np.uint8)

        for i, distance in enumerate(msg.ranges):
            #draw image if value is positive and less than/equal 12 meters
            if 0 < distance <= 12:
                object_angle = msg.angle_min +(i * msg.angle_increment) #angle_increment(constant) * how many times it increments 

                #use polar to get cartesian x and y, then convert meters to pixels
                cartesian_x = int(distance * math.cos(object_angle) * 25)
                cartesian_y = int(distance * math.sin(object_angle) * 25)
                
                #mapping to center
                x_coordinate = 300 + cartesian_x
                y_coordinate = 300 - cartesian_y #image starts in upper left corner at (0,0) so going up has us subtracting

                #draw each dot where it lies on output_image
                cv2.circle(output_image,(x_coordinate,y_coordinate), 1, 255, -1) 
        
        #convert cv2 to image message
        lidar_image = self.bridge.cv2_to_imgmsg(output_image, encoding = "mono8")

        self.publisher.publish(lidar_image)

def main(args = None):
    rclpy.init(args = args)

    lidar_office = LidarOffice()

    rclpy.spin(lidar_office)

if __name__ == '__main__':
    main()
