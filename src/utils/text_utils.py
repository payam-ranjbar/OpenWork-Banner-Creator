import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

# Path to the custom font file (update this with your actual font)
FONT_PATH = "../../assets/Anton-Regular.ttf"


def add_text(image, text, color, max_font_size=500, min_font_size=60, letter_spacing=30, y_offset=0):
    """Adds centered, uppercase text with a custom font that covers the image width and allows letter spacing."""
    print("📝 Adding spaced text to the image with custom font...")


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

    print(f"✅ Text added with font size {font_size}, centered with letter spacing {letter_spacing}.")

    # Convert back to OpenCV format
    return np.array(image_pil)


def add_text_fit_width(image, text, color, letter_spacing=10, y_offset=0, max_font_size=90, min_font_size=10):
    return add_text(image, text, color, max_font_size=max_font_size, min_font_size=min_font_size, letter_spacing=letter_spacing, y_offset=y_offset)

def add_text_center(image, text, font_size, color, letter_spacing=10, y_offset=0):
    """
    Adds centered text to an image using a custom TTF font.

    Parameters:
    - image (np.ndarray): Input image (BGR format).
    - text (str): Text to add.
    - font_size (int): Font size.
    - color (tuple): Text color in BGR format (e.g., (255, 0, 0) for red).
    - letter_spacing (int): Spacing between letters (default: 10).
    - FONT_PATH (str): Path to the TTF font file (default: "arial.ttf").
    - y_offset (int): Vertical offset from the center (default: 0).

    Returns:
    - np.ndarray: Image with centered text added.
    """
    # Convert the OpenCV image (BGR) to a PIL image (RGB)
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Load the TTF font
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except IOError:
        print(f"Error: Font file not found at {FONT_PATH}. Using default font.")
        font = ImageFont.load_default()

    # Create a drawing context
    draw = ImageDraw.Draw(image_pil)

    # Calculate the total width and height of the text
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



def add_text_fit_width_uppercase(image, text, color, letter_spacing=10, FONT_PATH="arial.ttf", y_offset=0, max_font_size=100, first_letter_scale=1.5):
    """
    Adds text to an image, fitting it within the width of the image, with the first letter of each word slightly larger.

    Parameters:
    - image (np.ndarray): Input image (BGR format).
    - text (str): Text to add.
    - color (tuple): Text color in BGR format (e.g., (255, 0, 0) for red).
    - letter_spacing (int): Spacing between letters (default: 10).
    - FONT_PATH (str): Path to the TTF font file (default: "arial.ttf").
    - y_offset (int): Vertical offset from the center (default: 0).
    - max_font_size (int): Maximum font size (default: 100).
    - first_letter_scale (float): Scale factor for the first letter of each word (default: 1.5).

    Returns:
    - np.ndarray: Image with fitted text added.
    """
    # Convert the OpenCV image (BGR) to a PIL image (RGB)
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Get the width and height of the image
    image_width, image_height = image_pil.size

    # Initialize font size
    font_size = 1

    # Load the TTF font
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except IOError:
        print(f"Error: Font file not found at {FONT_PATH}. Using default font.")
        font = ImageFont.load_default()

    # Create a drawing context
    draw = ImageDraw.Draw(image_pil)

    # Split the text into words
    words = text.upper().split()

    # Calculate the total width of the text with the current font size
    total_width = 0
    for word in words:
        for i, char in enumerate(word):
            if i == 0:
                # Use a larger font size for the first letter
                first_letter_font = ImageFont.truetype(FONT_PATH, int(font_size * first_letter_scale))
                char_width = draw.textbbox((0, 0), char, font=first_letter_font)[2] - draw.textbbox((0, 0), char, font=first_letter_font)[0]
            else:
                char_width = draw.textbbox((0, 0), char, font=font)[2] - draw.textbbox((0, 0), char, font=font)[0]
            total_width += char_width + letter_spacing
        total_width += letter_spacing  # Add space between words

    # Remove the extra letter spacing for the last character
    total_width -= letter_spacing

    # Increase font size until the text fits within the image width or reaches max_font_size
    while total_width < image_width and font_size < max_font_size:
        font_size += 1
        try:
            font = ImageFont.truetype(FONT_PATH, font_size)
        except IOError:
            font = ImageFont.load_default()
        total_width = 0
        for word in words:
            for i, char in enumerate(word):
                if i == 0:
                    first_letter_font = ImageFont.truetype(FONT_PATH, int(font_size * first_letter_scale))
                    char_width = draw.textbbox((0, 0), char, font=first_letter_font)[2] - draw.textbbox((0, 0), char, font=first_letter_font)[0]
                else:
                    char_width = draw.textbbox((0, 0), char, font=font)[2] - draw.textbbox((0, 0), char, font=font)[0]
                total_width += char_width + letter_spacing
            total_width += letter_spacing  # Add space between words
        total_width -= letter_spacing

    # Decrease font size by 1 to ensure the text fits
    font_size -= 1
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except IOError:
        font = ImageFont.load_default()

    # Recalculate the total width with the final font size
    total_width = 0
    for word in words:
        for i, char in enumerate(word):
            if i == 0:
                first_letter_font = ImageFont.truetype(FONT_PATH, int(font_size * first_letter_scale))
                char_width = draw.textbbox((0, 0), char, font=first_letter_font)[2] - draw.textbbox((0, 0), char, font=first_letter_font)[0]
            else:
                char_width = draw.textbbox((0, 0), char, font=font)[2] - draw.textbbox((0, 0), char, font=font)[0]
            total_width += char_width + letter_spacing
        total_width += letter_spacing  # Add space between words
    total_width -= letter_spacing

    # Calculate the maximum height of the text
    max_height = 0
    for word in words:
        for i, char in enumerate(word):
            if i == 0:
                first_letter_font = ImageFont.truetype(FONT_PATH, int(font_size * first_letter_scale))
                char_height = draw.textbbox((0, 0), char, font=first_letter_font)[3] - draw.textbbox((0, 0), char, font=first_letter_font)[1]
            else:
                char_height = draw.textbbox((0, 0), char, font=font)[3] - draw.textbbox((0, 0), char, font=font)[1]
            if char_height > max_height:
                max_height = char_height

    # Calculate the starting position for centered text
    text_x = (image_width - total_width) // 2  # Center horizontally
    text_y = (image_height - max_height) // 2 + y_offset  # Center vertically with offset

    # Initialize the starting position
    x_offset = text_x

    # Loop through each word and character
    for word in words:
        for i, char in enumerate(word):
            if i == 0:
                # Use a larger font size for the first letter
                first_letter_font = ImageFont.truetype(FONT_PATH, int(font_size * first_letter_scale))
                char_width = draw.textbbox((0, 0), char, font=first_letter_font)[2] - draw.textbbox((0, 0), char, font=first_letter_font)[0]
                draw.text((x_offset, text_y), char, font=first_letter_font, fill=color[::-1])  # PIL uses RGB, so reverse BGR to RGB
            else:
                char_width = draw.textbbox((0, 0), char, font=font)[2] - draw.textbbox((0, 0), char, font=font)[0]
                draw.text((x_offset, text_y), char, font=font, fill=color[::-1])  # PIL uses RGB, so reverse BGR to RGB
            x_offset += char_width + letter_spacing
        x_offset += letter_spacing  # Add space between words

    # Convert the PIL image back to OpenCV format (BGR)
    image_with_text = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

    return image_with_text


