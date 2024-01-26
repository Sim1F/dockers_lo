# xhost +local:docker

# docker run --gpus all --rm -it --name mulls_container --env="DISPLAY" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -v $1:/home mulls_docker

xhost +si:localuser:root

docker run --gpus all --rm -it --privileged --name mulls_container -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $1:/home -v $2:/mulls mulls_docker