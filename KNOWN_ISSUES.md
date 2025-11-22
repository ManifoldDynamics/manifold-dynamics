# ⚠️ Manifold Dynamics — Known Issues (Pre-Alpha)

This document lists all currently known issues, limitations, and incomplete
systems in the Manifold Dynamics pre-alpha release. These will be resolved or
restructured during the Alpha milestone.

---

## 🧱 Repository Structure & Artifacts

### • Build artifacts included
Several compiled or auto-generated files remain in the repository, including:

- Windows / Visual Studio build folders (`x64/`, `Release/`)
- CMake-generated files
- `.pyd` Python extension binaries
- `.vcxproj` and `.filters` files
- Temporary `.dir` folders

**Reason:** These are included intentionally to allow early testing of the C++
backend without requiring users to compile locally.

---

## 📁 Layout is not final

The current directory structure reflects the internal development environment.
Notably:

- `view/` contains PyInstaller-style output and should eventually be removed.
- `data/` contains raw, processed, and intermediate datasets in one folder.
- C++ and Python code co-exist without a unified build or packaging system.
- Some modules are duplicated or partially overlapping in purpose.

A full restructuring will happen before Alpha.

---

## 🧪 Incomplete / Experimental Modules

### • **KESM-Lite physics model**
- Current drainage computation is a simplified Laplacian proxy.
- Parameters require tuning across DEM resolutions.
- Terrain classification thresholds are approximate.

### • **TopoCLIP multimodal model**
- Uses a placeholder text dataset.
- Embeddings are untrained or minimally trained.
- Loss temperatures and augmentations need refinement.
- No pretrained weights are provided yet.

### • **Terrain ingest pipeline**
- Destriping, void fill, and normalization are still being improved.
- Some edge-case DEMs produce artifacts.
- MFT header format is not yet versioned.

### • **Visualization tools**
- Napari viewer lacks multi-channel composite modes.
- `vis.py` is a minimal diagnostic tool and not production-ready.

---

## 🧮 Mathematical Limitations

- Roughness (λ₃) depends strongly on DEM noise; smoothing parameters vary by dataset.
- VRM, normals, and gradients may require additional filtering to generalize.
- No fully validated physical units for some derived metrics.
- Cold-air pooling model does not incorporate wind, vegetation, or radiative balance.

---

## 🧰 C++ Backend Issues

- Some `.cpp` files are stubs or partially implemented.
- CMake config is incomplete on Linux/macOS.
- Python bindings are Windows-only at the moment.
- Missing unit tests for backend solvers.

---

## 📦 Packaging and Installation Issues

- No `pyproject.toml` or pip install flow yet.
- Imports rely on local relative paths.
- No virtual environment isolation recommendations.
- Backend compilation is not automated.

---

## 🔍 Testing & Benchmarking

Current state:

- No formal test suite.
- `tests/` directory is empty or minimal.
- No regression tests for physics or ingest.
- Performance benchmarks not implemented.

---

## 🗺️ Dataset Issues

- `data/` includes internal and example datasets mixed together.
- Some ADF/GRID formats require proprietary ESRI tools.
- DEMs differ in resolution and projection; ingest normalizes them imperfectly.

---

## 📖 Documentation Gaps

- Outdated or incomplete LaTeX manuscripts.
- Missing API documentation.
- No usage examples for advanced physics.
- No full tutorial for training TopoCLIP end-to-end.

---

## 🧷 Miscellaneous

- Some Python files contain unused imports or experimental functions.
- Paths are partially hard-coded in scripts.
- Windows-specific assumptions in some modules.
- No GPU acceleration yet.

---

## ✔ Planned Fixes Before Alpha

- Cleaned repository layout (no binaries, no build folders)
- Fully versioned ManifoldTensor format
- Robust ingest + physics validation suite
- Proper dataset loaders and metadata
- Complete TopoCLIP dataset + pretrained weights
- Unified Python + C++ packaging
- Public documentation website

---

If you discover new issues, please open an Issue on GitHub with:
- Steps to reproduce  
- System information  
- Dataset used  
- Screenshots if relevant  

Thank you for helping improve Manifold Dynamics.