def add_text_center_first_letter_larger(image, text, font_size, color, letter_spacing=10, y_offset=0, first_letter_scale=1.5,):
 # Convert the OpenCV image (BGR) to a PIL image (RGB)
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Load the TTF font
    try:
        base_font = ImageFont.truetype(FONT_PATH, font_size)
        first_letter_font = ImageFont.truetype(FONT_PATH, int(font_size * first_letter_scale))
    except IOError:
        print(f"Error: Font file not found at {FONT_PATH}. Using default font.")
        base_font = ImageFont.load_default()
        first_letter_font = ImageFont.load_default()

    # Create a drawing context
    draw = ImageDraw.Draw(image_pil)

    # Split the text into words
    words = text.upper().split()  # Convert to uppercase and split into words

    # Calculate the total width and height of the text
    total_width = 0
    max_height = 0

    for word in words:
        for i, char in enumerate(word):
            # Use larger font for the first letter of each word
            if i == 0:
                font = first_letter_font
            else:
                font = base_font

            # Get the bounding box of the character
            bbox = draw.textbbox((0, 0), char, font=font)
            char_width = bbox[2] - bbox[0]  # Calculate width from bounding box
            char_height = bbox[3] - bbox[1]  # Calculate height from bounding box

            # Update total width and max height
            total_width += char_width + letter_spacing
            if char_height > max_height:
                max_height = char_height

        # Add space between words (except after the last word)
        if word != words[-1]:
            total_width += base_font.getlength(" ")  # Add space width

    # Remove the extra letter spacing for the last character
    total_width -= letter_spacing

    # Calculate the starting position for centered text
    image_width, image_height = image_pil.size
    text_x = (image_width - total_width) // 2  # Center horizontally
    text_y = (image_height - max_height) // 2 + y_offset  # Center vertically with offset

    # Initialize the starting position
    x_offset = text_x

    # Loop through each word
    for word in words:
        for i, char in enumerate(word):
            # Use larger font for the first letter of each word
            if i == 0:
                font = first_letter_font
                # Adjust the y-coordinate to align the baseline
                bbox = draw.textbbox((x_offset, text_y), char, font=font)
                char_height = bbox[3] - bbox[1]
                y_char = text_y + (max_height - char_height)  # Align baseline
            else:
                font = base_font
                y_char = text_y  # Use the baseline for smaller letters

            # Get the bounding box of the character
            bbox = draw.textbbox((x_offset, y_char), char, font=font)
            char_width = bbox[2] - bbox[0]  # Calculate width from bounding box

            # Add the character to the image
            draw.text((x_offset, y_char), char, font=font, fill=color[::-1])  # PIL uses RGB, so reverse BGR to RGB

            # Update the x-coordinate for the next character
            x_offset += char_width + letter_spacing

        # Add space between words (except after the last word)
        if word != words[-1]:
            x_offset += base_font.getlength(" ")  # Add space width

    # Convert the PIL image back to OpenCV format (BGR)
    image_with_text = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

    return image_with_text