#!/bin/bash
pip3 install -r requirements.txt &&
    echo "Finished installing dependencies" &&
echo "Now cloning nml..."
git clone https://github.com/openttd/nml &&
    cd nml &&
    git checkout 3739dd40029a3a61303f1d43529b4504b56348c5 &&
    echo "Finished cloning NML"
