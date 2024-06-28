#!/bin/bash

# get current time
TIME=$(date +"%Y/%m/%d %H:%M:%S")

# preprocess tags.txt with gcc
gcc -E -x c -DCURRENT_TIME="$TIME PT" tags.txt > custom_tags.txt &&
    echo "Finished preprocessing tags.txt" &&

echo "Now preprocessing..." &&
gcc -E -x c wins.pnml > wins.nml &&
    echo "Finished preprocessing" &&
    echo "Now compiling..." &&
    nml/nmlc wins.nml -o    wins.grf --nml="wins_parsed.nml" &&
    nml/nmlc wins.nml -c -o wins_crop.grf &&
    echo "Finished compiling!"

# if we have an extra copy argument, copy the files to the right place
if [ "$1" == "copy" ]; then
    # path variable
    path="/d/data/documents/openttd/newgrf"
    cp wins.grf $path &&
        echo "Copied wins.grf to ${path}"
fi
