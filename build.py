#!/usr/bin/env python3
# filepath: /home/jeremyg/code/jppluswins/build.py
import yaml
import re
from item_template import item_templates

check_temps = re.compile(r"LOAD_TEMP\((\w+)\)|EXTRACT_INFO\((.*?),.*?\)")

PLATFORMS = ("src/platforms.yml",)


def load_templates():
    with open("src/parts.yml", "r") as f:
        return yaml.safe_load(f)


def layout(key, val_layout, templates, fw):
    kw = set()
    for direction in ("x", "y"):
        print(f"spritelayout sp_{key}_{direction}(){{", file=fw)
        for i in val_layout:
            a, b = i.split(".")
            d = templates[a][b][direction]
            for i in re.findall(check_temps, d):
                kw |= set(j for j in i if j.strip())
            print(d, file=fw)
        print("}", file=fw)
    return sorted(kw)


def write_constants(templates, fw):
    for ind, val in enumerate(sorted(templates["temps"].keys())):
        print(f"const {val} = {ind + 10};", file=fw)


def process_item(key, val, templates, fw):
    temps = layout(key, val["layout"], templates, fw)
    registers = ""
    for t in temps:
        registers += f"STORE_TEMP({templates['temps'][t]}, {t}),\n"

    sprite_layouts = f"[sp_{key}_x, sp_{key}_y]"
    misc = ""
    if "preview" in val:
        sprite_layouts = f"[sp_{key}_x, sp_{key}_y, sp_preview({val['preview'] * 2}), sp_preview({val['preview'] * 2 + 1})]"
        misc += "\nselect_sprite_layout: 0;"
        misc += "\npurchase_select_sprite_layout: 2;"

    printstr = item_templates[val.get("template", "default")].substitute(
        name=key,
        name_label=val.get("name_label", "DEFAULT"),
        temps=registers,
        sprite_layouts=sprite_layouts,
        class_label=val.get("class_label", "WINS"),
        class_name=val.get("class_name", "STR_CLASS_WINS"),
        misc=misc
    )
    print(printstr, file=fw)


def main():
    templates = load_templates()

    with open("generated/platforms.nml", "w+") as fw:
        for platform_file in PLATFORMS:
            with open(platform_file, "r") as f:
                write_constants(templates, fw)
                data = yaml.safe_load(f)
                for key, val in data.items():
                    process_item(key, val, templates, fw)


if __name__ == "__main__":
    main()
