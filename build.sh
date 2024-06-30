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
    # no decompiling console output
    yagl -d wins.grf      > /dev/null 2>&1 &&
    yagl -d wins_crop.grf > /dev/null 2>&1 &&
    echo "Finished decompiling!"
    # show size of final grf, translate to KiB
    size=$(stat --printf="%s" wins.grf)
    size=$(($size / 1024))
    echo "Final GRF size: ${size} KiB"
    # size of cropped grf
    size=$(stat --printf="%s" wins_crop.grf)
    size=$(($size / 1024))
    echo "Cropped GRF size: ${size} KiB"

# if we have an extra copy argument, copy the files to the right place
if [ "$1" == "copy" ]; then
    # path variable
    path="/d/data/documents/openttd/newgrf"
    cp wins.grf $path &&
        echo "Copied wins.grf to ${path}"
fi

# if we have an extra "release" argument, pack the files into a tarball
# and output it to the current directory
if [ "$1" == "release" ]; then
    cp README.md README.txt &&
    tar -cvf winsrel.tar wins_crop.grf LICENSE.txt README.txt &&
        echo "packed tarball" &&
    rm README.txt
fi

# if we have an extra "pack" argument then pack all files into a .tar.xz archive
if [ "$1" == "pack" ]; then
    cp README.md README.txt &&
    tar -cvf winspak.tar wins.grf wins_crop.grf LICENSE.txt README.txt &&
    xz -z winspak.tar &&
        echo "packed tarball" &&
    rm README.txt
fi
