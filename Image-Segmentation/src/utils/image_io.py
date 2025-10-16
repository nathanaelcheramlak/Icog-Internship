import os
from pathlib import Path
from typing import Optional, Literal

import numpy as np
from skimage import io, img_as_float
from skimage.color import rgba2rgb
from skimage.transform import resize as sk_resize
from scipy.ndimage import gaussian_filter

SourceType = Literal["path", "url", "sample"]


def _ensure_rgb_float(image: np.ndarray) -> np.ndarray:
    """
    Convert image to float in [0,1] and ensure 3 channels (RGB).
    """
    img = img_as_float(image)
    if img.ndim == 2:
        # grayscale -> RGB
        img = np.stack([img, img, img], axis=-1)
    if img.shape[-1] == 4:
        img = rgba2rgb(img)
    return img


def load_image(
    source: SourceType,
    value: str,
    resize_to: Optional[tuple[int, int]] = None,
    sigma: Optional[float] = None,
) -> np.ndarray:
    """
    Load an image as float RGB from a local path, URL, or sample name.
    Optionally apply Gaussian blur.

    Args:
        source: one of {"path", "url", "sample"}
        value: path on disk, URL string, or sample file under ./images
        resize_to: optional (width, height)
        sigma: optional Gaussian blur strength (e.g., 0.5–1.0)
    Returns:
        np.ndarray (H, W, 3), float in [0,1]
    """
    if source == "path":
        if not os.path.exists(value):
            raise FileNotFoundError(f"Image not found: {value}")
        img = io.imread(value)
    elif source == "url":
        img = io.imread(value)
    elif source == "sample":
        sample_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "demo_images", value
        )
        if not os.path.exists(sample_path):
            raise FileNotFoundError(f"Sample not found: {sample_path}")
        img = io.imread(sample_path)
    else:
        raise ValueError("source must be one of 'path' | 'url' | 'sample'")

    # Ensure RGB in float
    img = _ensure_rgb_float(img)

    # Resize if needed
    if resize_to is not None:
        w, h = resize_to
        img = sk_resize(img, (h, w), anti_aliasing=True, preserve_range=True)

    # Gaussian Blur
    # if sigma is not None and sigma > 0:
    #     img = gaussian_filter(img, sigma=(sigma, sigma, 0))  # blur only spatially

    return img


def save_image(image: np.ndarray, path: str):
    """
    Save an RGB or grayscale image safely to disk.
    Converts to uint8 to avoid Pillow float64 issues.
    """
    dirpath = os.path.dirname(path)
    if dirpath:
        Path(dirpath).mkdir(parents=True, exist_ok=True)
    img = np.clip(image, 0, 1)
    img_uint8 = (img * 255.0).round().astype(np.uint8)
    io.imsave(path, img_uint8)


def save_overlay(image: np.ndarray, labels: np.ndarray, path: str, alpha=0.5):
    from .visualization import label_to_color
    colors = label_to_color(labels)
    overlay = np.clip((1 - alpha) * image + alpha * colors, 0, 1)
    save_image(overlay, path)
