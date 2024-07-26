#!/usr/bin/env python3
from PIL import Image
import sys
from typing import *

class Print:
    colours = {
        "red": "\033[91m",
        "yellow": "\033[93m",
        "reset": "\033[0m"
    }

    @staticmethod
    def error(message):
        sys.stderr.write(f"{Print.colours["red"]}Error: {message}{Print.colours["reset"]}\n")

    @staticmethod
    def warn(message):
        sys.stderr.write(f"{Print.colours["yellow"]}Warning: {message}{Print.colours["reset"]}\n")

    @staticmethod
    def info(message):
        sys.stdout.write(f"{message}\n")


class ProcessImage:
    def __init__(self, image_path):
        self.image_path: str = image_path
        self._image = self._load_image()
        self._spritemap = self._load_spritemap()
        self._used_colours = self._get_used_colours()

    def _load_image(self):
        try:
            with Image.open(self.image_path) as img:
                if img.mode != "P":
                    Print.error(f"Image {self.image_path} is not in index mode")
                    sys.exit(1)
                return img.copy()
        except Exception as e:
            Print.error(f"Error when loading image, {type(e)}, {e}")
            sys.exit(1)

    def _load_spritemap(self):
        width, height = self._image.size
        pixels = list(self._image.getdata())
        return tuple(
            tuple(pixels[i * width:(i + 1) * width])
            for i in range(height)
        )

    def _get_used_colours(self):
        return set(pix for row in self._spritemap for pix in row)

    @property
    def image(self):
        return self._image

    @property
    def spritemap(self):
        return self._spritemap

    @property
    def used_colours(self):
        return self._used_colours

class CompareImage:
    def __init__(self, patient1, patient2):
        self.patient1 = patient1
        self.patient2 = patient2
        if not self.same_size:
            Print.error(f"Images {self.patient1.image_path} and {self.patient1.image_path} are not the same size")
            sys.exit(1)

    @property
    def same_size(self) -> bool:
        return self.patient1.image.size == self.patient2.image.size

    @staticmethod
    def get_recinfo(compare1, compare2) -> tuple:
        new_list = [[0 for _ in range(len(compare1.spritemap[0]))] for _ in range(len(compare1.spritemap))]
        # dict initialization
        recolour_dict1 = {_:_ for _ in range(256)}
        recolour_dict2 = {_:_ for _ in range(256)}
        processed_coords = set()

        common_colours = compare1.used_colours & compare2.used_colours

        for colour in compare1.used_colours:
            coords1 = [(x, y) for y, row in enumerate(compare1.spritemap) for x, pix in enumerate(row) if pix == colour]
            for coord in coords1:
                if coord in processed_coords: continue
                colour2 = compare2.spritemap[coord[1]][coord[0]]
                coords2 = [(x, y) for y, row in enumerate(compare2.spritemap) for x, pix in enumerate(row) if pix == colour2]
                final_coords:set = set(coords1) & set(coords2)
                processed_coords |= final_coords
                if colour == colour2:
                    for coord in final_coords:
                        new_list[coord[1]][coord[0]] = colour
                else:
                    new_colour = 0
                    while new_colour in common_colours:
                        new_colour += 1
                        if new_colour > 255:
                            Print.error("new colour exceeded 255, exiting")
                            sys.exit(1)
                    common_colours |= {new_colour}
                    for coord in final_coords:
                        new_list[coord[1]][coord[0]] = new_colour
                    recolour_dict1[new_colour] = colour
                    recolour_dict2[new_colour] = colour2

        Print.info(f"Current number of colours: {len(common_colours)}")
        return (tuple(new_list), recolour_dict1, recolour_dict2)

def gen_recolour_sprite(rec1, rec2):
    rec_copy = rec1.copy()
    rec_copy_1 = rec1.copy()
    for dkey, dval in rec2.items():
        rec_copy[dkey] = rec_copy_1[dval]

    return rec_copy

def process_image(image_paths: list[str]) -> tuple:
    class ProcessedImage:
        def __init__(self, spritemap):
            self.spritemap = spritemap

        @property
        def used_colours(self) -> set:
            if self.spritemap is None:
                return set()
            return set(pix for row in self.spritemap for pix in row)


    images = [ProcessImage(image_path) for image_path in image_paths]
    spritemap, rec1, rec2 = CompareImage.get_recinfo(images[0], images[1])

    recolour_sprites = {image_paths[0]:rec1.copy(), image_paths[1]:rec2.copy()}
    processed        = ProcessedImage(spritemap)

    for i in range(2, len(images)):
        spritemap, base_rec, new_rec = CompareImage.get_recinfo(processed, images[i])
        processed.spritemap = spritemap

        for key, recolour_sprite in recolour_sprites.items():
            recolour_sprites[key] = gen_recolour_sprite(recolour_sprite, base_rec)

        recolour_sprites[image_paths[i]] = new_rec

    return (processed.spritemap, images[0].image.getpalette(), recolour_sprites)


def write_image(filename: str, data: tuple, palette: Image.Palette) -> None:
    new_image = Image.new("P", (len(data[0]), len(data)))
    new_image.putdata([item for sublist in data for item in sublist])
    new_image.putpalette(palette)
    new_image.save(filename)

def format_recolour_data(recolour_data: dict[dict]) -> dict:
    f = {}
    for ind, rec in recolour_data.items():
        s = ""
        s+=("recolour_sprite {")
        s+=(f"\n    // {ind}")
        counter = 0
        for key, value in rec.items():
            if key == value: continue
            if counter % 12 == 0: s+=("\n    ")
            s+=(f"0x{key:02x}:0x{value:02x};")
            counter += 1
        s+=("\n}\n")
        Print.info(f"Used colours: {counter}")
        f[ind] = s
    return f

def write_recolour(filename: str, recolour_data: dict[dict]) -> None:
    with open(filename, "w+") as f:
        for rec in format_recolour_data(recolour_data).values():
            f.write(rec)
    Print.info(f"Recolour data written to {filename}")

def copyright():
    from datetime import datetime

    Print.info("blend.py - A tool to blend multiple images together")
    Print.info(f"Copyright 2024-{datetime.now().year} WenSim <wensimehrp@gmail.com>")
    Print.info("Licensed under the MIT License")
    Print.info("")


def main():
    import time
    start = time.time()

    copyright()

    if len(sys.argv) < 2:
        Print.error("Please provide at least one image to process\nUsage: blend.py <image1> <image2> ...")
        sys.exit(1)

    if sys.argv[1] in ("-h", "--help", "-?"):
        Print.info("Usage: blend.py <image1> <image2> ...")
        sys.exit(0)


    if len(sys.argv) > 3:
        Print.warn("You are processing more than 3 images, this may use a lot of colours")


    files = sys.argv[1:]

    spritemap, palette, recs = process_image(files)
    write_image("output.png", spritemap, palette)
    write_recolour("recolour.txt", recs)


    Print.info("Finished processing images")
    Print.info(f"Time taken: {time.time() - start:.2f}s")

if __name__ == "__main__":
    main()
