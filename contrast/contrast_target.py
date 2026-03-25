import colour

from utils import adjust_c, adjust_y, rgb_to_string, string_to_rgb, get_y_from_rgb

FOREGROUND = "#FFD966"
BACKGROUND = "#38751E"
TARGET_CONTRAST = 75


def darker_limit(bg: float, c: float):
    p = (114 * (bg ** 0.56) - c + 2.7) / 114
    if (p < 0):
        return 0
    return p ** (1/0.57)


def lighter_limit(bg: float, c: float):
    p = (114 * (bg ** 0.65) + c - 2.7) / 114
    if (p < 0):
        return 0
    return p ** (1/0.62)


def adjust_contrast(to_boost: str, target_y: float) -> tuple[str, float]:
    input_rgb = string_to_rgb(to_boost)

    oklch = colour.convert(input_rgb, "srgb", "oklch")
    for i in range(3):
        adjust_y(oklch, 100, target_y)
        adjust_c(oklch, 100)
    boosted_rgb = colour.convert(oklch, "oklch", "srgb")
    return rgb_to_string(boosted_rgb), get_y_from_rgb(boosted_rgb)


def main():
    bg_rgb = string_to_rgb(BACKGROUND)
    bg_y = get_y_from_rgb(bg_rgb)
    low_target = darker_limit(bg_y, TARGET_CONTRAST)
    high_target = lighter_limit(bg_y, TARGET_CONTRAST)
    print(FOREGROUND, get_y_from_rgb(string_to_rgb(FOREGROUND)))
    print(BACKGROUND, bg_y)
    print(*adjust_contrast(FOREGROUND, low_target))
    print(*adjust_contrast(FOREGROUND, high_target))


if __name__ == "__main__":
    main()
