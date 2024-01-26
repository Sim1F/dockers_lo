#!/usr/bin/env python3

import rospy
import rosbag
from sensor_msgs.msg import PointCloud2
from sensor_msgs.point_cloud2 import create_cloud_xyz32
import numpy as np

def convert_livox_to_pointcloud2(input_bagfile, output_bagfile):
    with rosbag.Bag(input_bagfile, 'r') as input_bag, rosbag.Bag(output_bagfile, 'w') as output_bag:
        for topic, msg, t in input_bag.read_messages(topics=['/livox/lidar']):
            # Extract Livox point cloud data from the message
            points = []
            for custom_point in msg.points:
                x = custom_point.x
                y = custom_point.y
                z = custom_point.z
                # You can access other fields like reflectivity, tag, and line if needed
                points.append([x, y, z])

            # Create a PointCloud2 message
            pc2_msg = create_cloud_xyz32(msg.header, points)

            # Write the PointCloud2 message to the output bag file
            output_bag.write('/livox/pointcloud2', pc2_msg, t)

if __name__ == '__main__':
    rospy.init_node('convert_livox_to_pointcloud2')
    input_bagfile = 'uzh_tracking_area_run2.bag'
    output_bagfile = 'livox_pointcloud.bag'
    convert_livox_to_pointcloud2(input_bagfile, output_bagfile)