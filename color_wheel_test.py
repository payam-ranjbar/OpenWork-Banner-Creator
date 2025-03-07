import numpy as np
import cv2
from utils.color_wheel import get_analogous_colors,get_complementary_color
from utils.bg_remover import remove_background_fast
from utils.file_utils import save_poster, load_image_rgb
from utils.color_utils import extract_colors, create_gradient_rectangle, get_dominant_color
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
def plot_colors(image_path, output_name):
    """
    Loads an image, extracts important colors, and displays them using Matplotlib.

    Parameters:
    - image_path (str): Path to the input image.
    """

    # Load images and process colors
    base_image = load_image_rgb(image_path)
    cutout = remove_background_fast(image_path)

    dom_color = get_dominant_color(base_image)
    complementary_color = get_complementary_color(dom_color)
    left_bg, right_bg = get_analogous_colors(dom_color)

    # text_color = get_complementary_color(get_dominant_color(base_image))
    text_color = complementary_color

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

    plt.savefig("color_visualization.png")  # Save the figure as an image
    print("✅ Color visualization saved as 'color_visualization.png'")


# Example Usage

if __name__ == "__main__":
    image_path = "sample-image/ali.png"  # Update this path
    plot_colors(image_path)
