import cv2

from src.utils.color_utils import create_gradient_rectangle
from src.utils.bg_remover import remove_background_fast
from src.utils.image_filters import decrease_contrast, apply_tint_filter, process_background_image, apply_gaussian_blur
from src.utils.masking import apply_mask
from src.utils.overlay_utils import overlay_image, add_images, create_fade_to_transparent, generate_gradient_mask_from_image
from src.utils.text_utils import add_text_center, add_text_fit_width, add_text
from src.utils.file_utils import save_poster
from src.models.Profile import Profile
from src.models.ColorPaletteGenerator import ColorPaletteGenerator, ColorPalette


def banner_service(profile: Profile, color_palette: ColorPalette = None):
    image_path = profile.picture
    bg_pattern_source = check_pattern(profile)
    person_name = profile.name
    person_header = profile.header

    if color_palette is None:
        color_palette = ColorPaletteGenerator(image_path)


    print(f"color paletet is: {color_palette}")
    left_bg = color_palette.accent_color_left
    right_bg = color_palette.accent_color_right
    text_color = color_palette.text_color

    profile_pic = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    cutout = remove_background_fast(profile_pic)
    background = create_gradient_rectangle(left_bg, right_bg)

    low_contrast = decrease_contrast(cutout, 0.1)
    tinted_cutout = apply_tint_filter(low_contrast, right_bg, strength=0.2)
    gradient_mask = generate_gradient_mask_from_image(profile_pic, fade_strength=1, interploation="quadratic")

    masked_cutout = apply_mask(tinted_cutout, gradient_mask)

    background = cv2.cvtColor(background, cv2.COLOR_RGB2RGBA)
    print(f"pattern is at {bg_pattern_source}")

    bg_pattern = cv2.imread(bg_pattern_source, cv2.IMREAD_UNCHANGED)
    bg_pattern = process_background_image(bg_pattern, opacity=0.2)
    bg_pattern = apply_mask(bg_pattern, generate_gradient_mask_from_image(bg_pattern, interploation="linear"))
    bg_pattern = apply_gaussian_blur(bg_pattern, 9)
    background = add_images(background, bg_pattern)
    background = add_text(background, "#Open to Work".upper(), text_color, y_offset=-200)

    poster = overlay_image(background.copy(), masked_cutout)
    fade_gradient = create_fade_to_transparent(left_bg, fade_strength=1.5)
    poster = add_images(poster, fade_gradient)
    poster = add_text_center(poster, person_name.upper(), font_size=70, color=text_color, letter_spacing=10,
                             y_offset=350)
    poster = add_text_fit_width(poster, person_header, color=text_color, letter_spacing=0, y_offset=450,
                                max_font_size=50)

    output_path, output_name = save_poster(poster, image_path)
    profile.generated_poster = output_name
    print(f"Banner saved at: {output_path}")
    return profile


def check_pattern(profile: Profile):
    return  "../assets/background-patterns/default.png" if profile.pattern_bg is None else profile.pattern_bg
