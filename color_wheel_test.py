import numpy as np
import cv2
from utils.color_wheel import get_complementary_color, get_colors, get_dominant_color,get_analogous_colors, increase_saturation
from utils.bg_remover import remove_background_fast
from utils.file_utils import load_image_rgb
from utils.file_utils import get_unique_filename
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

def plot_colors(image_path):
    # Load images and process colors
    base_image = load_image_rgb(image_path)
    cutout = remove_background_fast(image_path)

    dom_color_og = get_dominant_color(base_image)
    complementary_color = get_complementary_color(dom_color_og)
    left_bg, right_bg, text_color = get_colors(image_path, dom_color_og)
    # _, left_bg, right_bg= get_analogous_colors(complementary_color)
    sat_increase = 2
    # left_bg, right_bg, dom_color_og = increase_saturation(left_bg,sat_increase ), increase_saturation(right_bg,sat_increase ), increase_saturation(dom_color_og,sat_increase )
    color_labels = ["Dom Color", "Comp Color", "Left", "Right ", "Text"]
    color_values = [dom_color_og, complementary_color, left_bg, right_bg, text_color]

    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle("Extracted Colors from Image", fontsize=16)

    # Plot the color palette on the left subplot
    for i, (color, label) in enumerate(zip(color_values, color_labels)):
        rect = plt.Rectangle((i * 1.1, 0), 1, 1, color=np.array(color) / 255)
        ax1.add_patch(rect)
        ax1.text(i * 1.1 + 0.5, -0.2, label, ha='center', va='center', fontsize=10, color="black")

    ax1.set_xlim(0, len(color_values) * 1.1)
    ax1.set_ylim(-0.5, 1)
    ax1.set_xticks([])  # Remove x-axis
    ax1.set_yticks([])  # Remove y-axis

    # Plot the input image on the right subplot
    ax2.imshow(base_image)
    ax2.set_xticks([])  # Remove x-axis
    ax2.set_yticks([])  # Remove y-axis

    # Adjust layout and save the figure
    plt.tight_layout()
    path = get_unique_filename("color-palette", "pallet.png")
    plt.savefig(path)  # Save the figure as an image
    print(f"✅ Color visualization saved as '{path}'")



# Example Usage

if __name__ == "__main__":
    image_path = "sample-image/payam.png"  # Update this path
    plot_colors(image_path)
