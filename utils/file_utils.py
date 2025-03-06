import os
import cv2

def get_unique_filename(base_path, filename):
    """Returns a unique filename by adding numbers if the file already exists."""
    base_name, ext = os.path.splitext(filename)
    full_path = os.path.join(base_path, filename)
    counter = 1

    while os.path.exists(full_path):
        full_path = os.path.join(base_path, f"{base_name}-{counter}{ext}")
        counter += 1

    return full_path

def save_poster(image, image_path):
    """Saves the poster in the 'posters/' directory with a unique filename."""
    print("💾 Saving poster...")

    os.makedirs("posters", exist_ok=True)  # Ensure the directory exists

    output_path = get_unique_filename("posters", f"{os.path.basename(image_path).split('.')[0]}-poster.png")

    cv2.imwrite(output_path, image)  # Save the poster
    print(f"✅ Poster saved at: {output_path}")

    return output_path
