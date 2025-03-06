import cv2
import os
from utils.color_utils import extract_colors, create_gradient_rectangle
from utils.text_utils import add_text
from utils.bg_remover import remove_background_fast
from utils.overlay_utils import overlay_image, create_fade_to_transparent, overlay_transparent
from utils.file_utils import save_poster

def generate_poster(image_path):
    """Main function that generates the poster."""
    print("\n🚀 Starting Poster Generation Pipeline...")

    left_bg, right_bg, text_color = extract_colors(image_path)

    background = create_gradient_rectangle(left_bg, right_bg)
    background = add_text(background, "#Open to Work", text_color)

    cutout = remove_background_fast(image_path)

    background = cv2.cvtColor(background, cv2.COLOR_RGB2RGBA)

    poster = overlay_image(background.copy(), cutout)

    fade_gradient = create_fade_to_transparent(left_bg)
    poster = overlay_transparent(poster, fade_gradient)

    # 🔹 Save the final poster using `save_poster()`
    output_path = save_poster(poster, image_path)

    return output_path

# Example Usage
if __name__ == "__main__":
    image_path = "sample-image/ali.jpg"
    generate_poster(image_path)
