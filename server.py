from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os
from models.Profile import Profile
from models.ColorPaletteGenerator import ColorPalette, ColorPaletteGenerator

app = FastAPI()

UPLOAD_FOLDER = "DB/profile-pictures/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/color-palette")
async def get_color_palette(
    name: str = Form(...),
    header: str = Form(...),
    picture: UploadFile = File(...)
):
    """
    Extracts a color palette from the uploaded profile picture.
    """
    # Save the profile picture
    profile_image_path = os.path.join(UPLOAD_FOLDER, picture.filename)
    with open(profile_image_path, "wb") as buffer:
        shutil.copyfileobj(picture.file, buffer)

    # Create a Profile instance
    profile = Profile(name=name, header=header, picture=profile_image_path)

    # Generate the color palette
    color_palette = ColorPaletteGenerator(profile.picture).get_palette()

    return color_palette
