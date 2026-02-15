# 📁 Manifold Dynamics — Repository Structure (Pre-Alpha)

This document describes the structure of the Manifold Dynamics repository.

---

# 1. Top-Level Layout

```
manifold-dynamics/
│
├── src/                # Source code
│   └── manifold/       # Core Python package
│       ├── core/       # IO, Ingest, Geometry
│       ├── physics/    # KESM and related physical modeling
│       └── vision/     # TopoCLIP + multimodal models
│
├── cpp/                # C++ backend, solvers, bindings, CMake project
│
├── tests/              # Test suite (pytest)
│
├── data/
│   ├── raw/            # Source DEMs, ADF/GRID files
│   ├── processed/      # .mft ManifoldTensor outputs
│   └── ...
│
├── docs/               # Documentation
│
├── pyproject.toml      # Project configuration and dependencies
├── README.md           # Project introduction
├── QUICK_START.md      # Setup and minimal usage guide
└── ...
```

---

# 2. Directory Breakdown

## 📦 `src/manifold/`
The main Python package.

### `core/`
- `ingest.py`: Full DEM → MFT pipeline.
- `io.py`: ManifoldTensor (.mft) loading/writing.
- `diagnose.py`: Terrain QA + diagnostic cross-sections.
- `viewer.py`: Napari visualization.
- `vis.py`: Simple Matplotlib visualizer.

### `physics/`
- `kesm.py`: KESM-Lite terrain stability modeling.

### `vision/`
- `topo_clip_train.py`: TopoCLIP training loop.
- `topo_clip_encoder.py`: TopoCLIP model architecture.
- `topo_clip_data.py`: Dataset loader.

---

## ⚙️ `cpp/`  
The C++ backend providing:
- High-performance kernels  
- pybind11 Python bindings  
- CMake build scripts

---

## 🧪 `tests/`
Contains `pytest` tests for:
- `test_io.py`: ManifoldTensor verification.
- `test_ingest.py`: Ingest pipeline logic.
- `test_kesm.py`: Physics model verification.
- `test_vision.py`: TopoCLIP architecture checks.

---
