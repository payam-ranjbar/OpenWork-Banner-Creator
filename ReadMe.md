# LinkedIn Banner Creator 

A dynamic poster generator tailored for LinkedIn profiles. 
Creates professional "Open to Work" banners with custom color schemes derived from your profile picture.

## Poster Examples
| [<img src="https://payam.pro/wp-content/uploads/2025/03/payam-poster.png" width="300" alt="Tech Poster">](#) | [<img src="https://payam.pro/wp-content/uploads/2025/03/yaro4-poster.png" width="300" alt="Academic Poster">](#) |
|:---:|:---:|
| [<img src="https://payam.pro/wp-content/uploads/2025/03/yaro-2-poster.png" width="300" alt="Developer Poster">](#) | [<img src="https://payam.pro/wp-content/uploads/2025/03/yaro-1-poster.png" width="300" alt="Research Poster">](#) |

---

## Features

- **Smart Color Extraction**: Dominant & complementary colors automatically derived from your profile picture.
- **Custom Patterns**: Include optional background patterns with adjustable opacity and blur.

---

## Installation

1. **Requirements**  
   - Python 3.8+  
   - OpenCV  
   - NumPy  
   - rembg  
   - Matplotlib  
   - Pillow  

   Install everything from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

2. **Font Setup**  
   Place your `.ttf` font file in `/assets/` and update the `FONT_PATH` inside `text_utils.py` if you want to change the default font.

---

## Usage

### 1. Prepare Assets
- **Profile Image** (e.g., `sample-image/jane.png`).
- **Background Pattern** (optional, e.g., `background-patterns/jane-pattern-bg.png`).

### 2. Create a Profile

You can programmatically define a `Profile` object:

```python
from src.models.Profile import Profile

user = Profile(
    name="Jane",
    header="Creative Developer",
    picture="sample-image/jane.png",
    pattern_bg="background-patterns/jane-pattern-bg.png"  # Optional
)
```

### 3. Generate Poster via CLI

You can also create a banner directly from the command line using the script in `src/cli/make_banner_cli.py`:

```bash
python src/cli/make_banner_cli.py \
  "Jane" \
  "Creative Developer" \
  "sample-image/jane.png" \
  --pattern "background-patterns/jane-pattern-bg.png" \
  --popup \
  --palette
```

- `--popup` shows the final banner in a matplotlib window.
- `--palette` displays the extracted color palette in a separate matplotlib window.

### 4. View Color Palette (Optional)

If you just want to see the color palette for your image without generating a full banner, you can run:

```bash
python -m src.cli.make_banner_cli "Jane" "Developer" "sample-image/jane.png" --popup
```

---

## File Structure

A representative layout for the project is shown below. `server.py` lives inside `src/` while `assets/` (containing images, fonts, etc.) sits at the same level as `src/`. Packages are organized to separate concerns:

```
project-root/
├── assets/
│   └── ... (fonts, background images, output folders, etc.)
└── src
    ├── cli
    │   └── make_banner_cli.py
    ├── models
    │   ├── ColorPaletteGenerator.py
    │   └── Profile.py
    ├── service
    │   ├── banner_service.py
    │   └── color_palette_service.py
    ├── tests
    ├── utils
    │   ├── bg_remover.py
    │   ├── blending_modes.py
    │   ├── color_utils.py
    │   ├── color_wheel.py
    │   ├── file_utils.py
    │   ├── image_filters.py
    │   ├── masking.py
    │   ├── overlay_utils.py
    │   └── text_utils.py
    └── server.py
```

---

## Customization Tips

- **Fonts**: Update the `FONT_PATH` in `text_utils.py` to point to any `.ttf` you prefer.  
- **Color Tuning**: Adjust the complementary or saturation logic in `color_wheel.py` and `color_utils.py` to alter the final palette.  
- **Background Patterns**: Provide different patterns and tweak opacity/blur in `image_filters.py` or `banner_service.py`.  
- **Layout**: Modify banner size and text positions in `banner_service.py`, or switch up the blending functions in `blending_modes.py`.  

---

## To-Do

- **LinkedIn API Integration**: Automate uploading banners and updating profiles directly via the LinkedIn API.
- **FastAPI Deployment**: Further develop the existing `server.py` endpoints for a full REST API and simplify deployment (e.g., Docker + Uvicorn).
- **Advanced Customization**: Add more blending modes and text styling options.

