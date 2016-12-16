#!/bin/bash

sudo apt-get install owfs owfs-fuse python-ow
sudo mkdir /mnt/1wire
sudo owfs --allow_other -u -m /mnt/1wire/
