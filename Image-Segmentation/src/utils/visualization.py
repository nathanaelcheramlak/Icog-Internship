import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


def label_to_color(labels, cmap='tab20'):
    """
    Convert label matrix into a colored image for visualization.
    """
    unique_labels = np.unique(labels)
    n_labels = len(unique_labels)
    cmap_obj = plt.get_cmap(cmap, n_labels)
    norm = colors.Normalize(vmin=0, vmax=n_labels - 1)
    color_map = cmap_obj(norm(np.arange(n_labels)))
    label_to_color_map = {l: color_map[i, :3] for i, l in enumerate(unique_labels)}

    H, W = labels.shape
    seg_image = np.zeros((H, W, 3), dtype=float)
    for l in unique_labels:
        seg_image[labels == l] = label_to_color_map[l]
    return seg_image


def visualize_segmentation(original, labels, num_segments, title=None, cmap='tab20'):
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(original)
    axes[0].set_title("Original")
    axes[0].axis("off")

    seg_viz = label_to_color(labels, cmap)
    axes[1].imshow(seg_viz)
    axes[1].set_title(f"Segmented ({num_segments} segments)")
    axes[1].axis("off")

    if title:
        fig.suptitle(title)
    plt.tight_layout()
    plt.show()


def show_parameter_comparison(image, results):
    n = len(results)
    cols = min(3, n)
    rows = int(np.ceil(n / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
    axes = np.array(axes).reshape(-1)

    for ax, res in zip(axes, results):
        seg_img = label_to_color(res["labels"])
        ax.imshow(seg_img)
        ax.set_title(
            f"k={res['k']}, σ={res['sigma']}, min={res['min_size']}\nSegments={res['num_segments']}"
        )
        ax.axis("off")

    for ax in axes[len(results):]:
        ax.axis("off")

    plt.tight_layout()
    plt.show()


def show_individual_segments(image: np.ndarray, labels: np.ndarray, max_segments: int = 16):
    """
    Visualize individual segments as masked overlays (up to max_segments).
    """
    unique_labels = np.unique(labels)
    num = min(len(unique_labels), max_segments)
    cols = min(4, num)
    rows = int(np.ceil(num / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 3.5 * rows))
    axes = np.array(axes).reshape(-1)
    for i, (ax, label) in enumerate(zip(axes, unique_labels[:num])):
        mask = labels == label
        seg = image.copy()
        seg[~mask] = 0.0
        ax.imshow(seg)
        ax.set_title(f"Segment {i} (label {int(label)})")
        ax.axis("off")
    for ax in axes[num:]:
        ax.axis("off")
    plt.tight_layout()
    plt.show()
