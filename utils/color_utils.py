import cv2
import numpy as np


def extract_colors(image_path):
    """Extracts two background colors and one contrasting text color from an image."""
    print("🔍 Extracting colors from image...")

    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    height, width, _ = image.shape

    left_color = np.median(image[:, :10], axis=(0, 1)).astype(int)
    right_color = np.median(image[:, -10:], axis=(0, 1)).astype(int)

    middle_pixels = image.reshape(-1, 3)[::100]
    text_color = max(middle_pixels, key=lambda c: abs(np.mean(left_color) - np.mean(c)))

    return tuple(map(int, left_color)), tuple(map(int, right_color)), tuple(map(int, text_color))


def create_gradient_rectangle(color1, color2, width=1920, height=1080):
    """Creates a horizontal linear gradient between two colors."""
    gradient = np.zeros((height, width, 3), dtype=np.uint8)
    for x in range(width):
        alpha = x / (width - 1)
        gradient[:, x] = (1 - alpha) * np.array(color1) + alpha * np.array(color2)
    return gradient
