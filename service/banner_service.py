import cv2
import numpy as np

from utils.color_utils import create_gradient_rectangle
from utils.file_utils import get_unique_filename
from utils.bg_remover import remove_background_fast
from utils.image_filters import decrease_contrast, apply_tint_filter, process_background_image, apply_gaussian_blur
from utils.masking import apply_mask
from utils.overlay_utils import overlay_image, add_images, create_fade_to_transparent, generate_gradient_mask_from_image
from utils.text_utils import add_text_center, add_text_fit_width
from models.Profile import Profile
from models.ColorPaletteGenerator import ColorPaletteGenerator, ColorPalette


def banner_service(profile: Profile, color_palette: ColorPalette = None):
    """Generates a professional banner based on the given profile and optional color palette."""
    print("\n🚀 Starting Banner Generation...")

    image_path = profile.picture
    bg_pattern_source = profile.pattern_bg
    person_name = profile.name
    person_header = profile.header

    if color_palette is None:
        color_palette = ColorPaletteGenerator(image_path)

    left_bg = color_palette.accent_color_left
    right_bg = color_palette.accent_color_right
    text_color = color_palette.title_text_color

    profile_pic = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    cutout = remove_background_fast(profile_pic)
    background = create_gradient_rectangle(left_bg, right_bg)

    low_contrast = decrease_contrast(cutout, 0.1)
    tinted_cutout = apply_tint_filter(low_contrast, right_bg, strength=0.2)
    gradient_mask = generate_gradient_mask_from_image(profile_pic, fade_strength=1, interploation="quadratic")

    masked_cutout = apply_mask(tinted_cutout, gradient_mask)

    background = cv2.cvtColor(background, cv2.COLOR_RGB2RGBA)
    bg_pattern = process_background_image(bg_pattern_source, opacity=0.2)
    bg_pattern = apply_mask(bg_pattern, generate_gradient_mask_from_image(bg_pattern, interploation="linear"))
    bg_pattern = apply_gaussian_blur(bg_pattern, 9)
    background = add_images(background, bg_pattern)

    poster = overlay_image(background.copy(), masked_cutout)
    fade_gradient = create_fade_to_transparent(left_bg, fade_strength=1.5)
    poster = add_images(poster, fade_gradient)
    poster = add_text_center(poster, person_name.upper(), font_size=70, color=text_color, letter_spacing=10,
                             y_offset=350)
    poster = add_text_fit_width(poster, person_header, color=text_color, letter_spacing=0, y_offset=450,
                                max_font_size=50)

    output_path, output_name = save_poster(poster, image_path)
    print(f"✅ Banner saved at: {output_path}")
    return output_name

def check_pattern(profile: Profile):
    return None if profile.pattern_bg is None else "../assets/background-patterns/default.png"