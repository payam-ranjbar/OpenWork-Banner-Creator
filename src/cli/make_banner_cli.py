import argparse
import os

import cv2
import matplotlib.pyplot as plt
from src.models.ColorPaletteGenerator import ColorPaletteGenerator
from src.models.Profile import Profile
from src.service.banner_service import generate_banner


def generate_from_profile():
    parser = argparse.ArgumentParser(
        description="Generate a LinkedIn banner using profile data (name, header, profile pic)")
    parser.add_argument("name", type=str, help="display name on banner")
    parser.add_argument("header", type=str, help="display linkedin header (occupation)")
    parser.add_argument("picture", type=str, help="profile picture path")
    parser.add_argument("--pattern", type=str, default=None, help="Path to an optional background pattern.")
    parser.add_argument("--popup", action="store_true", help="Show the generated banner")
    parser.add_argument("--palette", action="store_true", help="Show the extracted color palette.")

    args = parser.parse_args()

    if not os.path.exists(args.picture):
        print("profile picture address invalid")
        return
    if args.pattern and not os.path.exists(args.pattern):
        print("background pattern address invalid")
        return

    picture_path = os.path.abspath(args.picture)
    pattern_bg_path = os.path.abspath(args.pattern) if args.pattern else None
    user_profile = Profile(
        name=args.name,
        header=args.header,
        picture=picture_path,
        pattern_bg=pattern_bg_path
    )

    out_profile = generate_banner(user_profile)
    print(f">>>> Banner created successfully")
    if args.palette:
        palette = ColorPaletteGenerator(args.picture)
        palette.plot_palette()

    if args.popup:
        image = cv2.imread(out_profile.generated_poster)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        plt.imshow(image_rgb)
        plt.axis("off")
        plt.show()

if __name__ == "__main__":
    generate_from_profile()
