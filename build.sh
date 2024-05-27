#!/bin/bash

gcc -E -x c -o wins.nml wins.pnml &&
    echo "Finished preprocessing" &&
    echo "Now compiling..." &&
    nml/nmlc wins.nml -o wins.grf --nml="wins_parsed.nml" &&
    echo "Finished compiling!"
