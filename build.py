#!/usr/bin/env python3
import yaml
import re

check_temps = re.compile(r"LOAD_TEMP\((\w+)\)")

platforms = ("src/platforms.yml",)

with open("src/parts.yml", "r") as f:
    tem = yaml.safe_load(f)


def layout(name: str, val: dict) -> list:
    kw = set()
    for direction in ("x", "y"):
        print(f"spritelayout sp_{key}_{direction}(){{", file=fw)
        for i in val:
            a, b = i.split(".")
            d = tem[a][b][direction]
            kw |= set(re.findall(check_temps, d))
            print(d, file=fw)
        print("}", file=fw)
    return sorted(kw)


with open("generated/platforms.nml", "w+") as fw:
    for p in platforms:
        with open(p, "r") as f:
            for ind, val in enumerate(sorted(tem["temps"].keys())):
                print(f"const {val} = {ind+10};", file=fw)
            data = yaml.safe_load(f)
            for key, val in data.items():
                temps = layout(key, val["layout"])
                print(f"switch(FEAT_STATIONS, SELF, sw_item_{key}_prepare, [", file=fw)
                for t in temps:
                    print(f"STORE_TEMP({tem['temps'][t]}, {t}),", file=fw)
                print("]){return;}", file=fw)
                print(f"item(FEAT_STATIONS, i_{key}){{", file=fw)
                print(
                    """
    property {
        class: "WINS";
        classname: string(STR_GRF_NAME);
        name: string(STR_GRF_NAME);
        tile_flags: [
            1,1,1,1,1,1,1,1,
        ];
    }""",
                    file=fw,
                )
                print(
                    f"""
    graphics {{
        prepare_layout: sw_item_{key}_prepare();
        custom_spritesets: [s_fences_and_underlay];
        sprite_layouts: [sp_{key}_x, sp_{key}_y];
    }}""",
                    file=fw,
                )
                print("}", file=fw)
