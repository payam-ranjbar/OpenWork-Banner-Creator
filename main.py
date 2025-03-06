import cv2
import os
from utils.color_utils import extract_colors, create_gradient_rectangle
from utils.text_utils import add_text
from utils.bg_remover import remove_background_fast
from utils.image_filters import apply_tint_filter, decrease_contrast, process_background_image
from utils.overlay_utils import overlay_image, create_fade_to_transparent, add_images
from utils.file_utils import save_poster
from utils.blending_modes import blend_overlay
def generate_poster(image_path,bg_pattern_source):
    """Main function that generates the poster."""
    print("\n🚀 Starting Poster Generation Pipeline...")

    left_bg, right_bg, text_color = extract_colors(image_path)

    background = create_gradient_rectangle(left_bg, right_bg)

    cutout = remove_background_fast(image_path)

    low_contrast = decrease_contrast(cutout, 0.1)
    tinted = apply_tint_filter(low_contrast, right_bg, strength=0.2)

    background = cv2.cvtColor(background, cv2.COLOR_RGB2RGBA)

    bg_pattern = process_background_image(bg_pattern_source, opacity=0.2)

    background = add_images(background, bg_pattern)
    background = add_text(background, "#Open to Work", text_color)

    poster = overlay_image(background.copy(), tinted)

    fade_gradient = create_fade_to_transparent(left_bg, fade_strength=1)
    poster = add_images(poster, fade_gradient)

    # 🔹 Save the final poster using `save_poster()`
    output_path = save_poster(poster, image_path)

    return output_path

# Example Usage
if __name__ == "__main__":
    image_path = "sample-image/soroosh-head.jpg"
    bg_pattern_source = "background-patterns/soroosh-pattern-bg.png"

    generate_poster(image_path, bg_pattern_source)
