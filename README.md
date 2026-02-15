# 🏔️ Manifold Dynamics  
### *Physics-Driven Terrain Intelligence & Multimodal Geospatial Learning*  
**Pre-Alpha Release (2025)**

Manifold Dynamics is an open research framework for **terrain physics**,  
**geomorphometry**, **C++ accelerated computation**, and **multimodal  
terrain–language models** (TopoCLIP).

This pre-alpha drop includes:
- A **7-channel ManifoldTensor (.mft)** data format  
- A complete **DEM → MFT ingest system**  
- **KESM-Lite** cold-air drainage physics  
- **TopoCLIP** multimodal terrain/text training pipeline  
- **Visualization + diagnostics tools**  
- **C++ backend bindings**  
- **LaTeX manuals & documentation**  

This is an **early, experimental research release** — expect rapid changes.

---

# ⚠️ Pre-Alpha Status

Manifold Dynamics is currently in early experimental development.

Please read:  
👉 [`PRE_ALPHA_NOTICE.md`](PRE_ALPHA_NOTICE.md)  
👉 [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md)

---

# 📦 Features

### ✔ Physics & Geomorphometry
- Surface normals (smoothed gradients)
- PCA eigen-roughness (λ₃)
- Topographic Position Index (TPI)
- Vector Ruggedness Measure (VRM)
- Laplacian terrain stability (KESM-Lite)

### ✔ Multimodal Learning (TopoCLIP)
- 7-channel terrain encoder
- DistilBERT text encoder
- Symmetric InfoNCE contrastive loss
- Patch sampling + embedding tools

### ✔ C++ Backend
- High-performance kernels
- pybind11 Python bindings
- Optional prebuilt `.pyd` for Windows

### ✔ Tools
- `viewer.py` — Napari multi-channel viewer  
- `vis.py` — quick heatmaps  
- `diagnose.py` — cross-sections, QA  
- Full ingest & processing CLI

---

# 📐 System Architecture

```
Raw DEM (GeoTIFF/ADF)
        ↓
   manifold-ingest
        ↓
 ManifoldTensor (.mft)
   7 float32 channels
        ↓
   Physics Engine
     (KESM-Lite)
        ↓
 Multimodal Engine
     (TopoCLIP)
        ↓
Visualization / QA
```

---

# 🧠 Mathematical Foundations (Short Version)

### Structure Tensor Roughness
\[
R = \sqrt{|\lambda_3|}
\]

### Normals
\[
\mathbf{n} =
\frac{1}{\sqrt{1+z_x^2+z_y^2}}
\begin{bmatrix}
-z_x \\ z_y \\ 1
\end{bmatrix}
\]

### Laplacian Stability (KESM)
\[
S = \frac{\nabla^2 z}{\mathrm{GSD}^2}
\]

Full math:  
👉 `docs/techdocs/`  
👉 `FULL_MANUAL.tex`

---

# 🚀 Quick Start

### Install Requirements
```bash
# Install the package in editable mode
pip install -e .

# To install test dependencies
pip install -e .[test]
```

### Ingest a DEM → `.mft`
You can use the CLI command:
```bash
manifold-ingest raw/smokies.tif data/processed/smokies.mft
```
Or use Python:
```python
from manifold.core.ingest import ingest_geotiff
tensor = ingest_geotiff("raw/smokies.tif", "data/processed/smokies.mft")
```

### Run Physics (KESM-Lite)
```bash
python -m manifold.physics.kesm data/processed/smokies.mft
```
Or via Python API:
```python
from manifold.physics.kesm import KESM_Lite
from manifold.core.io import ManifoldTensor

t = ManifoldTensor.load("data/processed/smokies.mft")
solver = KESM_Lite(t)
stability = solver.compute_stability_index()
```

### Train TopoCLIP
```bash
python -m manifold.vision.topo_clip_train data/processed/smokies.mft --epochs 5
```
Or via Python API:
```python
from manifold.vision.topo_clip_train import train_topo_clip
train_topo_clip("data/processed/smokies.mft", epochs=5)
```

### Run Tests
```bash
pytest tests/
```

---

# 🗂️ Repository Structure

See full explanation:  
👉 [`docs/structure.md`](docs/structure.md)

```
manifold-dynamics/
├── src/
│   └── manifold/        # Core Python library
│       ├── core/        # IO, Ingest, Geometry
│       ├── physics/     # KESM + physical models
│       └── vision/      # TopoCLIP + multimodal models
├── tests/               # Test suite
├── data/                # Raw + processed terrain
├── docs/                # Manuals, LaTeX, notebooks
└── pyproject.toml       # Project configuration
```

---

# 📚 Documentation

### User Guides
- [`QUICK_START.md`](QUICK_START.md)  
- [`HOW_TO_BUILD.md`](HOW_TO_BUILD.md)

### Manuals
- `FULL_MANUAL.tex`
- Additional LaTeX docs in `docs/techdocs/`

### Internal Status
- [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md)  
- [`PRE_ALPHA_NOTICE.md`](PRE_ALPHA_NOTICE.md)

---

# 🤝 Contributing

We welcome early feedback and experimental contributions.  
Please read:  
👉 [`CONTRIBUTING.md`](CONTRIBUTING.md)

---

# 🔓 License

**Apache 2.0 / MIT** (See [`LICENSE`](LICENSE))

---

# 🛰️ Project Vision

Manifold Dynamics aims to unify:
- terrain geometry  
- environmental physics  
- AI-based semantic understanding  
into a single, modular, research-grade system.

This is only the beginning — expect:  
- GPU-accelerated ingest  
- ViT/Swin-based encoders  
- Zero-shot semantic terrain labeling  
- Fully validated physics  
- Scientific paper (Spring 2025)  

---

# ⭐ Acknowledgements

Thanks to early testers, researchers, and geospatial communities providing  
open DEMs and terrain datasets.
