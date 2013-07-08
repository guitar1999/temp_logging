#!/bin/bash

status0=$(cat /mnt/1wire/EF.9F8C20150000/hub/branch.0)
if [ "$status0" = "0" ]
then
    echo "1" > /mnt/1wire/EF.9F8C20150000/hub/branch.0
fi
