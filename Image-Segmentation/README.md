# 🧩 Graph-Based Image Segmentation (Felzenszwalb–Huttenlocher)

## Overview

This project implements the **Felzenszwalb–Huttenlocher (FH)** graph-based image segmentation algorithm **from scratch**, including a custom-built **Union-Find (Disjoint Set Union)** data structure.  
No prebuilt segmentation or clustering libraries are used — everything is implemented at the algorithmic level for clarity and experimentation.

---

## 🚀 Key Features

- ✅ **Union-Find** with path compression and union by rank
- 🧠 **Graph construction** from image pixels using 4- or 8-connectivity
- 🎨 **Distance metrics:** color (default) and intensity, with weighted combinations
- 🔍 **FH segmentation** with min-size post-processing
- 🖼️ **Flexible Image I/O:** load from local path, URL, or built-in samples (`./images`)
- 📊 **Visualization tools:**
  - Original vs. segmented overlays
  - Parameter grid comparisons
  - Individual segment highlights
- 🧩 **Command-Line Interface (CLI):**
  - Single runs
  - Parameter sweeps
  - Auto-save of segmentation overlays

---

## 🧰 Environment

- **Python:** 3.12
- **Dependencies:** see [`requirements.txt`](./requirements.txt)

---

## ⚙️ Usage

### 1️⃣ Single Run

```bash
python -m src.main run \
  --source sample --value duck.webp \
  --k 500 \
  --min_size 50 \
  --sigma 0.8 \
  --metrics color \
  --weights 1.0 \
  --connectivity 8 \
  --distance_scale 50 \
  --save images/result_overlay.png
  --distance_scale 20
```

## Source Options

| Type   | Example                          | Description                      |
| ------ | -------------------------------- | -------------------------------- |
| path   | `--value /abs/path/to/image.jpg` | Load from local path             |
| url    | `--value https://.../image.png`  | Load from web URL                |
| sample | `--value duck.webp`              | Load from `./demo_images` folder |

### 2️⃣ Parameter Grid Search

```bash
python -m src.main grid
  --source sample --value duck.webp
  --k_values 200 500 800
  --sigma_values 0.5 1.0
  --min_size_values 20 50
  --metrics color
  --weights 1.0
```

## 🧩 Notes & Tips

- **`k`** controls segmentation granularity — higher k → larger segments
- **`min_size`** enforces minimum segment size after merging
- **`sigma`** applies Gaussian smoothing before graph construction
- **`distance_scale`** adjusts pixel-difference sensitivity

### Metric Combinations

You can combine multiple metrics with custom weights:

```bash
--metrics color intensity --weights 0.7 0.3
```

## 🖼️ Segmentation Demo

Explore example segmentation outputs in the `demo_images/` folder.

**Example:** [Check Out Examples!](/demo_images/segmented/)

## 📁 Project Structure

```
src/
├── graph_builder.py # Builds weighted pixel adjacency graph
├── fh_segment.py # Core FH algorithm and labeling
├── union_find.py # Union-Find (path compression + rank)
├── utils/
│ ├── image_io.py # Load/save images from path, URL, or sample set
│ └── visualization.py # Plotting helpers and overlays
└── main.py # CLI and experiment runner
```

# 👤 Author

**Nathanael Cheramlak** (2025)
