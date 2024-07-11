# JP+ WINS Is Not Stations

This project aims to a total replacement of JP3 stations and is currently in active development.
Made by WenSim. Licensed under GPL 2.

## Features

- Swappable platform material
- Automatic buffers
- Automatic fences
- Cargo sprite randomization (hoho thanks ISR)
- (Currently) much smaller than JP3 stations - ~204KB vs ~5.97MB, at a size around 3% of JP3 stations (wow, does that also count?)
- can't remember the rest

## Building

To build the GRF, you should have these subjects installed;

- bash
- nml
- gcc
- python

Note: you should be able to access `bash` after you installed `git` if you are on Windows.\
You could use `install_dependencies.sh` to quickly install nml and its requirements.

Please note that this grf requires the latest version of NML. It is recommended to install
NML using the install script.

After installing all dependencies, you should be able to build the grf by running `build.sh`.

Additionally, you can create a release package by running `bash build.sh release`, or, a compressed archive by running `bash build.sh pack`. Note that `xz` is required for the latter operation.

## Credits

Contributors:

- Japan Set Team
- WenSim

Translations:

- If you want to translate the GRF to your own language, feel free to submit a translation PR or submit translations via an issue.
