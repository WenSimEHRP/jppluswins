#!/bin/bash

# get current time
TIME=$(date +"%Y/%m/%d %H:%M:%S")
TIME=$TIME" PT"

echo "=============== BUILDING WINS ==============="
echo "Current time: $TIME"

if [[ "$1" == "patch" || "$1" == "sample" ]]; then
    echo "Current tile will not be written into the final grf"
    TIME="PATCH"
fi

# preprocess tags.txt with gcc
gcc -E -x c -DCURRENT_TIME="$TIME" tags.txt > custom_tags.txt &&
    echo "Finished preprocessing tags.txt" &&

echo "Now preprocessing..." &&
gcc -E -x c wins.pnml > wins.nml &&
    echo "Finished preprocessing" &&
    echo "Now compiling..." &&
    nml/nmlc wins.nml -o    wins.grf --nml="wins_parsed.nml" &&
    nml/nmlc wins.nml -c -o wins_crop.grf > /dev/null 2>&1 &&
    echo "Finished compiling!"
    # optimize the grf
    ../grf-optimizer/target/release/grf-optimizer.exe ./wins_crop.grf wins_crop_optimized.grf &&
    yagl -d ./wins_crop_optimized.grf > /dev/null 2>&1 &&
    echo "Finished optimizing!"
    # no decompiling console output
    yagl -d wins.grf                    > /dev/null 2>&1 &&
    yagl -d wins_crop.grf               > /dev/null 2>&1 &&
    yagl -d wins_crop_optimized.grf     > /dev/null 2>&1 &&
    echo "Finished yagl decompiling!"
    grfcodec -d wins.grf                > /dev/null 2>&1 &&
    grfcodec -d wins_crop.grf           > /dev/null 2>&1 &&
    grfcodec -d wins_crop_optimized.grf > /dev/null 2>&1 &&
    echo "Finished grfcodec decompiling!"
    # show size of final grf, translate to KiB
    size=$(stat --printf="%s" wins.grf)
    size=$(($size / 1024))
    echo "Final GRF size:     ${size} KiB"
    # size of cropped grf
    size=$(stat --printf="%s" wins_crop.grf)
    size=$(($size / 1024))
    echo "Cropped GRF size:   ${size} KiB"
    # size of optimized grf
    size=$(stat --printf="%s" wins_crop_optimized.grf)
    size=$(($size / 1024))
    echo "Optimized GRF size: ${size} KiB"

if [ "$1" == "sample" ]; then
    echo "Sample mode! will output wins_sample.grf"
    cp wins.grf wins_sample.grf
    cp ./sprites/wins.yagl ./sprites/wins_sample.yagl
fi

if [ "$1" == "patch" ]; then
    echo "Patch mode! will detect decompiled files' md5 checksums"
    # get md5 checksums of decompiled files
    # we then compare them
    checksum=$(md5sum wins.grf | cut -d ' ' -f 1)
    checksum_sample=$(md5sum wins_sample.grf | cut -d ' ' -f 1)
    echo "Checksum of wins.grf:        ${checksum}"
    echo "Checksum of wins_sample.grf: ${checksum_sample}"
    if [ "$checksum" == "$checksum_sample" ]; then
        echo "Checksums match! wins.grf is the same as wins_sample.grf"
    else
        echo "Checksums do not match! wins.grf is different from wins_sample.grf"
        diff ./sprites/wins.yagl ./sprites/wins_sample.yagl
    fi
fi

# if we have an extra copy argument, copy the files to the right place
if [[ "$1" == "copy" || "$2" == "copy" ]]; then
    # path variable
    path="/d/data/documents/openttd/newgrf"
    cp wins_crop_optimized.grf $path &&
        echo "Copied wins_crop_optimized.grf to ${path}"
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
    tar -cvf winspak.tar wins.grf wins_crop.grf wins_crop_optimized.grf LICENSE.txt README.txt &&
    xz -z winspak.tar &&
        echo "packed tarball" &&
    rm README.txt
fi
