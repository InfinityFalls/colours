
import colour
import numpy as np
import sys

TARGET_Y = 0.34937594007454498


def string_to_rgb(hex_str: str):
    r = int(hex_str[1:3], 16) / 255
    g = int(hex_str[3:5], 16) / 255
    b = int(hex_str[5:7], 16) / 255
    return np.array((r, g, b))


def rgb_to_string(rgb):
    r = hex(round(rgb[0] * 255))[2:].rjust(2, "0")
    g = hex(round(rgb[1] * 255))[2:].rjust(2, "0")
    b = hex(round(rgb[2] * 255))[2:].rjust(2, "0")
    return "#"+r+g+b


def adjust_y(oklch, steps):
    for _ in range(steps):
        xyz = colour.convert(oklch, "oklch", "cie xyz")
        xyz[1] = TARGET_Y
        oklch[0] = colour.convert(xyz, "cie xyz", "oklch")[0]
        print(xyz[1])


def get_y_from_rgb(rgb):
    xyz = colour.convert(rgb, "srgb", "cie xyz")
    return xyz[1]


def check_oklch(oklch):
    rgb = colour.convert(oklch, "oklch", "srgb")
    return np.all((0 <= rgb) & (rgb <= 1))


def adjust_c(oklch, steps):
    l = 0
    r = 0.32
    for _ in range(steps):
        m = (l + r) / 2
        oklch[1] = m
        if check_oklch(oklch):
            l = m
        else:
            r = m
        print(r - l)
    oklch[1] = l


def main():
    to_boost = sys.argv[1]
    input_rgb = string_to_rgb(to_boost)
    oklch = colour.convert(input_rgb, "srgb", "oklch")
    for i in range(3):
        adjust_y(oklch, 100)
        adjust_c(oklch, 100)
    boosted_rgb = colour.convert(oklch, "oklch", "srgb")
    print(rgb_to_string(boosted_rgb))
    print(get_y_from_rgb(boosted_rgb) - TARGET_Y)


if __name__ == "__main__":
    main()
