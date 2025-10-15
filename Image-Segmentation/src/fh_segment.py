"""
Felzenszwalb-Huttenlocher (FH) Segmentation Algorithm.
Based on:
Felzenszwalb, P. F., & Huttenlocher, D. P. (2004).
Efficient graph-based image segmentation. IJCV, 59(2), 167–181.
"""

from typing import Optional, Tuple, Iterable, Sequence
import numpy as np
from .union_find import UnionFind


def _validate_and_prepare_edges(edges: Iterable[Sequence]) -> np.ndarray:
    """
    Validates and converts edges to np.ndarray with dtype [float64, int64, int64].
    Expects edges already sorted by weight.
    """
    edges_arr = np.asarray(edges)
    if edges_arr.size == 0:
        return np.zeros((0, 3), dtype=np.float64)

    if edges_arr.ndim != 2 or edges_arr.shape[1] != 3:
        raise ValueError("edges must be iterable of (weight, node_u, node_v) tuples")

    weights = edges_arr[:, 0].astype(np.float64)
    u = edges_arr[:, 1].astype(np.int64)
    v = edges_arr[:, 2].astype(np.int64)
    return np.column_stack((weights, u, v))


def felzenszwalb_segment(
    edges: Iterable[Sequence],
    num_nodes: int,
    *,
    k: float = 500.0,
    min_size: int = 20,
    uf=None,
    image_shape: Optional[Tuple[int, int]] = None,
):
    """
    Run Felzenszwalb-Huttenlocher segmentation.

    Parameters
    ----------
    edges : iterable of (weight, u, v)
        Weighted edges between pixel nodes. Must be sorted by ascending weight.
    num_nodes : int
        Number of nodes (typically H * W).
    k : float
        Scale parameter (larger k => larger regions).
    min_size : int
        Minimum allowed component size.
    uf : optional
        External Union-Find instance. If None, an internal UF is used.
    image_shape : optional (H, W)
        If provided, labels are reshaped accordingly.

    Returns
    -------
    labels : np.ndarray
        (num_nodes,) or (H, W) array of segment labels.
    num_segments : int
        Number of final segments.
    uf_instance : UnionFind
        The internal UF object (for inspection).
    """
    if num_nodes <= 0:
        raise ValueError("num_nodes must be positive")
    if k <= 0:
        raise ValueError("k must be positive")
    if min_size < 1:
        raise ValueError("min_size must be >= 1")

    edges_arr = _validate_and_prepare_edges(edges)
    ufw = uf or UnionFind(num_nodes)

    internal_diff = np.zeros(num_nodes, dtype=np.float64)

    # --- Main FH merging loop ---
    for w_f, u_f, v_f in edges_arr:
        w = float(w_f)
        u = int(u_f)
        v = int(v_f)

        ru = ufw.find(u)
        rv = ufw.find(v)
        if ru == rv:
            continue

        size_ru = ufw.component_size(ru)
        size_rv = ufw.component_size(rv)

        thr_ru = internal_diff[ru] + (k / size_ru)
        thr_rv = internal_diff[rv] + (k / size_rv)

        if w <= min(thr_ru, thr_rv):
            new_root = ufw.union(ru, rv)
            internal_diff[new_root] = max(internal_diff[ru], internal_diff[rv], w)

    # --- Post-processing: merge small regions ---
    for w_f, u_f, v_f in edges_arr:
        w = float(w_f)
        u = int(u_f)
        v = int(v_f)

        ru = ufw.find(u)
        rv = ufw.find(v)
        if ru == rv:
            continue

        if ufw.component_size(ru) < min_size or ufw.component_size(rv) < min_size:
            new_root = ufw.union(ru, rv)
            internal_diff[new_root] = max(internal_diff[ru], internal_diff[rv], w)

    # --- Relabel components ---
    roots = [ufw.find(i) for i in range(num_nodes)]
    unique_roots, inverse_idx = np.unique(np.array(roots, dtype=np.int64), return_inverse=True)
    labels_1d = inverse_idx.astype(np.int32)
    num_segments = len(unique_roots)

    if image_shape:
        H, W = image_shape
        if H * W != num_nodes:
            raise ValueError("image_shape does not match num_nodes")
        labels = labels_1d.reshape((H, W))
    else:
        labels = labels_1d

    return labels, num_segments, ufw
