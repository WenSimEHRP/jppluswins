#!/usr/bin/env python3
import yaml


def read(filename):
    with open(filename, "r") as f:
        return yaml.safe_load(f)


def create_index(cat, item, prev_ind, fw):
    size = item["size"]
    num_sets = len(item["items"])
    print(f"const pos_{cat}_start = {prev_ind};", file=fw)
    print(f"const id_{cat}_size = {size};", file=fw)
    counter = 0
    for key in item["items"]:
        for k in key:
            print(f"const id_{cat}_{k} = {counter};", file=fw)
        counter += 1
    return prev_ind + size * num_sets


def write_spriteset(item, fw):
    for key in item["items"]:
        for v in key.values():
            print(f"    {v}", file=fw)

y = read("src/spritesets.yml")

prev_ind = 0
with open("generated/spritesets.nml", "w+") as fw:
    for key, val in y.items():
        prev_ind = create_index(key, val, prev_ind, fw)
        print(file=fw)
    print("spriteset(s_fences_and_underlay, ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP,){", file=fw)
    for key, val in y.items():
        write_spriteset(val, fw)
    print("}", file=fw)
