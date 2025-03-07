import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from utils.color_utils import extract_colors, create_gradient_rectangle, get_dominant_color
from utils.color_wheel import get_analogous_colors, get_complementary_color, get_best_text_color
from utils.text_utils import add_text
from utils.bg_remover import remove_background_fast
from utils.image_filters import apply_tint_filter, decrease_contrast, process_background_image
from utils.overlay_utils import overlay_image, create_fade_to_transparent, add_images
from utils.file_utils import save_poster, load_image_rgb, get_unique_filename
from utils.blending_modes import blend_overlay


def get_colors(image_path):
    base_image = load_image_rgb(image_path)
    dom_color = get_dominant_color(base_image)
    complementary_color = get_complementary_color(dom_color)
    left_bg, right_bg = get_analogous_colors(dom_color)
    text_color = complementary_color
    return left_bg, right_bg, text_color

def generate_poster(image_path, bg_pattern_source):
    """Main function that generates the poster."""
    print("\n🚀 Starting Poster Generation Pipeline...")

    # left_bg, right_bg, text_color = extract_colors(image_path)

    left_bg, right_bg, text_color = get_colors(image_path)
    # Load images and process colors
    cutout = remove_background_fast(image_path)
    background = create_gradient_rectangle(left_bg, right_bg)

    low_contrast = decrease_contrast(cutout, 0.1)
    tinted = apply_tint_filter(low_contrast, right_bg, strength=0.2)

    background = cv2.cvtColor(background, cv2.COLOR_RGB2RGBA)

    bg_pattern = process_background_image(bg_pattern_source, opacity=0.2)

    background = add_images(background, bg_pattern)
    background = add_text(background, "#Open to Work", text_color)

    poster = overlay_image(background.copy(), tinted)

    fade_gradient = create_fade_to_transparent(right_bg, fade_strength=1)
    poster = add_images(poster, fade_gradient)

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

# Example Usage
if __name__ == "__main__":
    image_path = "sample-image/ali.png"
    bg_pattern_source = "background-patterns/soroosh-pattern-bg.png"
    output = generate_poster(image_path, bg_pattern_source)
    plot_colors(image_path, output)
