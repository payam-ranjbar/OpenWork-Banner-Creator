import cv2
import numpy as np

def decrease_contrast(image, amount=0.2):
    """
    Decreases the contrast of an image by a given amount.

    Parameters:
    - image (np.ndarray): Input image (RGB or RGBA).
    - amount (float): Contrast reduction strength (0 = no change, 1 = fully gray).

    Returns:
    - np.ndarray: Image with reduced contrast.
    """
    print(f"🎨 Reducing contrast with strength {amount}...")

    # Ensure amount is within valid range
    amount = max(0, min(amount, 1))

    # Convert image to float32 for contrast manipulation
    image = image.astype(np.float32)

    # Compute mean pixel intensity
    mean = np.mean(image[:, :, :3], axis=(0, 1))  # Compute mean of R, G, B

    # Blend image towards its mean intensity (reducing contrast)
    for c in range(3):  # Apply to R, G, B channels only
        image[:, :, c] = (1 - amount) * image[:, :, c] + amount * mean[c]

    # Ensure values stay in range (0-255)
    image = np.clip(image, 0, 255).astype(np.uint8)

    print("✅ Contrast reduced successfully.")
    return image

def apply_tint_filter(image, tint_color, strength=0.5):
    """
    Applies a color tint (filter) to an image.

    Parameters:
    - image (np.ndarray): Input image (RGBA or RGB format).
    - tint_color (tuple[int, int, int]): RGB color of the tint.
    - strength (float): Tint strength (0 = no effect, 1 = full tint).

    Returns:
    - np.ndarray: Image with the applied tint.
    """
    print(f"🎨 Applying tint filter with color {tint_color} and strength {strength}...")

    # Ensure strength is within valid range
    strength = max(0, min(strength, 1))

    # Convert image to float32 for blending calculations
    tinted_image = image.astype(np.float32)

    # Apply tint by blending the original image with the tint color
    for c in range(3):  # Apply to R, G, B channels (skip alpha if present)
        tinted_image[:, :, c] = (1 - strength) * tinted_image[:, :, c] + strength * tint_color[c]

    # Ensure values are within valid range (0-255)
    tinted_image = np.clip(tinted_image, 0, 255).astype(np.uint8)

    print("✅ Tint filter applied successfully.")
    return tinted_image