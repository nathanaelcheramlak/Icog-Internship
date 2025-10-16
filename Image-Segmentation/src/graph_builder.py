import numpy as np
from itertools import product
from typing import List, Sequence


def compute_feature_distance(pixel_a: np.ndarray, pixel_b: np.ndarray, metrics: Sequence[str], weights: Sequence[float], scale: float = 1.0) -> float:
    total_distance = 0.0
    for metric_name, metric_weight in zip(metrics, weights):
        if metric_name == "intensity":
            distance_value = abs(float(np.mean(pixel_a)) - float(np.mean(pixel_b)))
        elif metric_name == "color":
            distance_value = float(np.linalg.norm(pixel_a - pixel_b))
        else:
            raise ValueError(f"Unknown metric: {metric_name}")
        total_distance += float(metric_weight) * distance_value

    return float(scale) * total_distance


def build_graph(image: np.ndarray, metrics: Sequence[str] | None = None, weights: Sequence[float] | None = None, connectivity: int = 8, distance_scale: float = 1.0) -> np.ndarray:
    """
    Build a weighted pixel adjacency graph.

    - Nodes: each pixel index i = x * W + y
    - Edges: undirected, constructed to one-sided neighbors to avoid duplicates

    Returns a numpy array of shape (E, 3): (weight, u, v) sorted by weight asc.
    """
    if metrics is None:
        metrics = ["color"]
    if isinstance(metrics, str):
        metrics = [metrics]

    if weights is None:
        weights = [1.0] * len(metrics)
    weights = np.asarray(weights, dtype=np.float64)
    if weights.ndim != 1 or weights.size != len(metrics):
        raise ValueError("weights must match metrics length")
    sum_w = float(weights.sum())
    if sum_w <= 0:
        raise ValueError("weights must sum to positive value")
    weights = weights / sum_w

    H, W, _ = image.shape
    node_index = lambda x, y: x * W + y
    edges: List[tuple[float, int, int]] = []

    if connectivity == 4:
        directions = [(1, 0), (0, 1)]
    elif connectivity == 8:
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    else:
        raise ValueError("connectivity must be 4 or 8")

    for x, y in product(range(H), range(W)):
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < H and 0 <= ny < W:
                p1, p2 = image[x, y], image[nx, ny]
                dist = compute_feature_distance(p1, p2, metrics, weights, scale=distance_scale)
                edges.append((dist, node_index(x, y), node_index(nx, ny)))

    edges = np.array(sorted(edges, key=lambda e: e[0]), dtype=np.float64)
    return edges
