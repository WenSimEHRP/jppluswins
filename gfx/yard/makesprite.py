#!/usr/bin/env python3
from PIL import Image
import glob
import os

source = glob.glob("gfx/yard_source/*.png")
target_dir = "gfx/yard_target/"

# clear target directory and create it if it doesn't exist
if not os.path.exists(target_dir):
    os.makedirs(target_dir)
else:
    for f in glob.glob(target_dir + "*.png"):
        os.remove(f)

for s in source:
    with Image.open(s, "r") as img:
        img = img.convert("RGBA")
        # create a new image sized 512 * 256
        new_img = Image.new("RGBA", (512, 256), (255, 255, 255, 255))
        # crop and get parts of the original image
        straight = img.copy().crop((0, 360, 63, 390))
        bent = img.copy().crop((32, 160, 54, 176))
        junc = img.copy().crop((70, 96, 92, 110))
        bent2 = img.copy().crop((0, 59, 34, 67))
        junc2 = img.copy().crop((384, 0, 413, 11))
        # paste the parts to the new image
        new_a = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
        new_b = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
        new_c = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
        new_a.paste(straight, (0, 0), straight)
        new_b.paste(straight, (0, 0), straight)
        new_b.paste(bent, (0, 16), bent)
        new_b.paste(junc, (0, 32), junc)
        new_c.paste(bent2,    (32, 3), bent2)
        new_c.paste(straight, (0, 0), straight)
        new_c.paste(junc2,    (66, 0), junc2)
        new_img.paste(new_a, (128 * 0, 0))
        new_img.paste(new_b, (128 * 1 + 10, 0))
        new_img.paste(new_c, (128 * 2 + 20, 0))
        # mirror the images and paste again
        new_a = new_a.transpose(Image.FLIP_LEFT_RIGHT)
        new_b = new_b.transpose(Image.FLIP_LEFT_RIGHT)
        new_c = new_c.transpose(Image.FLIP_LEFT_RIGHT)
        new_img.paste(new_a, (128 * 0, 74))
        new_img.paste(new_b, (128 * 1 + 10, 74))
        new_img.paste(new_c, (128 * 2 + 20, 74))
        # save the new image
        new_img.save(target_dir + os.path.basename(s))
