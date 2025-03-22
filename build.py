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


def load_temporary_registers():
    with open("src/temps.yml", "r") as f:
        return yaml.safe_load(f)


def layout(key, val_layout, templates, fw):
    temp_vars = set()
    output_lines = []

    for direction in ("x", "y"):
        output_lines.append(f"spritelayout sp_{key}_{direction}(){{")
        for part in val_layout:
            category, element = part.split(".")
            template_code = templates[category][element][direction]
            for matches in re.findall(check_temps, template_code):
                if "t_style" in matches:
                    continue
                temp_vars.update(var for var in matches if var.strip())
            output_lines.append(template_code)
        output_lines.append("}")

    max_offset = max(
        (
            templates["temps"].get(var, 0)
            for var in temp_vars
            if var in templates["temps"]
        ),
        default=0,
    )

    var_indices = {var: i + max_offset for i, var in enumerate(sorted(temp_vars))}

    replaced_lines = []
    for line in output_lines:
        for var, index in var_indices.items():
            if var in line:
                line = re.sub(r"\b" + re.escape(var) + r"\b", str(index), line)
        replaced_lines.append(line)

    print("\n".join(replaced_lines), file=fw)
    return var_indices


def process_item(key, val, templates, fw):
    temps = layout(key, val["layout"], templates, fw)
    registers = []
    if "style" in val:
        registers.append(f"STORE_TEMP({val['style']}, t_style),")
    for k, v in temps.items():
        registers.append(f"STORE_TEMP({k.replace('t_', 'sw_')}(), {v}),")

    sprite_layouts = f"[sp_{key}_x, sp_{key}_y]"
    misc = []
    general_flags = []
    if "preview" in val:
        sprite_layouts = f"[sp_{key}_x, sp_{key}_y, sp_preview_x, sp_preview_y]"
        misc.append("select_sprite_layout: 0;")
        misc.append("purchase_select_sprite_layout: 2;")
        registers.append(f"STORE_TEMP({val['preview']}, t_preview),")
    if "foundation" in val:
        general_flags.append("STAT_FLAG_CUSTOM_FOUNDATIONS")
        general_flags.append("STAT_FLAG_EXTENDED_FOUNDATIONS")
        misc.append(f"foundations: {val['foundation']};")

    printstr = item_templates[val.get("template", "default")].substitute(
        name=key,
        name_label=val.get("name_label", "DEFAULT"),
        general_flags=f"bitmask({', '.join(general_flags)})",
        temps="\n    ".join(registers),
        sprite_layouts=sprite_layouts,
        class_label=val.get("class_label", "WINS"),
        class_name=val.get("class_name", "STR_CLASS_WINS"),
        misc="\n    ".join(misc),
    )
    print(printstr, file=fw)


def main():
    templates = load_templates()
    templates = {**templates, **load_temporary_registers()}

    with open("generated/platforms.nml", "w+") as fw:
        for platform_file in PLATFORMS:
            with open(platform_file, "r") as f:
                data = yaml.safe_load(f)
                for key, val in data.items():
                    process_item(key, val, templates, fw)


if __name__ == "__main__":
    main()
