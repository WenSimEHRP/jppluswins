from blend import *
from string import Template
import os

sub_file = "src/spritesets.pynml"
with open(sub_file, "r") as f:
    sub_string = f.read()

files_to_blend = [
    "gfx/platform/wood.png",
    # "gfx/platform/tiles.png",
    "gfx/platform/cement.png",
]

init_dict = {_:_ for _ in range(256)}

recolour_substitutes = {
    "cement": {
        "target": "cement",
        "mode": "amend",
        "era1": {**init_dict.copy(), **{
            0x40: 0x07,
            0x41: 0x08,
            0x42: 0x08,
        }},
        "era2": {**init_dict.copy(), **{
            0x40: 0x0B,
            0x41: 0x0C,
            0x42: 0x0D,
        }},
        "era3": init_dict.copy()
    },
    "wood": {
        "target": "wood",
        "mode": "amend",
        "era1": init_dict.copy(),
        "era2": init_dict.copy(),
        "era3": init_dict.copy()
    },
    "asphalt": {
        "target": "cement",
        "mode": "new",
        "era1": {**init_dict.copy(), **{
            0x40: 16,
            0x41: 17,
            0x42: 17,
            7:  16,
            8:  17,
            9:  18,
            10: 19,
        }},
        "era2": {**init_dict.copy(), **{
            0x40: 21,
            0x41: 22,
            0x42: 23,
            7:  16,
            8:  17,
            9:  18,
            10: 19,
        }},
        "era3": {**init_dict.copy(), **{
            0x40: 0x40,
            0x41: 0x41,
            0x42: 0x42,
            7:  16,
            8:  17,
            9:  18,
            10: 19,
        }}
    },
    "tiles": {
        "target": "cement",
        "mode": "new",
        "era1": init_dict.copy(),
        "era2": init_dict.copy(),
        "era3": init_dict.copy()
    }
}

final_image, palette, recolour_sprites = process_image(files_to_blend)
write_image("gfx/platform/real.png", final_image, palette)

new_recoulour_sprites = recolour_substitutes.copy()
"""
dict = {
    "this": {
        "era1": {},
        "era2": {},
        "era3": {}
    }
}



"""

for key, val in recolour_substitutes.items():
    deep_dict = val # dict's pizza
    target_sprite = None
    for dkey, dsprite in recolour_sprites.items():
        if deep_dict["target"] in dkey:
            target_sprite = dsprite
            break

    for i in ("era1", "era2", "era3"):
        new_recoulour_sprites[key][i] = gen_recolour_sprite(deep_dict[i], target_sprite)

recolour_strings = {}
for key in recolour_substitutes.keys():
    recolour_strings[key] = ""

for key, val in new_recoulour_sprites.items():
        local_string = format_recolour_data({"era1":val["era1"], "era2":val["era2"], "era3":val["era3"]})
        recolour_strings[key] += "".join([value for value in local_string.values()])

template_string = sub_string

my_template = Template(template_string)
out_file = my_template.substitute({f"recolour_{key}": val for key, val in {**recolour_strings}.items()})

with open("src/spritesets.pnml", "w+") as f:
    f.write(out_file)
