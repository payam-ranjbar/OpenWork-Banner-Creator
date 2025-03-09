from src.models.ColorPaletteGenerator import ColorPaletteGenerator, ColorPalette
from src.models.Profile import Profile


def get_color_palette_img(profile: Profile):
    generator = ColorPaletteGenerator(profile.picture)
    return generator.get_palette()
