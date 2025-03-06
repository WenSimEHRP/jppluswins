NAME := "wins"

def:
    @just --list

# build the newgrf (debug, no crop)
build: preprocess
    ./nml/nmlc {{NAME}}.nml --grf {{NAME}}.grf --nml {{NAME}}_parsed.nml --nfo={{NAME}}.nfo
    @echo "All jobs done"
    @du -bh {{NAME}}.nml
    @du -bh {{NAME}}.grf
    @du -bh {{NAME}}.nfo

# build the newgrf (release, crop)
release: preprocess
    ./nml/nmlc -c {{NAME}}.nml --grf {{NAME}}.grf
    @echo "All jobs done"
    @du -bh {{NAME}}.nml
    @du -bh {{NAME}}.grf

# preprocess the pnml file
preprocess:
    gcc -E -x c {{NAME}}.pnml \
        -D COMMIT="$(git rev-list --count HEAD || echo 1145)" \
        -D MIN_COMMIT="$(git rev-list --count "$(cat min_compatible_version)" || echo 1)" \
        > {{NAME}}.nml

# set up nml
setup:
    rm -rf ./nml
    git clone --depth 1 https://github.com/openttd/nml.git || true
    cd nml && git pull

# copy the grf to the openttd newgrf folder (linux)
cp:
    cp {{NAME}}.grf ~/.local/share/openttd/newgrf/

# clean up
clean:
    rm *.grf
    rm *.nml
    rm *.nfo
    rm -rf ./.nmlcache
