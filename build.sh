#!/bin/bash

# get current time
TIME=$(date +"%Y/%m/%d %H:%M:%S")

# preprocess tags.txt with gcc
gcc -E -x c -DCURRENT_TIME="$TIME PT" -o custom_tags.txt tags.txt &&
    echo "Finished preprocessing tags.txt" &&

echo "Now preprocessing..." &&
gcc -E -x c -o wins.nml wins.pnml &&
    echo "Finished preprocessing" &&
    echo "Now compiling..." &&
    nml/nmlc wins.nml -o wins.grf --nml="wins_parsed.nml" &&
    echo "Finished compiling!"
