import cv2
import numpy as np
from rembg import remove

def remove_background_fast(image, target_size=(500, 500)):
    """Removes background using rembg while preserving original colors."""
    print("⚡ Removing background...")

    # Read the image
    if image is None:
        raise ValueError("Error: Image not found.")

    # Convert from BGR (cv2 default) to RGB (rembg expects RGB)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Resize for faster processing
    original_size = image.shape[:2]
    image = cv2.resize(image, target_size)

    # Convert to RGBA for transparency support
    if image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)

    # Remove background
    output = remove(image)

    # Resize back to original size
    output = cv2.resize(output, (original_size[1], original_size[0]))

    # Convert back to OpenCV format (BGR)
    output = cv2.cvtColor(output, cv2.COLOR_RGBA2BGRA)

    return output
