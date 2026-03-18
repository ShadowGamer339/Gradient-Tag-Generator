# Released under the MIT License. See LICENSE for details. 

# MULTI-COLOR WAVE GENERATOR (HEX → WAVE + PREVIEW + CUSTOM KEY)

import re
import time
import os
import colorsys
import math

# --------------------------
#    WELCOME BANNER
# --------------------------
B  = "\033[94m"  # blue
W  = "\033[97m"  # white
BOLD = "\033[1m"
RST = "\033[0m"

banner = f"""
{B}╔════════════════════════════════════════╗
║         {W}{BOLD}MADE BY SHADOWGAMER{RST}{B}            ║
║        {W}{BOLD}DC id : 1shadowgamer1{RST}{B}           ║
╚════════════════════════════════════════╝{RST}
"""
print(banner)

# --------------------------
#    COLOR PRESETS
# --------------------------

COLOR_MAP = {
"red": "#ff0000",
"orange": "#ff7f00",
"yellow": "#ffff00",
"green": "#00ff00",
"blue": "#0000ff",
"purple": "#8000ff",
"pink": "#ff00aa",
"white": "#ffffff",
"cyan": "#00ffff"
}

# --------------------------
#    UTILS
# --------------------------
def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16)/255 for i in (0, 2, 4))

def parse_color(c):
    c = c.lower()
    if c in COLOR_MAP:
        return hex_to_rgb(COLOR_MAP[c])
    if re.fullmatch(r"#?[0-9a-fA-F]{6}", c):
        return hex_to_rgb(c)
    return None

def interpolate(c1, c2, t):
    t = t * t * (3 - 2 * t)
    return (
        round(c1[0] + (c2[0] - c1[0]) * t, 3),
        round(c1[1] + (c2[1] - c1[1]) * t, 3),
        round(c1[2] + (c2[2] - c1[2]) * t, 3),
    )

def interpolate_colors(color_list, steps):
    result = []
    segments = len(color_list) - 1
    for i in range(steps):
        t = i / (steps - 1)
        seg = int(t * segments)
        seg_t = (t * segments) - seg
        c1 = color_list[seg]
        c2 = color_list[min(seg + 1, segments)]
        result.append(interpolate(c1, c2, seg_t))
    return result

# --------------------------
#    INPUTS
# --------------------------
def get_steps():
    while True:
        try:
            steps = int(input("Enter steps(8–32)(recommended 16): "))
            if 8 <= steps <= 32:
                return steps
        except:
            pass
        print("Invalid. Try again.")

def get_mode():
    while True:
        print("\n1 = Smooth Gradient")
        print("2 = Shiny Wave Gradient")
        choice = input("Choose mode: ")
        if choice in ("1", "2"):
            return choice
        print("Invalid choice.")

def get_single_color():
    while True:
        c = input("Enter base color: ")
        parsed = parse_color(c)
        if parsed:
            return parsed
        print("Invalid color.")

def get_multiple_colors():
    colors = []
    while True:
        c = input("Enter color (or 'done'): ")
        if c.lower() == "done":
            if len(colors) >= 2:
                return colors
            print("Enter at least 2 colors.")
            continue
        parsed = parse_color(c)
        if parsed:
            colors.append(parsed)
        else:
            print("Invalid color.")

def get_key():
    while True:
        key = input("Enter key (e.g. WAVE_1): ")
        if re.fullmatch(r"[A-Z_][A-Z0-9_]*", key):
            return key
        print("Invalid key.")

# --------------------------
#    SMOOTH GRADIENT (UNCHANGED)
# --------------------------
def smooth_gradient(colors, steps):
    return interpolate_colors(colors, steps)

# --------------------------
#    SHINY WAVE (SAFE & SMOOTH)
# --------------------------
def shiny_gradient(base_color, steps):
    """
    Dynamic shiny gradient:
    - Mirrored highlight and base layers
    - Smooth interpolation
    - Avoids muddy dark colors
    """
    r0, g0, b0 = base_color
    # Convert to HLS
    h, l, s = colorsys.rgb_to_hls(r0, g0, b0)

    # Compute key lightness stops
    highlight = min(l + (1.0 - l) * 0.9, 1.0)   # very close to white
    light = min(l + (1.0 - l) * 0.5, 1.0)       # lighter than base
    base = l                                     # original lightness
    deep = max(l - l * 0.3, 0.0)                # slightly darker

    # Create a mirrored list of stops
    stops = [highlight, light, base, deep, base, light, highlight]
    # Map to number of steps
    result = []
    n = len(stops) - 1
    for i in range(steps):
        t = i / (steps - 1) * n
        idx = int(t)
        frac = t - idx
        start_l = stops[idx]
        end_l = stops[min(idx + 1, n)]
        new_l = start_l + (end_l - start_l) * frac
        r, g, b = colorsys.hls_to_rgb(h, new_l, s)
        result.append((round(r,3), round(g,3), round(b,3)))

    return result

# --------------------------
#    PREVIEW
# --------------------------
def preview(colors):
    print("\nPreview:")
    for c in colors:
        r = int(c[0]*255)
        g = int(c[1]*255)
        b = int(c[2]*255)
        print(f"\033[38;2;{r};{g};{b}m██\033[0m", end="")
    print("\n")

    print("Animation Preview (Ctrl+C to stop):")
    try:
        while True:
            for shift in range(len(colors)):
                os.system('clear')
                for i in range(len(colors)):
                    c = colors[(i + shift) % len(colors)]
                    r = int(c[0]*255)
                    g = int(c[1]*255)
                    b = int(c[2]*255)
                    print(f"\033[38;2;{r};{g};{b}m██\033[0m", end="")
                print()
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopped preview.\n")

# --------------------------
#    MAIN
# --------------------------
def main():
    steps = get_steps()
    mode = get_mode()

    if mode == "1":
        base_colors = get_multiple_colors()
        colors = smooth_gradient(base_colors, steps)
    else:
        base_color = get_single_color()
        colors = shiny_gradient(base_color, steps)

    key = get_key()

    # 🔥 PRINT FIRST
    print("\nGenerated:\n")
    print(f"{key} = [")
    for c in colors:
        print(f"    {c},")
    print("]")

    # 🔥 THEN PREVIEW
    if input("\nPreview? (y/n): ").lower() == "y":
        preview(colors)


if __name__ == "__main__":
    main()