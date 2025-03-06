Here is the **detailed documentation** for your **poster generation script**. It includes:  

- **Overview of the script**  
- **Pipeline explanation**  
- **Detailed documentation for each method** (input types, return types, and explanations)  

---

### **🚀 Poster Generation Script Documentation**

## **📌 Overview**
This script generates a **custom poster** using an **input image**, removing the background and applying visual effects.  
It follows a **pipeline of methods** to extract colors, create a gradient background, add text, overlay the subject, and blend in a transparent fade effect.

---

## **📌 Pipeline Explanation**
The script follows these steps:  

1️⃣ **Extract Colors** – Detects **background and text colors** from the image.  
2️⃣ **Create Gradient Background** – Generates a **horizontal color gradient** using sampled colors.  
3️⃣ **Add Text** – Places the **"#Open to Work"** text in the center.  
4️⃣ **Remove Background** – Removes the **subject's background** using `rembg`.  
5️⃣ **Overlay Subject** – Places the **subject on the background**, maintaining **aspect ratio**.  
6️⃣ **Create Transparent Gradient** – Generates a **fade effect** from color to transparent.  
7️⃣ **Blend Transparency** – Overlays the **fade effect** on the final poster.  
8️⃣ **Save with Unique Filename** – Ensures **no file overwriting** by adding numbers.  

---

## **📌 Detailed Method Documentation**
Each function in the script performs a specific task in the **poster generation pipeline**.

---

### **🔹 `extract_colors(image_path: str) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]`**
Extracts **two background colors** and **one contrasting text color** from an image.

#### **📥 Parameters**  
- `image_path` *(str)* – Path to the image file.

#### **📤 Returns**  
- `left_bg_color` *(tuple[int, int, int])* – RGB color sampled from the **left edge**.  
- `right_bg_color` *(tuple[int, int, int])* – RGB color sampled from the **right edge**.  
- `text_color` *(tuple[int, int, int])* – A **contrasting color** chosen for text.

#### **🔹 How It Works**  
- Uses **OpenCV (`cv2`)** to read the image.  
- Samples the **left and right edges** for background colors.  
- Picks a **contrasting color** from random pixels for the text.

---

### **🔹 `create_gradient_rectangle(color1: tuple[int, int, int], color2: tuple[int, int, int], width: int = 1920, height: int = 1080) -> np.ndarray`**
Generates a **horizontal gradient background** using two colors.

#### **📥 Parameters**  
- `color1` *(tuple[int, int, int])* – Left-side background color (RGB).  
- `color2` *(tuple[int, int, int])* – Right-side background color (RGB).  
- `width` *(int, optional)* – Width of the gradient (default: `1920`).  
- `height` *(int, optional)* – Height of the gradient (default: `1080`).  

#### **📤 Returns**  
- `gradient` *(np.ndarray)* – The **generated gradient image**.

#### **🔹 How It Works**  
- Creates an **empty image**.  
- Gradually blends **color1 → color2** across the width.

---

### **🔹 `add_text(image: np.ndarray, text: str, color: tuple[int, int, int], font_scale: float = 4, thickness: int = 6) -> np.ndarray`**
Adds **text overlay** onto an image.

#### **📥 Parameters**  
- `image` *(np.ndarray)* – Image to add text to.  
- `text` *(str)* – The text string to overlay (default: `"#Open to Work"`).  
- `color` *(tuple[int, int, int])* – RGB color of the text.  
- `font_scale` *(float, optional)* – Size of the text (default: `4`).  
- `thickness` *(int, optional)* – Stroke thickness (default: `6`).  

#### **📤 Returns**  
- `image_with_text` *(np.ndarray)* – The image with text applied.

#### **🔹 How It Works**  
- Uses **OpenCV (`cv2.putText`)** to add **centered text** at the bottom.

---

### **🔹 `remove_background_fast(image_path: str, target_size: tuple[int, int] = (500, 500)) -> np.ndarray`**
Removes the **background** from an image using `rembg`.

#### **📥 Parameters**  
- `image_path` *(str)* – Path to the image file.  
- `target_size` *(tuple[int, int], optional)* – Resizes image for **faster processing** (default: `(500, 500)`).  

#### **📤 Returns**  
- `output` *(np.ndarray)* – The **image with transparent background**.

#### **🔹 How It Works**  
- Uses `cv2` to **resize** the image for faster processing.  
- Uses **rembg** to remove the background.  
- Resizes the image **back to original dimensions**.

---

### **🔹 `overlay_image(bg: np.ndarray, fg: np.ndarray) -> np.ndarray`**
Overlays the **cutout subject** onto the background while maintaining **aspect ratio**.

#### **📥 Parameters**  
- `bg` *(np.ndarray)* – The **background image**.  
- `fg` *(np.ndarray)* – The **foreground (cutout subject) image**.  

#### **📤 Returns**  
- `output` *(np.ndarray)* – The **composite image**.

#### **🔹 How It Works**  
- Maintains **subject aspect ratio**.  
- Places the subject **in the center**.  
- Uses **alpha blending** for **smooth edges**.

---

### **🔹 `create_fade_to_transparent(color: tuple[int, int, int], width: int = 1920, height: int = 1080, fade_strength: float = 0.7) -> np.ndarray`**
Creates a **vertical gradient** that fades from a **solid color** to **transparent**.

#### **📥 Parameters**  
- `color` *(tuple[int, int, int])* – Base color for the fade.  
- `width` *(int, optional)* – Width of the image (default: `1920`).  
- `height` *(int, optional)* – Height of the image (default: `1080`).  
- `fade_strength` *(float, optional)* – How much of the height should fade (default: `0.7`).  

#### **📤 Returns**  
- `gradient` *(np.ndarray)* – The **generated transparent fade**.

#### **🔹 How It Works**  
- Creates an **RGBA gradient image**.  
- Sets **alpha values** to gradually fade out.

---

### **🔹 `overlay_transparent(bg: np.ndarray, fg: np.ndarray) -> np.ndarray`**
Blends a **transparent image** onto another image.

#### **📥 Parameters**  
- `bg` *(np.ndarray)* – Background image.  
- `fg` *(np.ndarray)* – Transparent overlay image.  

#### **📤 Returns**  
- `output` *(np.ndarray)* – The **final blended image**.

#### **🔹 How It Works**  
- Uses **alpha blending** to overlay the **fade effect** on the final poster.

---

### **🔹 `get_unique_filename(base_path: str, filename: str) -> str`**
Generates a **unique filename** if a file already exists.

#### **📥 Parameters**  
- `base_path` *(str)* – Directory where the file is saved.  
- `filename` *(str)* – Desired filename.  

#### **📤 Returns**  
- `unique_filename` *(str)* – A **new filename** with a number if needed.

---

### **🔹 `generate_poster(image_path: str) -> str`**
**Main function** that executes the full **poster generation pipeline**.

#### **📥 Parameters**  
- `image_path` *(str)* – Path to the input image.  

#### **📤 Returns**  
- `output_path` *(str)* – Path to the saved poster.

