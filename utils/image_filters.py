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


def process_background_image(image, opacity=0.5):
    """
    Loads a background image, removes white pixels (makes them transparent), and applies opacity.

    Parameters:
    - image_path (str): Path to the background image file.
    - opacity (float): Opacity level (0 = fully transparent, 1 = fully opaque).

    Returns:
    - np.ndarray: Processed background image with transparency.
    """
    print(f"🖼️ Processing background image from {image} with opacity {opacity}...")

    # Convert to RGBA if it's not already
    if image.shape[2] == 3:  # If the image has no alpha channel, add one
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    # Define the white color range to be removed
    lower_white = np.array([200, 200, 200, 255], dtype=np.uint8)  # Bright white
    upper_white = np.array([255, 255, 255, 255], dtype=np.uint8)

    # Create a mask for white pixels
    white_mask = cv2.inRange(image, lower_white, upper_white)

    # Set white pixels to fully transparent
    image[white_mask == 255] = [0, 0, 0, 0]  # RGBA: (0, 0, 0, 0)

    # Apply opacity by modifying the alpha channel
    image[:, :, 3] = (image[:, :, 3] * opacity).astype(np.uint8)

    print("✅ Background processing complete (White pixels removed, opacity applied).")
    return image

import cv2
import numpy as np

def apply_gaussian_blur(image, blur_amount=5):
    """
    Applies a Gaussian blur to an image.

    Parameters:
    - image (np.ndarray): Input image.
    - blur_amount (int): Blur intensity (must be an odd number, e.g., 3, 5, 7).

    Returns:
    - np.ndarray: Blurred image.
    """
    print(f"🌫️ Applying Gaussian Blur with intensity {blur_amount}...")

    # Ensure blur_amount is an odd number (required by cv2.GaussianBlur)
    if blur_amount % 2 == 0:
        blur_amount += 1  # Make it the next odd number

    # Apply Gaussian blur
    blurred_image = cv2.GaussianBlur(image, (blur_amount, blur_amount), 0)

    return blurred_image
