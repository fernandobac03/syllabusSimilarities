#!/bin/bash


#stop and remove container
docker stop comparingtext
docker rm comparingtext

#remove image
docker rmi comparingtext

#build new image 
docker build -t comparingtext .
