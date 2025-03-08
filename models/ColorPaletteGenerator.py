import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from utils.color_wheel import (
    get_dominant_color, get_complementary_color, get_colors
)
from utils.file_utils import get_unique_filename, load_image_rgb

from pydantic import BaseModel

from typing import Tuple

class ColorPalette(BaseModel):
    primary_color: Tuple[int, int, int]
    secondary_color: Tuple[int, int, int]
    accent_color_left: Tuple[int, int, int]
    accent_color_right: Tuple[int, int, int]
    text_color: Tuple[int, int, int]

class ColorPaletteGenerator:
    def __init__(self, image_path):
        """Extracts a color palette from an image."""
        self.image_path = image_path
        self._base_image = load_image_rgb(image_path)
        self._extract_colors()

    def _extract_colors(self):
        self._primary_color = get_dominant_color(self._base_image)
        self._secondary_color = get_complementary_color(self._primary_color)
        self._accent_color_left, self._accent_color_right, self._text_color = get_colors(self.image_path,
                                                                                         self._primary_color)
        self._title_text_color = self._text_color
        self._subtitle_text_color = self._text_color

    @property
    def primary_color(self):
        return self._primary_color

    @property
    def secondary_color(self):
        return self._secondary_color

    @property
    def accent_color_left(self):
        return self._accent_color_left

    @property
    def accent_color_right(self):
        return self._accent_color_right

    @property
    def title_text_color(self):
        return self._title_text_color

    @property
    def subtitle_text_color(self):
        return self._subtitle_text_color

    def get_palette(self) -> ColorPalette:
        """
        Returns a structured color palette as a Pydantic model.
        """
        return ColorPalette(
            primary_color=self._primary_color,
            secondary_color=self._secondary_color,
            accent_color_left=self._accent_color_left,
            accent_color_right=self._accent_color_right,
            text_color=self._text_color,
        )
    def plot_palette(self):
        """Visualizes the generated color palette and saves it as a PNG file."""
        labels = [
            "Primary Color", "Secondary Color", "Accent Left", "Accent Right", "Title Text", "Subtitle Text"
        ]
        colors = [
            self.primary_color, self.secondary_color, self.accent_color_left, self.accent_color_right,
            self.title_text_color, self.subtitle_text_color
        ]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        fig.suptitle("Extracted Colors from Image", fontsize=16)

        # Plot the color palette
        for i, (label, color) in enumerate(zip(labels, colors)):
            rect = plt.Rectangle((i * 1.1, 0), 1, 1, color=np.array(color) / 255)
            ax1.add_patch(rect)
            ax1.text(i * 1.1 + 0.5, -0.2, label, ha='center', va='center', fontsize=10, color="black")

        ax1.set_xlim(0, len(colors) * 1.1)
        ax1.set_ylim(-0.5, 1)
        ax1.set_xticks([])
        ax1.set_yticks([])

        # Plot the input image
        ax2.imshow(self._base_image)
        ax2.set_xticks([])
        ax2.set_yticks([])

        # Adjust layout and save the figure
        plt.tight_layout()
        os.makedirs("assets/color_palette", exist_ok=True)
        file_name = os.path.basename(self.image_path).split('.')[0] + "_palette.png"
        save_path = get_unique_filename("../assets/color_palette", file_name)
        plt.savefig(save_path)
        print(f"✅ Color palette saved as '{save_path}'")
        plt.show()


