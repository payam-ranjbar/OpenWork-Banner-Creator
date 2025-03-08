import cv2
import numpy as np
from src.utils.blending_modes import blend_normal
def overlay_image(bg, fg):
    """Overlays the cutout image onto the background while maintaining aspect ratio."""
    print("🔗 Overlaying subject on background...")

    fg_height, fg_width = fg.shape[:2]
    aspect_ratio = fg_width / fg_height
    new_height = bg.shape[0]
    new_width = int(new_height * aspect_ratio)

    fg_resized = cv2.resize(fg, (new_width, new_height))

    x_offset = (bg.shape[1] - new_width) // 2
    y_offset = 0

    alpha_fg = fg_resized[:, :, 3] / 255.0
    for c in range(3):
        bg[y_offset:y_offset+new_height, x_offset:x_offset+new_width, c] = (
            fg_resized[:, :, c] * alpha_fg + bg[y_offset:y_offset+new_height, x_offset:x_offset+new_width, c] * (1 - alpha_fg)
        )

    return bg

def create_fade_to_transparent(color, width=1920, fade_strength=0.4, height=1080):
    """Creates a vertical gradient from a solid color at the bottom to fully transparent at the top."""
    print("🎨 Creating transparent fade overlay...")
    fade_height = int(height * fade_strength)
    gradient = np.zeros((height, width, 4), dtype=np.uint8)

    for y in range(height):
        alpha = int((y / fade_height) * 255) if y < fade_height else 255
        gradient[y, :, :3] = np.array(color)
        gradient[y, :, 3] = alpha

    return gradient

def add_images(bg, fg, blend_function=None):

    print(f"🔗 Applying custom blend mode...")

    fg = cv2.resize(fg, (bg.shape[1], bg.shape[0]))

    alpha_fg = fg[:, :, 3] / 255.0  # Alpha mask (0-1)

    if blend_function is None:
        blend_function = blend_normal

    blended_image = blend_function(bg, fg, alpha_fg)

    return blended_image

def generate_gradient_mask_from_image(image, fade_strength=1.0, fade_direction=1, gradient_direction="vertical", interploation = "quadratic"):
    """
    Generates a gradient mask based on an image's width and height.

    Parameters:
    - image (np.ndarray): Input image (to get width & height).
    - fade_strength (float): Strength of fade (0.0 to 1.0, higher = more fade).
    - direction (str): "vertical" (top to bottom) or "horizontal" (left to right).

    Returns:
    - np.ndarray: Gradient mask (grayscale, 0-255).
    """
    height, width = image.shape[:2]  # Get image dimensions
    print(f"📏 Generating {gradient_direction} gradient mask for {width}x{height} image with strength {fade_strength}...")

    # Ensure fade_strength is within valid range
    fade_strength = np.clip(fade_strength, 0.0, 1.0)

    # Determine the start and end values for the gradient
    start_value = 255 if fade_direction >= 0 else 0
    end_value = 0 if fade_direction >= 0 else 255

    # Generate the gradient using the interpolation function


    if gradient_direction == "vertical":
        gradient = interpolate_gradient(height, start_value, end_value, interpolation=interploation)
        mask = np.tile(gradient, (width, 1)).T  # Transpose to make it vertical
    else:
        gradient = interpolate_gradient(width, start_value, end_value, interpolation=interploation)
        mask = np.tile(gradient, (height, 1))  # No transpose needed for horizontal

        # Apply fade strength
    if fade_strength < 1.0:
        # Blend the gradient with a fully visible mask (white)
        fully_visible_mask = np.full_like(mask, 255)
        mask = cv2.addWeighted(mask, fade_strength, fully_visible_mask, 1 - fade_strength, 0)

    return mask

def interpolate_gradient(length, start_value, end_value, interpolation="quadratic"):
    """
    Generates a gradient using quadratic interpolation.

    Parameters:
    - length (int): Length of the gradient (number of steps).
    - start_value (int): Starting value of the gradient (0-255).
    - end_value (int): Ending value of the gradient (0-255).
    - interpolation (str): Type of interpolation ("linear", "quadratic").

    Returns:
    - np.ndarray: Gradient array (0-255).
    """
    # Generate a linear gradient from 0 to 1
    gradient = np.linspace(0, 1, length)

    # Apply interpolation
    if interpolation == "quadratic":
        gradient = gradient ** 8  # Quadratic interpolation
    elif interpolation == "linear":
        pass  # Keep the gradient linear
    else:
        raise ValueError("Unsupported interpolation type. Use 'linear' or 'quadratic'.")

    # Scale the gradient to the desired range (start_value to end_value)
    gradient = start_value + (end_value - start_value) * gradient

    # Convert to uint8
    return gradient.astype(np.uint8)