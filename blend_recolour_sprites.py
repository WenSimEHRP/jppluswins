from blend import gen_recolour_sprite, Print, write_recolour, copyright
import sys
import re

if __name__ == "__main__":
    copyright()

    recolour_sprites = [{_:_ for _ in range(256)} for _ in range(2)]

    if len(sys.argv) != 3:
        Print.error("Usage: blend_recolour_sprites.py <sprite1> <sprite2>\nUse the cat command if you want to read files")
        sys.exit(1)
    data = sys.argv[1:]

    for i, my_data in enumerate(data):
        # if pair starts with 0x it's a hex
        new_recolour_sprites = {
            (int(pair[0], 16) if pair[0].startswith("0x") else int(pair[0])):
            (int(pair[1], 16) if pair[1].startswith("0x") else int(pair[1]))
            for pair in re.findall(r"(0x[0-9a-fA-F]{2}|\d{1,3}):\s*(0x[0-9a-fA-F]{2}|\d{1,3})", my_data)}
        # use the new data to update the recolour sprites
        recolour_sprites[i].update(new_recolour_sprites)

    try:
        write_recolour("new_recolour.txt",{"new_recolour.txt":gen_recolour_sprite(recolour_sprites[0], recolour_sprites[1])})
    except KeyError:
        Print.error("Recolour sprites don't match")
        sys.exit(1)
    except Exception as e:
        Print.error(f"An error occurred: {e}")
        sys.exit(1)
