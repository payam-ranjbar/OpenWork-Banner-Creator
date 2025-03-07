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


def get_dominant_color(image):
    """
    Detects the dominant color in an image.

    Parameters:
    - image (np.ndarray): Input image in BGR format.

    Returns:
    - tuple[int, int, int]: The dominant RGB color.
"""
    print("🎨 Detecting dominant color...")

    # Convert to RGB (since OpenCV loads in BGR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Resize image to speed up processing
    small_image = cv2.resize(image, (50, 50))  # Reduce size for faster processing

    # Reshape the image to be a list of pixels
    pixels = small_image.reshape(-1, 3)

    # Use k-means clustering to find the dominant color
    num_clusters = 3  # Using 3 clusters to avoid noise
    pixels = np.float32(pixels)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(pixels, num_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Find the most common cluster (dominant color)
    dominant_color = centers[np.argmax(np.bincount(labels.flatten()))]

    # Ensure values are properly scaled and converted to standard int
    dominant_color = tuple(map(int, np.clip(dominant_color, 0, 255)))

    print(f"🎨 Dominant color detected: {dominant_color}")
    return dominant_color