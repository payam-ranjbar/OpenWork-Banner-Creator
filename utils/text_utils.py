import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

# Path to the custom font file (update this with your actual font)
FONT_PATH = "../assets/Anton-Regular.ttf"

def add_text(image, text, color, max_font_size=500, min_font_size=60, letter_spacing=30):
    """Adds centered, uppercase text with a custom font that covers the image width and allows letter spacing."""
    print("📝 Adding spaced text to the image with custom font...")

    text = text.upper()  # Convert text to ALL CAPS

    color_rgb = (color[2], color[1], color[0])  # Convert BGR → RGB
    color = color_rgb
    # Convert OpenCV image to PIL for better text rendering
    image_pil = Image.fromarray(image)

    draw = ImageDraw.Draw(image_pil)
    width, height = image_pil.size

    # Start with a large font size and decrease until it fits
    font_size = max_font_size
    while font_size > min_font_size:
        font = ImageFont.truetype(FONT_PATH, font_size)

        # Measure text size with letter spacing
        text_width = sum((font.getbbox(char)[2] - font.getbbox(char)[0]) + letter_spacing for char in text) - letter_spacing
        text_height = font.getbbox(text)[3] - font.getbbox(text)[1]

        text_height = text_height + 70
        if text_width < width * 0.9:  # Ensure text covers ~90% of width
            break
        font_size -= 5  # Reduce font size in small steps

    # Calculate start position (center horizontally and vertically)
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    # Draw each letter separately with spacing
    x_cursor = text_x
    for char in text:
        draw.text((x_cursor, text_y), char, font=font, fill=color)
        x_cursor += (font.getbbox(char)[2] - font.getbbox(char)[0]) + letter_spacing  # Move cursor for next letter

    print(f"✅ Text added with font size {font_size}, centered with letter spacing {letter_spacing}.")

    # Convert back to OpenCV format
    return np.array(image_pil)