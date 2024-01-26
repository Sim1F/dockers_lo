FROM nvidia/cuda:12.3.1-devel-ubuntu20.04
ENV DEBIAN_FRONTEND=noninteractive
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1

ARG STANDARD_PKG="git vim wget"

ARG LIBRARIES="sudo libeigen3-dev \
 libsuitesparse-dev \
 libqglviewer-dev-qt5 \
 freeglut3-dev \
 libpcl-dev"

# installing all the packages
RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get install -y ${STANDARD_PKG} ${LIBRARIES}

# Manually add the ROS GPG key
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -fsSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    chmod 644 /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list

# Install ROS
RUN apt-get update && apt-get install ros-noetic-desktop-full -y


# Install g++ and python3-pip
RUN apt-get update && apt-get install -y g++ python3-pip

# Create a destination folder inside the image
RUN mkdir app

# Set a build argument for the desired CMake version
ARG CMAKE_VERSION=3.18.2

# Install build dependencies
RUN apt-get update && \
    apt-get install -y build-essential wget

# Download and extract the CMake source code
WORKDIR /build
RUN wget https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}.tar.gz && \
    tar xzf cmake-${CMAKE_VERSION}.tar.gz

# Build and install CMake
WORKDIR /build/cmake-${CMAKE_VERSION}
RUN ./bootstrap && \
    make -j$(nproc) && \
    make install

# Copy the contents of the source folder to the destination folder
COPY kiss-icp/. /app/kiss-icp

# Set the working directory to the python folder
WORKDIR /app/kiss-icp/python

# Install the package using pip
RUN pip install --verbose .

RUN pip install -U rosbags
RUN pip install open3d

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics

#RUN apt-get update && apt-get install -y libgl1

WORKDIR /home

RUN pip install numpy==1.20.3
