import cv2
import numpy as np

def blend_normal(bg, fg, alpha_fg):
    """Applies normal alpha blending."""
    alpha_bg = 1.0 - alpha_fg
    for c in range(3):
        bg[:, :, c] = fg[:, :, c] * alpha_fg + bg[:, :, c] * alpha_bg
    return bg

def blend_multiply(bg, fg, alpha_fg):
    """Applies multiply blending (darken effect)."""
    for c in range(3):
        bg[:, :, c] = (bg[:, :, c] * fg[:, :, c]) / 255.0
    return bg

def blend_add(bg, fg, alpha_fg):
    """Applies additive blending (bright effect)."""
    for c in range(3):
        bg[:, :, c] = cv2.add(bg[:, :, c], fg[:, :, c])
    return bg

def blend_overlay(bg, fg, alpha_fg):
    """Applies overlay blending (contrast effect)."""
    for c in range(3):
        bg[:, :, c] = np.where(bg[:, :, c] < 128,
                               (2 * bg[:, :, c] * fg[:, :, c]) / 255.0,
                               255 - (2 * (255 - bg[:, :, c]) * (255 - fg[:, :, c])) / 255.0)
    return bg
