import colour
import numpy as np



def rgb_to_string(rgb):
    r = hex(round(rgb[0] * 255))[2:].rjust(2, "0")
    g = hex(round(rgb[1] * 255))[2:].rjust(2, "0")
    b = hex(round(rgb[2] * 255))[2:].rjust(2, "0")
    return "#"+r+g+b


def string_to_rgb(hex_str: str):
    r = int(hex_str[1:3], 16) / 255
    g = int(hex_str[3:5], 16) / 255
    b = int(hex_str[5:7], 16) / 255
    return np.array((r, g, b))


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
    oklch[1] = l


def adjust_y(oklch, steps, target_y):
    for _ in range(steps):
        xyz = colour.convert(oklch, "oklch", "cie xyz")
        xyz[1] = target_y
        oklch[0] = colour.convert(xyz, "cie xyz", "oklch")[0]
        
        
def contrast(fg: float, bg: float):
    c = 1.14
    if bg > fg:
        c *= bg ** 0.56 - fg ** 0.57
    else:
        c *= bg ** 0.65 - fg ** 0.62
    
    c = abs(c)
    if abs(c) < 0.1:
        return 0
    else:
        c += 0.027
    return c * 100