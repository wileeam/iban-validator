#!/bin/sh

docker run -p 80:5000 --rm -it $(docker build -q .)
