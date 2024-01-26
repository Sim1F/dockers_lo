xhost +si:localuser:root

docker run --gpus all --rm -it --privileged --name kiss_icp_container -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $1:/home -v $2:/app/kiss-icp kiss_icp_docker

