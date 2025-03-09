import colorsys

import cv2
import numpy as np


def bgr_to_hsv(bgr_color):
    """Convert BGR color to HSV."""
    return cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)[0][0]


def hsv_to_bgr(hsv_color):
    """Convert HSV color to BGR."""
    return cv2.cvtColor(np.uint8([[hsv_color]]), cv2.COLOR_HSV2BGR)[0][0]


def get_analogous_colors(bgr_color, n=3, offset=30):
    """
    Generate analogous colors.
    :param bgr_color: Input BGR color.
    :param n: Number of colors to generate.
    :param offset: Hue offset in degrees.
    :return: List of BGR colors.
    """
    hsv_color = bgr_to_hsv(bgr_color)
    h, s, v = hsv_color
    return [hsv_to_bgr(((h + i * offset) % 180, s, v)) for i in range(n)]


def get_complementary_color(bgr_color, boost_s=1, boost_v=1.2):

    hsv_color = bgr_to_hsv(bgr_color)
    h, s, v = hsv_color

    comp_h = (h + 90) % 180

    comp_s = min(s * boost_s, 255)
    comp_v = min(v * boost_v, 255)

    return hsv_to_bgr((comp_h, comp_s, comp_v))


def get_triadic_colors(bgr_color):
    """
    Generate triadic colors.
    :param bgr_color: Input BGR color.
    :return: List of 3 BGR colors.
    """
    hsv_color = bgr_to_hsv(bgr_color)
    h, s, v = hsv_color
    return [hsv_to_bgr(((h + i * 60) % 180, s, v)) for i in range(3)]


def get_tetradic_colors(bgr_color):
    """
    Generate tetradic colors.
    :param bgr_color: Input BGR color.
    :return: List of 4 BGR colors.
    """
    hsv_color = bgr_to_hsv(bgr_color)
    h, s, v = hsv_color
    return [hsv_to_bgr(((h + i * 45) % 180, s, v)) for i in range(4)]


def get_split_complementary_colors(bgr_color):
    """
    Generate split-complementary colors.
    :param bgr_color: Input BGR color.
    :return: List of 3 BGR colors.
    """
    hsv_color = bgr_to_hsv(bgr_color)
    h, s, v = hsv_color
    return [hsv_to_bgr(((h + i * 150) % 180, s, v)) for i in range(3)]


def square_colors(bgr_color):
    """
    Generate square colors.
    :param bgr_color: Input BGR color.
    :return: List of 4 BGR colors.
    """
    hsv_color = bgr_to_hsv(bgr_color)
    h, s, v = hsv_color
    return [hsv_to_bgr(((h + i * 90) % 180, s, v)) for i in range(4)]


def increase_saturation(bgr_color, saturation_boost=1.5):
    """
    Increases the saturation of a BGR color.

    Parameters:
    - bgr_color (tuple[int, int, int]): Input BGR color.
    - saturation_boost (float): Multiplier to increase saturation (default: 1.5).

    Returns:
    - tuple[int, int, int]: BGR color with increased saturation.
    """
    # Convert BGR to HSV
    hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)[0][0]

    # Increase saturation
    h, s, v = hsv_color
    s = min(s * saturation_boost, 255)  # Ensure saturation doesn't exceed 255

    # Convert back to BGR
    new_bgr_color = cv2.cvtColor(np.uint8([[[h, s, v]]]), cv2.COLOR_HSV2BGR)[0][0]
    return tuple(new_bgr_color)


def increase_luminance(bgr_color, luminance_boost=1.2):
    """
    Increases the luminance (brightness) of a BGR color.

    Parameters:
    - bgr_color (tuple[int, int, int]): Input BGR color.
    - luminance_boost (float): Multiplier to increase luminance (default: 1.2).

    Returns:
    - tuple[int, int, int]: BGR color with increased luminance.
    """
    # Convert BGR to HSV
    hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)[0][0]

    # Increase luminance (Value)
    h, s, v = hsv_color
    v = min(v * luminance_boost, 255)  # Ensure value doesn't exceed 255

    # Convert back to BGR
    new_bgr_color = cv2.cvtColor(np.uint8([[[h, s, v]]]), cv2.COLOR_HSV2BGR)[0][0]
    return tuple(new_bgr_color)


def get_dominant_color(image):

    print("> Detecting dominant color...")

    if image.shape[-1] == 4:  # If RGBA, remove alpha channel
        image = image[:, :, :3]  # Keep only RGB/BGR channels
    # Resize image to speed up processing
    small_image = cv2.resize(image, (50, 50))  # Keep in BGR format

    # Reshape the image to be a list of pixels
    pixels = small_image.reshape(-1, 3)

    # Use k-means clustering to find the dominant color
    num_clusters = 3
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(
        np.float32(pixels),  # Input must be float32
        num_clusters,
        None,
        criteria,
        10,
        cv2.KMEANS_RANDOM_CENTERS
    )

    # Find the most common cluster (dominant color)
    dominant_color = centers[np.argmax(np.bincount(labels.flatten()))]

    # Convert to integer BGR tuple (0-255)
    dominant_color = tuple(np.uint8(dominant_color))

    print(f">> Dominant color detected: {dominant_color}")

    return dominant_color



def get_text_color(left_bg, right_bg):
    # Previous contrast calculation remains the same
    light = (255, 247, 216)
    dark = (27, 31, 40)

    # Calculate contrast ratios
    contrast_white_left = get_contrast_ratio(light, left_bg)
    contrast_white_right = get_contrast_ratio(light, right_bg)
    min_white = min(contrast_white_left, contrast_white_right)

    contrast_black_left = get_contrast_ratio(dark, left_bg)
    contrast_black_right = get_contrast_ratio(dark, right_bg)
    min_black = min(contrast_black_left, contrast_black_right)



    # Choose color with  minimum contrast
    return light if min_white > min_black else dark


def get_colors(image_path, dominant_color=None):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Downsample
    small_img = cv2.resize(image, (100, 100), interpolation=cv2.INTER_AREA)

    if dominant_color is None:
        dominant_color = get_dominant_color(small_img)
    sat_increase = 2.5
    comp_color = get_complementary_color(dominant_color)
    _, left_bg, right_bg = get_analogous_colors(comp_color)
    text_color = get_text_color(left_bg, right_bg)

    left_bg = rgb_to_bgr(left_bg)
    right_bg = rgb_to_bgr(right_bg)
    text_color = rgb_to_bgr(text_color)
    left_bg, right_bg = increase_saturation(left_bg, sat_increase), increase_saturation(right_bg, sat_increase)

    return left_bg, right_bg, text_color


def get_relative_luminance(color):
    r, g, b = color
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0

    # Convert to linear RGB
    r = r if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4

    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def get_contrast_ratio(color1, color2):
    l1 = get_relative_luminance(color1)
    l2 = get_relative_luminance(color2)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)


def rgb_to_bgr(color):
    """Converts an RGB color to BGR."""
    return color[::-1]
