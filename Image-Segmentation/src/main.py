import argparse
from itertools import product
from typing import Sequence

import numpy as np
from skimage.filters import gaussian

from .graph_builder import build_graph
from .fh_segment import felzenszwalb_segment
from .utils.image_io import load_image, save_overlay
from .utils.visualization import visualize_segmentation, show_parameter_comparison, show_individual_segments


def run_segmentation(
    *,
    source: str,
    value: str,
    metrics: Sequence[str] = ("color",),
    weights: Sequence[float] = (1.0,),
    connectivity: int = 8,
    sigma: float = 0.8,
    k: float = 500.0,
    min_size: int = 20,
    uf=None,
    show: bool = True,
    save_path: str | None = None,
    resize_to: tuple[int, int] | None = None,
):
    """
    Load, preprocess, build graph, run FH segmentation, and visualize.
    """
    # Load image from path/url/sample
    img = load_image(source, value, resize_to=resize_to)

    if sigma and sigma > 0:
        img = gaussian(img, sigma=sigma, channel_axis=-1)

    H, W, _ = img.shape
    num_nodes = H * W

    # Build graph
    print("Building graph...")
    edges = build_graph(img, metrics=metrics, weights=weights, connectivity=connectivity)

    # Segment
    print(f"Running FH segmentation with k={k}, min_size={min_size}, sigma={sigma}, metrics={metrics}...")
    labels, num_segments, _ = felzenszwalb_segment(
        edges, num_nodes, k=k, min_size=min_size, uf=uf, image_shape=(H, W)
    )

    print(f"Segmentation complete: {num_segments} segments.")

    if show:
        visualize_segmentation(img, labels, num_segments, title=f"k={k}, σ={sigma}, min={min_size}")
        show_individual_segments(img, labels)
    if save_path:
        save_overlay(img, labels, save_path)

    return labels, num_segments


def run_parameter_experiments(
    *,
    source: str,
    value: str,
    k_values: Sequence[float] = (200, 500, 800),
    sigma_values: Sequence[float] = (0.5, 1.0),
    min_size_values: Sequence[int] = (20, 50),
    metrics: Sequence[str] = ("color",),
    weights: Sequence[float] = (1.0,),
    connectivity: int = 8,
    uf=None,
    show_grid: bool = True,
    resize_to: tuple[int, int] | None = None,
):
    """
    Runs multiple parameter combinations and visualizes comparisons.
    """
    results = []

    for k, sigma, min_size in product(k_values, sigma_values, min_size_values):
        labels, num_segments = run_segmentation(
            source=source,
            value=value,
            metrics=metrics,
            weights=weights,
            connectivity=connectivity,
            sigma=sigma,
            k=k,
            min_size=min_size,
            uf=uf,
            show=False,
            resize_to=resize_to,
        )
        results.append({
            "k": k,
            "sigma": sigma,
            "min_size": min_size,
            "labels": labels,
            "num_segments": num_segments,
        })

    if show_grid:
        img = load_image(source, value, resize_to=resize_to)
        show_parameter_comparison(img, results)


def build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FH Graph-based Image Segmentation")
    sub = parser.add_subparsers(dest="command", required=True)

    # Single run
    run = sub.add_parser("run", help="Run segmentation on a single input")
    run.add_argument("--source", choices=["path", "url", "sample"], default="path")
    run.add_argument("--value", required=True, help="Path/URL/sample filename")
    run.add_argument("--k", type=float, default=500.0)
    run.add_argument("--min_size", type=int, default=20)
    run.add_argument("--sigma", type=float, default=0.8)
    run.add_argument("--connectivity", type=int, choices=[4, 8], default=8)
    run.add_argument("--metrics", nargs="*", default=["color"], help="Metrics like color intensity")
    run.add_argument("--weights", nargs="*", type=float, default=[1.0], help="Weights per metric")
    run.add_argument("--save", default=None, help="Path to save overlay image")
    run.add_argument("--no-show", action="store_true", help="Disable visualization windows")
    run.add_argument("--resize", nargs=2, type=int, metavar=("W", "H"), help="Resize to width height for speed")

    # Experiments grid
    exp = sub.add_parser("grid", help="Run parameter grid and show comparison grid")
    exp.add_argument("--source", choices=["path", "url", "sample"], default="path")
    exp.add_argument("--value", required=True)
    exp.add_argument("--k_values", nargs="*", type=float, default=[200, 500, 800])
    exp.add_argument("--sigma_values", nargs="*", type=float, default=[0.5, 1.0])
    exp.add_argument("--min_size_values", nargs="*", type=int, default=[20, 50])
    exp.add_argument("--connectivity", type=int, choices=[4, 8], default=8)
    exp.add_argument("--metrics", nargs="*", default=["color"])
    exp.add_argument("--weights", nargs="*", type=float, default=[1.0])
    exp.add_argument("--resize", nargs=2, type=int, metavar=("W", "H"))
    return parser


def main():
    parser = build_cli_parser()
    args = parser.parse_args()
    if args.command == "run":
        labels, n = run_segmentation(
            source=args.source,
            value=args.value,
            metrics=args.metrics,
            weights=args.weights,
            connectivity=args.connectivity,
            sigma=args.sigma,
            k=args.k,
            min_size=args.min_size,
            show=(not args.no_show),
            save_path=args.save,
            resize_to=tuple(args.resize) if args.resize else None,
        )
        print(f"Segments: {n}")
    elif args.command == "grid":
        run_parameter_experiments(
            source=args.source,
            value=args.value,
            k_values=args.k_values,
            sigma_values=args.sigma_values,
            min_size_values=args.min_size_values,
            metrics=args.metrics,
            weights=args.weights,
            connectivity=args.connectivity,
            resize_to=tuple(args.resize) if args.resize else None,
        )


if __name__ == "__main__":
    main()
