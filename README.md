# WINS Is Not (only) Stations

![wakatime](https://wakatime.com/badge/user/3ccfe070-205f-4eef-826d-419a0ac19311/project/1f5ff741-a34c-4481-9c9f-e8379ed1e9b6.svg)
[![buidling status](https://github.com/wensimehrp/jppluswins/actions/workflows/build.yml/badge.svg)](https://github.com/wensimehrp/jppluswins/actions/workflows/build.yml)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

---

This is not yet JP+ Stations, but I'm working on the sprites - and maybe there will be some advanced stuff added in the future (auto platforms, buffers, also passenger and cargo on station platforms, etc.)

This set features a set of Japanese style platforms. Some of them are not based on Japanese stations though, rather they are based off SkyTrain systems.

## Features

- [JP+ Tracks](https://github.com/OpenTTD-JPplus/JPplusTracks)-compatible assets
  - Fences
  - Grass underlay
  - Marshalling yards
  - Catenary wires
- Extra railroad decorations
  - Catenary tensioners
  - Automatic buffers (as in CHIPS)

## Translating

Always maintained:

- en_GB
- zh_CN

These languages are not maintained by the author:

- _(none)_

## Building

Requirements:

- just
- gcc
- git
- sh (use git bash on windows)

```sh
# set up nml dependency
just setup

# build a "release" version of the GRF
just release

# pack
just pack

# or do it in one run
just setup release pack
```
