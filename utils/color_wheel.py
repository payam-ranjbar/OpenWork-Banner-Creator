import colorsys

def get_complementary_color(color):
    """
    Computes the complementary color of a given RGB color.

    Parameters:
    - color (tuple[int, int, int]): The input RGB color.

    Returns:
    - tuple[int, int, int]: The complementary RGB color.
    """
    print(f"🌈 Calculating complementary color for {color}...")

    r, g, b = map(lambda x: x / 255.0, color)  # Normalize to 0-1

    # Convert RGB to HSV
    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    # Find complementary hue (shift 180 degrees on color wheel)
    h_complementary = (h + 0.5) % 1.0  # Rotate hue by 180 degrees

    # Convert back to RGB
    r_comp, g_comp, b_comp = colorsys.hsv_to_rgb(h_complementary, s, v)

    # Scale back to 0-255
    complementary_color = tuple(map(lambda x: int(x * 255), (r_comp, g_comp, b_comp)))

    print(f"✅ Complementary color: {complementary_color}")
    return complementary_color

def get_analogous_colors(color, angle_offset=30):
    """
    Computes two neighboring analogous colors based on the given RGB color.

    Parameters:
    - color (tuple[int, int, int]): The input RGB color.
    - angle_offset (int): The offset in degrees for analogous colors (default is 30 degrees).

    Returns:
    - tuple[tuple[int, int, int], tuple[int, int, int]]: Two analogous RGB colors.
    """
    print(f"🎨 Calculating analogous colors for {color}...")

    r, g, b = map(lambda x: x / 255.0, color)  # Normalize to 0-1

    # Convert RGB to HSV
    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    # Convert degrees to the range of 0-1 (hue in HSV is between 0 and 1)
    angle_offset = angle_offset / 360.0

    # Compute analogous hues (shifting left and right on the color wheel)
    h1 = (h + angle_offset) % 1.0  # Shift hue forward
    h2 = (h - angle_offset) % 1.0  # Shift hue backward

    # Convert back to RGB
    r1, g1, b1 = colorsys.hsv_to_rgb(h1, s, v)
    r2, g2, b2 = colorsys.hsv_to_rgb(h2, s, v)

    # Scale RGB values back to 0-255 range
    analogous_color_1 = tuple(map(lambda x: int(x * 255), (r1, g1, b1)))
    analogous_color_2 = tuple(map(lambda x: int(x * 255), (r2, g2, b2)))

    print(f"✅ Analogous colors: {analogous_color_1}, {analogous_color_2}")
    return analogous_color_1, analogous_color_2

import colorsys

def get_best_text_color(background_color):
    """
    Determines an appealing and readable text color for a given background color.

    Parameters:
    - background_color (tuple[int, int, int]): The background color in RGB (0-255).

    Returns:
    - tuple[int, int, int]: The suggested text color in RGB (0-255).
    """
    print(f"🎨 Finding the best text color for background {background_color}...")

    # Convert background color to HSV
    r, g, b = background_color
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

    # Generate complementary color (opposite on the color wheel)
    h_complementary = (h + 0.5) % 1.0
    r_comp, g_comp, b_comp = colorsys.hsv_to_rgb(h_complementary, s, v)
    complementary_color = (int(r_comp * 255), int(g_comp * 255), int(b_comp * 255))

    # Determine brightness of the background color (YIQ formula)
    brightness = (r * 299 + g * 587 + b * 114) / 1000

    # If the background is dark, use a bright color (white/gold), otherwise use black
    if brightness < 128:
        # Use a bright color (Gold, White, or Complementary)
        best_text_color = (255, 215, 0) if complementary_color == background_color else complementary_color
    else:
        # Use a dark color (Black)
        best_text_color = (0, 0, 0)

    print(f"✅ Best text color: {best_text_color}")
    return best_text_color
