#!/bin/bash
# Script to run Space Drill Docker container with GUI support

xhost +local:
docker run -it \
  --env DISPLAY=$DISPLAY \
  --volume /tmp/.X11-unix:/tmp/.X11-unix:rw \
  space_drill:latest
