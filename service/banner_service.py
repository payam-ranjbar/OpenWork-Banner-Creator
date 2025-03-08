import cv2
import numpy as np
from utils.file_utils import get_unique_filename
from utils.bg_remover import remove_background_fast
from utils.image_filters import decrease_contrast, apply_tint_filter
from utils.overlay_utils import overlay_image, add_images, create_fade_to_transparent
from utils.text_utils import add_text_center, add_text_fit_width
from models.Profile import Profile
from models.ColorPalette import ColorPalette


def generate_banner(profile: Profile, color_palette: ColorPalette = None):
    image_path = profile.picture
    person_name = profile.name
    person_header = profile.header

    if color_palette is None:
        color_palette = ColorPalette(image_path)

    left_bg = color_palette.accent_color_left
    right_bg = color_palette.accent_color_right
    text_color = color_palette.title_text_color

    profile_pic = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    cutout = remove_background_fast(profile_pic)
    low_contrast = decrease_contrast(cutout, 0.1)
    tinted_cutout = apply_tint_filter(low_contrast, right_bg, strength=0.2)
    background = add_images(np.full((1080, 1920, 3), left_bg, dtype=np.uint8),
                            np.full((1080, 1920, 3), right_bg, dtype=np.uint8))

    poster = overlay_image(background.copy(), tinted_cutout)
    fade_gradient = create_fade_to_transparent(left_bg, fade_strength=1.5)
    poster = add_images(poster, fade_gradient)
    poster = add_text_center(poster, person_name.upper(), font_size=70, color=text_color, letter_spacing=10,
                             y_offset=350)
    poster = add_text_fit_width(poster, person_header, color=text_color, letter_spacing=0, y_offset=450,
                                max_font_size=50)

    output_path = get_unique_filename("assets/banners", f"{person_name}_banner.png")
    cv2.imwrite(output_path, poster)
    print(f"✅ Banner saved at: {output_path}")
    return output_path
