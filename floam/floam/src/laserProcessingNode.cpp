// Author of FLOAM: Wang Han 
// Email wh200720041@gmail.com
// Homepage https://wanghan.pro

//c++ lib
#include <cmath>
#include <vector>
#include <mutex>
#include <queue>
#include <thread>
#include <chrono>

//ros lib
#include <ros/ros.h>
#include <sensor_msgs/Imu.h>
#include <sensor_msgs/PointCloud2.h>
#include <nav_msgs/Odometry.h>
#include <tf/transform_datatypes.h>
#include <tf/transform_broadcaster.h>

//pcl lib
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>

//local lib
#include "lidar.h"
#include "laserProcessingClass.h"


LaserProcessingClass laserProcessing;
std::mutex mutex_lock;
std::queue<sensor_msgs::PointCloud2ConstPtr> pointCloudBuf;
lidar::Lidar lidar_param;

ros::Publisher pubEdgePoints;
ros::Publisher pubSurfPoints;
ros::Publisher pubLaserCloudFiltered;

void velodyneHandler(const sensor_msgs::PointCloud2ConstPtr &laserCloudMsg)
{
    std::cout << "Arrived new msg!" << std::endl;
    mutex_lock.lock();
    pointCloudBuf.push(laserCloudMsg);
    mutex_lock.unlock();
   
}

double total_time =0;
int total_frame=0;

