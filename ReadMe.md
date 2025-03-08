# LinkedIn Banner Creator 

A dynamic poster generator tailored for LinkedIn profiles. Creates professional "Open to Work" banners with custom color schemes derived from your profile picture. *No OpenAI integration—uses smart color analysis and user-provided patterns for backgrounds.*

## Poster Examples
| [<img src="https://payam.pro/wp-content/uploads/2025/03/payam-poster.png" width="300" alt="Tech Poster">](#) | [<img src="https://payam.pro/wp-content/uploads/2025/03/yaro4-poster.png" width="300" alt="Academic Poster">](#) |
|:---:|:---:|
| [<img src="https://payam.pro/wp-content/uploads/2025/03/yaro-2-poster.png" width="300" alt="Developer Poster">](#) | [<img src="https://payam.pro/wp-content/uploads/2025/03/yaro-1-poster.png" width="300" alt="Research Poster">](#) |


## Features
- **Smart Color Extraction**: Dominant & complementary colors extracted from your profile picture.
- **Gradient Backgrounds**: Seamless gradients based on analogous colors.
- **Custom Patterns**: Apply your own background patterns with adjustable opacity/blur.
- **Text Styling**: Auto-sized text with custom fonts, spacing, and contrast optimization.
- **Transparency Effects**: Soft fades, overlays, and clipping masks for professional polish.
- **Background Removal**: Fast subject isolation using `rembg`.

---

##  Installation
1. **Requirements**:  
   Python 3.8+ | OpenCV | NumPy | rembg | Matplotlib | Pillow  
   ```bash
   pip install -r requirements.txt
   ```

2. **Font Setup**:  
   Place your `.ttf` font file in `/assets/` and update `FONT_PATH` in `text_utils.py`.

---

## Usage
1. **Prepare Assets**:
   - Profile image (e.g., `sample-image/payam.png`).
   - Background pattern (optional, e.g., `background-patterns/payam-pattern-bg-2.png`).

2. **Create a Profile**:
   ```python
   from user_utils.Profile import Profile

   user = Profile(
       name="Payam Ranjbar",
       header="Unity Developer | Technical Game Designer",
       picture="path/to/profile.png",
       pattern_bg="path/to/pattern.png"  # Optional
   )
   ```

3. **Generate Poster**:
   ```python
   from main import generate_poster
   output_filename = generate_poster(user)
   ```

4. **View Color Palette** (Optional):
   ```python
   from main import plot_colors
   plot_colors(user.picture, output_filename)
   ```

---

## File Structure
```
.
├── utils/                 # Core modules
│   ├── color_wheel.py     # Color theory & extraction
│   ├── text_utils.py      # Text rendering & styling
│   ├── image_filters.py   # Blur, tint, contrast adjustments
│   └── ...                # Other utilities
├── background-patterns/   # Custom background images
├── sample-image/          # Example profile pictures
├── posters/               # Output directory
└── assets/                # Font files (e.g., Anton-Regular.ttf)
```

---

## Customization Tips
- **Background Patterns**: Use geometric/textured PNGs for `pattern_bg`.
- **Color Boosts**: Adjust saturation/luminance in `color_wheel.py`.
- **Text Styles**: Modify letter spacing/font sizes in `text_utils.py`.
- **Gradient Fades**: Tweak `fade_strength` in `overlay_utils.py`.

---

- **Performance**: Optimized for speed (resizing + k-means color clustering).
- **Transparency**: All outputs are PNGs with alpha channels.

