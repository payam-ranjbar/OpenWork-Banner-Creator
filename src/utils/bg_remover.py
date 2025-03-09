import cv2
from rembg import remove

def remove_background_fast(image, target_size=(500, 500)):
    print("> Removing background...")

    # Read the image
    if image is None:
        raise ValueError("Error: Image not found.")

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    original_size = image.shape[:2]
    image = cv2.resize(image, target_size)

    if image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)

    output = remove(image)

    # Resize back to original size
    output = cv2.resize(output, (original_size[1], original_size[0]))

    output = cv2.cvtColor(output, cv2.COLOR_RGBA2BGRA)

    return output
