import cv2

def add_text(image, text, color, font_scale=4, thickness=6):
    """Adds centered text across the width of the image."""
    print("📝 Adding text to the image...")
    height, width, _ = image.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = (width - text_size[0]) // 2
    text_y = height - 80

    cv2.putText(image, text, (text_x, text_y), font, font_scale, color, thickness, cv2.LINE_AA)
    return image
