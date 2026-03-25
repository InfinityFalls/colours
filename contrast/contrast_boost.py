
import colour
import sys

from contrast.utils import adjust_c, adjust_y, get_y_from_rgb, rgb_to_string, string_to_rgb

TARGET_Y = 0.34937594007454498


def main():
    to_boost = sys.argv[1]
    input_rgb = string_to_rgb(to_boost)
    oklch = colour.convert(input_rgb, "srgb", "oklch")
    for i in range(3):
        adjust_y(oklch, 100, TARGET_Y)
        adjust_c(oklch, 100)
    boosted_rgb = colour.convert(oklch, "oklch", "srgb")
    print(rgb_to_string(boosted_rgb))
    print(get_y_from_rgb(boosted_rgb) - TARGET_Y)


if __name__ == "__main__":
    main()
