#!/bin/bash
pip3 install -r requirements.txt &&
    echo "Finished installing dependencies" &&
echo "Now cloning nml..."
git clone https://github.com/openttd/nml &&
    echo "Finished cloning nml" &&
    echo "Now merging..." &&
    cd nml &&
    git config user.name "anonymous" &&
    git config user.email "anonymous@example.com" &&
    git remote add pr_source https://github.com/glx22/nml &&
    git fetch pr_source layout_registers &&
    git fetch pr_source var6B &&
    git merge -X ours pr_source/layout_registers -m "Merge layout_registers" &&
    git merge -X ours pr_source/var6B -m "Merge var6B" &&
    echo "Finished merging"
