FROM osrf/ros:melodic-desktop-full-bionic 


# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics

# install GLX-Gears
RUN apt-get update && apt-get install -y --no-install-recommends mesa-utils x11-apps && rm -rf /var/lib/apt/lists/*

RUN apt-get install -y ros-melodic-pcl-ros

# Install Eigen3
RUN apt-get install -y libeigen3-dev

# Set up ROS environment
RUN echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc

# Install Ceres Solver
RUN apt-get update && apt-get install -y libceres-dev

# Set C++ version to 14
#RUN echo "export CXX=/usr/bin/g++-9" >> ~/.bashrc

# Install PCL
#RUN apt-get install -y libpcl-dev

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /catkin_ws/src
WORKDIR /catkin_ws

# Copy your repository files to the Docker image
COPY ../ /catkin_ws/src/floam

# Build the ROS package
RUN /bin/bash -c "source /opt/ros/melodic/setup.bash && \
                  catkin_make"

RUN apt-get update && apt-get install -y ros-melodic-hector-trajectory-server

RUN apt-get install -y x11-utils
ENV DISPLAY=:0