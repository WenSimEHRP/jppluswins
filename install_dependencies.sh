#!/bin/bash
pip3 install -r requirements.txt &&
    echo "Finished installing dependencies" &&
echo "Now cloning nml..."
git clone https://github.com/openttd/nml &&
    cd nml &&
    git checkout dcbfdc7a771e6b3033a9e09c656ac3c441f466db &&
    echo "Finished cloning NML"
