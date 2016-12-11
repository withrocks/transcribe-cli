#!/bin/bash

set -e
./play-bit.py $1 $2 $3 $4 > /dev/null 2>&1 &
subprocess=$!

vim $1_$3.txt

echo "Finished editing, stopping track"
kill -9 $subprocess


# TODO: Not able to kill the subprocess!!!!
# find out why, until then:
pkill -f $1 > /dev/null 2>&1


