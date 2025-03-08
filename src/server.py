from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os
from src.models.Profile import Profile
from src.models.ColorPaletteGenerator import ColorPalette, ColorPaletteGenerator
from src.service.banner_service import banner_service
app = FastAPI()

UPLOAD_FOLDER = "../DB/profile-pictures/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/color-palette")
async def get_color_palette(
    name: str = Form(...),
    header: str = Form(...),
    picture: UploadFile = File(...)
):

    profile = await save_profile_picture(name, header, picture)

    generator = ColorPaletteGenerator(profile.picture)
    generator.plot_palette()
    color_palette = generator.get_palette()

    return color_palette




@app.post("/banner")
async def get_banner_from_profile(
        name: str = Form(...),
        header: str = Form(...),
        picture: UploadFile = File(...)
):
    profile = await save_profile_picture(name, header, picture)
    generator = ColorPaletteGenerator(profile.picture)
    banner = banner_service(profile, generator.get_palette())
    return banner


async def save_profile_picture(name, header, picture):
    profile_image_path = os.path.join(UPLOAD_FOLDER, picture.filename)
    profile = None
    with open(profile_image_path, "wb") as buffer:
        shutil.copyfileobj(picture.file, buffer)
        profile = Profile(name=name, header=header, picture=profile_image_path)
    return profile





