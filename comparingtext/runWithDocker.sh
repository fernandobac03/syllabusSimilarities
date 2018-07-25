#!/bin/bash

docker stop comparingtext
docker rm comparingtext

docker run -d --name comparingtext -p 5000:5000 comparingtext
