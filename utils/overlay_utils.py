import cv2
import numpy as np
from utils.blending_modes import blend_normal
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
