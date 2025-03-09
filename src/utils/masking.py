import cv2
import numpy as np

def apply_mask(image, mask):
    """
    Applies a grayscale gradient mask as an alpha channel to an image.

    Parameters:
    - image (np.ndarray): Input image (BGR or RGBA).
    - mask (np.ndarray): Grayscale gradient mask (single-channel, 0-255).

    Returns:
    - np.ndarray: Masked image with smooth transparency.
    """
    print("> Applying mask to the image...")

    # Ensure the mask is grayscale
    if len(mask.shape) == 3:
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    # Ensure the image has 4 channels (RGBA)
    if image.shape[-1] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    # Blend existing alpha with the mask instead of replacing
    existing_alpha = image[:, :, 3]  # Extract existing alpha channel
    new_alpha = cv2.multiply(existing_alpha.astype(np.float32) / 255.0, mask.astype(np.float32) / 255.0)
    new_alpha = (new_alpha * 255).astype(np.uint8)  # Convert back to 0-255

    # Apply the blended alpha channel back to the image
    image[:, :, 3] = new_alpha

    print(">> Clipping mask applied successfully.")
    return image