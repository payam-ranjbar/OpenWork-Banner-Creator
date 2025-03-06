import cv2
import numpy as np

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

def create_fade_to_transparent(color, width=1920, height=1080, fade_strength=0.7):
    """Creates a vertical gradient from a solid color at the bottom to fully transparent at the top."""
    print("🎨 Creating transparent fade overlay...")
    fade_height = int(height * fade_strength)
    gradient = np.zeros((height, width, 4), dtype=np.uint8)

    for y in range(height):
        alpha = int((1 - (y / fade_height)) * 255) if y < fade_height else 0
        gradient[y, :, :3] = np.array(color)
        gradient[y, :, 3] = alpha

    return gradient

def overlay_transparent(bg, fg):
    """Overlays a transparent gradient on top of another image."""
    print("🔗 Applying transparency effect...")
    alpha_fg = fg[:, :, 3] / 255.0
    for c in range(3):
        bg[:, :, c] = fg[:, :, c] * alpha_fg + bg[:, :, c] * (1 - alpha_fg)
    return bg
