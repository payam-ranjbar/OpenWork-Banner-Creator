import cv2
from rembg import remove

def remove_background_fast(image_path, target_size=(500, 500)):
    """Removes background using rembg with faster processing."""
    print("⚡ Removing background...")

    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # Resize for faster processing (optional)
    original_size = image.shape[:2]  # Store original size
    image = cv2.resize(image, target_size)

    # Convert to RGBA if needed
    if image.shape[2] == 3:  # If no alpha channel, add one
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)

    # Remove the background
    output = remove(image)

    output = cv2.resize(output, (original_size[1], original_size[0]))


    return output
