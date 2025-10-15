Graph-Based Image Segmentation (Felzenszwalb–Huttenlocher)

Overview
This project implements the Felzenszwalb–Huttenlocher (FH) graph-based image segmentation algorithm from scratch, including a Union-Find (Disjoint Set Union). No prebuilt segmentation/clustering libraries are used.

Key Features

- Union-Find (path compression + union by rank) implemented
- Graph construction from image pixels with 4/8-connectivity
- Distance metrics: color (default) and intensity, with weighted combinations
- FH segmentation with min-size post-processing
- Image I/O via local path, URL, or sample images in ./images
- Visualizations: original vs segmented, parameter grid, and individual segment views
- CLI for single runs and parameter sweeps; saves overlay outputs

Environment

- Python 3.12
- See requirements.txt for dependencies

Usage

1. Single run
   python -m src.main run --source sample --value duck.webp --k 500 --min_size 50 --sigma 0.8 --metrics color --weights 1.0 --connectivity 8 --save images/result_overlay.png

Sources

- --source path --value /abs/path/to/image.jpg
- --source url --value https://.../image.png
- --source sample --value duck.webp (reads from ./images)

2. Parameter grid
   python -m src.main grid --source sample --value duck.webp --k_values 200 500 800 --sigma_values 0.5 1.0 --min_size_values 20 50 --metrics color --weights 1.0

Notes

- Larger k produces larger segments; min_size enforces minimum component sizes after the main pass.
- You can mix metrics (e.g., --metrics color intensity --weights 0.7 0.3).

Project Structure

- src/graph_builder.py: Build weighted pixel adjacency graph
- src/fh_segment.py: FH algorithm core and labeling
- src/union_find.py: Union-Find (path compression + union by rank)
- src/utils/image_io.py: Image loading (path/url/sample) and saving
- src/utils/visualization.py: Plotting helpers and segment visualizations
- src/main.py: CLI and experiment harness

Author
Nathanael Cheramlak @ 2025