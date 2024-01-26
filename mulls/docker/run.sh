xhost +local:docker

docker run --gpus all --rm -it --name mulls_container --env="DISPLAY" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -v $1:/home mulls_docker