void laser_processing(){
    std::cout << "Laser processing" << std::endl;
    while(1){
        if(!pointCloudBuf.empty()){
            std::cout << "Reading data: " << pointCloudBuf.size() << std::endl;
            //read data
            mutex_lock.lock();
            std::cout << "Uno" << std::endl;
            pcl::PointCloud<pcl::PointXYZI>::Ptr pointcloud_in(new pcl::PointCloud<pcl::PointXYZI>());
            std::cout << "Uno" << std::endl;

            std::cout << "size: " << pointCloudBuf.front()->data.size() << std::endl;
            std::cout << "height: " << pointCloudBuf.front()->height << std::endl;
            std::cout << "width: " << pointCloudBuf.front()->width << std::endl;
            std::cout << "header.seq: " << pointCloudBuf.front()->header.seq << std::endl;
            std::cout << "header.stamp: " << pointCloudBuf.front()->header.stamp << std::endl;
            std::cout << "header.frame_id: " << pointCloudBuf.front()->header.frame_id << std::endl;
            std::cout << "point_step: " << pointCloudBuf.front()->point_step << std::endl;
            std::cout << "row_step: " << pointCloudBuf.front()->row_step << std::endl;

            sensor_msgs::PointCloud2 output_cloud;
            output_cloud.header = pointCloudBuf.front()->header;

            output_cloud.height = pointCloudBuf.front()->height;
            output_cloud.width = pointCloudBuf.front()->width;

            output_cloud.fields = pointCloudBuf.front()->fields;

            output_cloud.is_bigendian = pointCloudBuf.front()->is_bigendian;
            output_cloud.point_step = pointCloudBuf.front()->point_step;
            output_cloud.row_step = output_cloud.width * output_cloud.point_step;
            output_cloud.data = pointCloudBuf.front()->data;

            output_cloud.is_dense = pointCloudBuf.front()->is_dense;

            pcl::fromROSMsg(output_cloud, *pointcloud_in);
            std::cout << "Uno" << std::endl;
            ros::Time pointcloud_time = (pointCloudBuf.front())->header.stamp;
            std::cout << "Uno" << std::endl;
            pointCloudBuf.pop();
            std::cout << "Uno" << std::endl;
            mutex_lock.unlock();

            std::cout << "Uno" << std::endl;

            pcl::PointCloud<pcl::PointXYZI>::Ptr pointcloud_edge(new pcl::PointCloud<pcl::PointXYZI>());          
            pcl::PointCloud<pcl::PointXYZI>::Ptr pointcloud_surf(new pcl::PointCloud<pcl::PointXYZI>());

            std::chrono::time_point<std::chrono::system_clock> start, end;
            start = std::chrono::system_clock::now();
            laserProcessing.featureExtraction(pointcloud_in,pointcloud_edge,pointcloud_surf);
            end = std::chrono::system_clock::now();
            std::chrono::duration<float> elapsed_seconds = end - start;
            total_frame++;
            float time_temp = elapsed_seconds.count() * 1000;
            total_time+=time_temp;
            //ROS_INFO("average laser processing time %f ms \n \n", total_time/total_frame);

            std::cout << "Due" << std::endl;

            sensor_msgs::PointCloud2 laserCloudFilteredMsg;
            pcl::PointCloud<pcl::PointXYZI>::Ptr pointcloud_filtered(new pcl::PointCloud<pcl::PointXYZI>());  
            *pointcloud_filtered+=*pointcloud_edge;
            *pointcloud_filtered+=*pointcloud_surf;
            pcl::toROSMsg(*pointcloud_filtered, laserCloudFilteredMsg);
            laserCloudFilteredMsg.header.stamp = pointcloud_time;
            laserCloudFilteredMsg.header.frame_id = "base_link";
            pubLaserCloudFiltered.publish(laserCloudFilteredMsg);

            std::cout << "Tre" << std::endl;

            sensor_msgs::PointCloud2 edgePointsMsg;
            pcl::toROSMsg(*pointcloud_edge, edgePointsMsg);
            edgePointsMsg.header.stamp = pointcloud_time;
            edgePointsMsg.header.frame_id = "base_link";
            pubEdgePoints.publish(edgePointsMsg);

            std::cout << "Quattro" << std::endl;


            sensor_msgs::PointCloud2 surfPointsMsg;
            pcl::toROSMsg(*pointcloud_surf, surfPointsMsg);
            surfPointsMsg.header.stamp = pointcloud_time;
            surfPointsMsg.header.frame_id = "base_link";
            pubSurfPoints.publish(surfPointsMsg);

            std::cout << "END Reading data" << std::endl;
        }
        //sleep 2 ms every time
        std::chrono::milliseconds dura(2);
        std::this_thread::sleep_for(dura);
    }
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "main");
    ros::NodeHandle nh;

    int scan_line = 128;
    double vertical_angle = 2.0;
    double scan_period= 0.1;
    double max_dis = 60.0;
    double min_dis = 2.0;
    std::string cloud_topic_name = "/ouster/points";

    nh.getParam("/scan_period", scan_period); 
    nh.getParam("/vertical_angle", vertical_angle); 
    nh.getParam("/max_dis", max_dis);
    nh.getParam("/min_dis", min_dis);
    nh.getParam("/scan_line", scan_line);
    nh.getParam("/point_cloud_topic", cloud_topic_name);

    std::cout << "scan_period: " << scan_period << std::endl;
    std::cout << "vertical_angle: " << vertical_angle << std::endl;
    std::cout << "max_dis: " << max_dis << std::endl;
    std::cout << "min_dis: " << min_dis << std::endl;
    std::cout << "scan_line: " << scan_line << std::endl;
    std::cout << "cloud_topic_name: " << cloud_topic_name << std::endl;

    lidar_param.setScanPeriod(scan_period);
    lidar_param.setVerticalAngle(vertical_angle);
    lidar_param.setLines(scan_line);
    lidar_param.setMaxDistance(max_dis);
    lidar_param.setMinDistance(min_dis);

    laserProcessing.init(lidar_param);

    ros::Subscriber subLaserCloud = nh.subscribe<sensor_msgs::PointCloud2>(cloud_topic_name, 100, velodyneHandler);

    pubLaserCloudFiltered = nh.advertise<sensor_msgs::PointCloud2>("/velodyne_points_filtered", 100);

    pubEdgePoints = nh.advertise<sensor_msgs::PointCloud2>("/laser_cloud_edge", 100);

    pubSurfPoints = nh.advertise<sensor_msgs::PointCloud2>("/laser_cloud_surf", 100); 

    std::thread laser_processing_process{laser_processing};

    ros::spin();

    return 0;
}

