import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from utils.color_utils import create_gradient_rectangle
from utils.color_wheel import get_colors, get_complementary_color, get_dominant_color
from utils.text_utils import add_text, add_text_center, add_text_fit_width , add_text_center_first_letter_larger
from utils.bg_remover import remove_background_fast
from utils.image_filters import apply_tint_filter, decrease_contrast, process_background_image, apply_gaussian_blur
from utils.overlay_utils import overlay_image, create_fade_to_transparent, add_images, generate_gradient_mask_from_image
from utils.file_utils import save_poster, load_image_rgb, get_unique_filename
from utils.blending_modes import blend_overlay
from utils.masking import apply_mask
from user_utils.Profile import Profile

def generate_poster(user_profile: Profile):
    """Main function that generates the poster."""
    print("\n🚀 Starting Poster Generation Pipeline...")

    image_path = user_profile.picture
    bg_pattern_source = user_profile.pattern_bg

    person_name = user_profile.name
    person_header = user_profile.header


    left_bg, right_bg, text_color = get_colors(image_path)
    profile_pic = cv2.imread(image_path,cv2.IMREAD_UNCHANGED )
    cutout = remove_background_fast(profile_pic)
    background = create_gradient_rectangle(left_bg, right_bg)

    low_contrast = decrease_contrast(cutout, 0.1)
    tinted_cutout = apply_tint_filter(low_contrast, right_bg, strength=0.2)
    gradient_mask = generate_gradient_mask_from_image(profile_pic, fade_strength=1, interploation= "quadratic")
    masked_cutout = apply_mask(tinted_cutout, gradient_mask)

    debug_save_gradient_mask(gradient_mask)
    background = cv2.cvtColor(background, cv2.COLOR_RGB2RGBA)

    bg_pattern = process_background_image(bg_pattern_source, opacity=0.2)

    bg_pattern = apply_mask(bg_pattern, generate_gradient_mask_from_image(bg_pattern, interploation="linear"))
    bg_pattern = apply_gaussian_blur(bg_pattern, 9)
    background = add_images(background, bg_pattern)
    background = add_text(background, "#Open to Work".upper(), text_color, y_offset=-200)

    poster = overlay_image(background.copy(), masked_cutout)

    fade_gradient = create_fade_to_transparent(left_bg, fade_strength=1.5)
    poster = add_images(poster, fade_gradient)
    poster = add_text_center(image=poster, text=person_name.upper(), font_size=70, color=text_color, letter_spacing=10, y_offset=350, )
    poster = add_text_fit_width(image=poster, text=person_header, color=text_color, letter_spacing=0, y_offset=450,
                                max_font_size=50)
    # 🔹 Save the final poster using `save_poster()`
    output_path, output_name = save_poster(poster, image_path)

    return output_name


def plot_colors(image_path, output_name):


    base_image = load_image_rgb(image_path)
    dom_color = get_dominant_color(base_image)
    complementary_color = get_complementary_color(dom_color)
    left_bg, right_bg, text_color = get_colors(image_path)

    # Create color labels and values
    color_labels = ["Dominant Color", "Complementary Color", "Left Analogous", "Right Analogous", "Text Color"]
    color_values = [dom_color, complementary_color, left_bg, right_bg, text_color]

    # Create a blank figure
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xticks([])  # Remove x-axis
    ax.set_yticks([])  # Remove y-axis
    ax.set_title("Extracted Colors from Image")

    # Create color swatches
    for i, (color, label) in enumerate(zip(color_values, color_labels)):
        rect = plt.Rectangle((i * 1.1, 0), 1, 1, color=np.array(color) / 255)
        ax.add_patch(rect)
        ax.text(i * 1.1 + 0.5, -0.2, label, ha='center', va='center', fontsize=10, color="black")

    # Adjust axis limits and save as an image (fixes display issues)
    ax.set_xlim(0, len(color_values) * 1.1)
    ax.set_ylim(-0.5, 1)

    path ="color-pallert-" + output_name
    path = get_unique_filename("", path)
    plt.savefig(path) # Save the figure as an image
    print(f"✅ Color visualization saved as '{path}'")

def debug_save_gradient_mask(mask, filename="debug_mask.png", show=False):

        print(f"🖼️ Saving gradient mask as '{filename}'...")

        # Ensure mask is in correct grayscale format
        if len(mask.shape) == 3:
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

        # Save the mask
        cv2.imwrite(filename, mask)
        print(f"✅ Gradient mask saved: {filename}")

        # Optionally show the mask
        if show:
            cv2.imshow("Gradient Mask Debug", mask)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

# Example Usage
if __name__ == "__main__":

    payam = Profile(name="Payam Ranjbar",
                    header = "Unity Developer | Software Engineer | Technical Game Designer",
                    picture = "sample-image/payam.png",
                    pattern_bg = "background-patterns/payam-pattern-bg-2.png")

    soroosh = Profile(name="Soroosh Esmalian",
                    header = "Backend Developer | Skilled in Next.js, Django, Express.js, Java, AWS | Master's in CS | Interested in CyberSecurity",
                    picture = "sample-image/soroosh-head.jpg",
                    pattern_bg = "background-patterns/soroosh-pattern-bg.png")

    pezh = Profile(name=" Pezhvak Moghaddasi",
                    header = "MSc Chemist | Electrochemist | Computational Materials Scientist",
                    picture = "sample-image/pezhvak-head.jpg",
                    pattern_bg = "background-patterns/pezh-pattern-2.png")

    drvoid = Profile (name="Ali M. Dehaghi",
                    header = "PhD Candidate | Computer Vision Researcher",
                    picture = "sample-image/drvoid.png",
                    pattern_bg = "background-patterns/drvoid-pattern-bg.png")

    ali = Profile(name="Ali Salmani",
                    header = "Software Engineer, AI and Machine Learning",
                    picture = "sample-image/ali.png",
                    pattern_bg = "background-patterns/alis-p-2.png")

    pic = cv2.imread(payam.picture, cv2.IMREAD_UNCHANGED)
    # mask = generate_gradient_mask_from_image(pic,fade_strength=0.7)
    # debug_save_gradient_mask(mask)
    user = ali
    output = generate_poster(payam)
    output = generate_poster(soroosh)
    output = generate_poster(pezh)
    output = generate_poster(drvoid)
    output = generate_poster(ali)
    # plot_colors(user.picture, output)
