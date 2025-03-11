#!/usr/bin/env python3
import yaml
import re
from item_template import item_templates

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
                registers = ""
                for t in temps:
                    registers += f"STORE_TEMP({tem["temps"][t]}, {t}),\n"
                printstr = item_templates[val.get("template", "default")].substitute(
                    name=key, temps=registers, class_label=val.get("class_label", "WINS")
                )
                print(printstr, file=fw)
