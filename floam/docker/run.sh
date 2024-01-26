# xhost +local:docker

# docker run --gpus all --rm -it --name floam_container --env="DISPLAY" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -v $1:/catkin_ws/src/floam -v $2:/home floam_docker

xhost +si:localuser:root

docker run --gpus all --rm -it --privileged --name floam_container -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $1:/catkin_ws/src/floam -v $2:/home floam_docker