import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

FONT_PATH = "../../assets/Anton-Regular.ttf"


def add_text(image, text, color, max_font_size=500, min_font_size=60, letter_spacing=30, y_offset=0):
    """Adds centered, uppercase text with a custom font that covers the image width and allows letter spacing."""
    print("> Adding spaced text to the image with custom font...")


    color_rgb = (color[2], color[1], color[0])  # Convert BGR → RGB
    color = color_rgb
    # Convert OpenCV image to PIL for better text rendering
    image_pil = Image.fromarray(image)

    font = None

    draw = ImageDraw.Draw(image_pil)
    width, height = image_pil.size

    # Start with a large font size and decrease until it fits
    font_size = max_font_size

    while font_size > min_font_size:
        font = ImageFont.truetype(FONT_PATH, font_size)

        # Measure text size with letter spacing
        text_width = sum(
            (font.getbbox(char)[2] - font.getbbox(char)[0]) + letter_spacing for char in text) - letter_spacing
        text_height = font.getbbox(text)[3] - font.getbbox(text)[1]

        if text_width < width * 0.9:
            break
        font_size -= 5  # Reduce font size in small steps

    # Calculate start position (center horizontally and vertically)
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    text_y = text_y + y_offset

    # Draw each letter separately with spacing
    x_cursor = text_x
    for char in text:
        draw.text((x_cursor, text_y), char, font=font, fill=color)
        x_cursor += (font.getbbox(char)[2] - font.getbbox(char)[0]) + letter_spacing  # Move cursor for next letter

    print(f">> Text added with font size {font_size}, centered with letter spacing {letter_spacing}.")

    # Convert back to OpenCV format
    return np.array(image_pil)


def add_text_fit_width(image, text, color, letter_spacing=10, y_offset=0, max_font_size=90, min_font_size=10):
    return add_text(image, text, color, max_font_size=max_font_size, min_font_size=min_font_size, letter_spacing=letter_spacing, y_offset=y_offset)

def add_text_center(image, text, font_size, color, letter_spacing=10, y_offset=0):


    # BGR to a PIL image
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except IOError:
        print(f"Error: Font file not found at {FONT_PATH}. Using default font.")
        font = ImageFont.load_default()

    # Create a drawing context
    draw = ImageDraw.Draw(image_pil)

    total_width = 0
    max_height = 0

    for char in text:
        # Get the bounding box of the character
        bbox = draw.textbbox((0, 0), char, font=font)
        char_width = bbox[2] - bbox[0]  # Calculate width from bounding box
        char_height = bbox[3] - bbox[1]  # Calculate height from bounding box

        # Update total width and max height
        total_width += char_width + letter_spacing
        if char_height > max_height:
            max_height = char_height

    # Remove the extra letter spacing for the last character
    total_width -= letter_spacing

    # Calculate the starting position for centered text
    image_width, image_height = image_pil.size
    text_x = (image_width - total_width) // 2  # Center horizontally
    text_y = (image_height - max_height) // 2 + y_offset  # Center vertically with offset

    # Initialize the starting position
    x_offset = text_x

    # Loop through each character in the text
    for char in text:
        # Get the bounding box of the character
        bbox = draw.textbbox((x_offset, text_y), char, font=font)
        char_width = bbox[2] - bbox[0]  # Calculate width from bounding box

        # Add the character to the image
        draw.text((x_offset, text_y), char, font=font, fill=color[::-1])  # PIL uses RGB, so reverse BGR to RGB

        # Update the x-coordinate for the next character
        x_offset += char_width + letter_spacing

    # Convert the PIL image back to OpenCV format (BGR)
    image_with_text = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

    return image_with_text


