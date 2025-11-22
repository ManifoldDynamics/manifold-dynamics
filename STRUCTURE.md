# 📁 Manifold Dynamics — Repository Structure (Pre-Alpha)

This document describes the structure of the Manifold Dynamics repository in its
current **pre-alpha** state. The layout reflects an active research environment
with multiple evolving components (Python, C++, data processing, physics
models, multimodal learning, and documentation). A full cleanup and packaging
pass will occur during the Alpha release.

---

# 1. Top-Level Layout

```
manifold-dynamics/
│
├── manifold/           # Core Python library (geometry, IO, physics helpers)
├── vision/             # TopoCLIP + multimodal models
├── physics/            # KESM and related physical modeling
├── cpp/                # C++ backend, solvers, bindings, CMake project
│
├── ingest.py           # DEM → ManifoldTensor converter pipeline
├── kesm.py             # Physics entrypoint (Python reference model)
├── diagnose.py         # Terrain QA + diagnostic cross-sections
├── viewer.py           # Napari visualization
├── vis.py              # Simple Matplotlib visualizer
│
├── tests/              # (Pre-alpha) test stubs
│
├── data/
│   ├── raw/            # Source DEMs, ADF/GRID files, external data
│   ├── processed/      # .mft ManifoldTensor outputs
│   ├── biomes/         # Sample biome metadata and region examples
│   └── ...             # May contain mixed intermediate datasets
│
├── docs/               # Papers, LaTeX tech docs, manuals, notebook prototypes
│   ├── techdocs/       # In-depth mathematical + system documentation
│   └── notebooks/      # Jupyter notebooks for experiments
│
├── view/               # Build artifacts (PyInstaller / CLI viewer output)
│
├── x64/                # Visual Studio auto-generated build output (Windows)
├── Release/            # Windows C++ build output (.pyd, .exe)
│
├── CMakeLists.txt      # C++ build configuration
├── README.md           # Project introduction
├── QUICK_START.md      # Setup and minimal usage guide
├── FULL_MANUAL.tex     # Full technical manual (LaTeX)
├── PRE_ALPHA_NOTICE.md # Development disclaimer
├── KNOWN_ISSUES.md     # Open issues in the pre-alpha
├── HOW_TO_BUILD.md     # Build + installation instructions
└── LICENSE.md          # MIT license
```

---

# 2. Directory Breakdown

## 📦 `manifold/`  
Core Python modules implementing:

- ManifoldTensor loading/writing  
- Normal computation  
- Structure tensor roughness  
- TPI and VRM  
- Small geometry utilities  
- Map projection helpers  
- Backend loader (when `.pyd` is present)

This is the “core” library referenced by physics and vision modules.

---

## 🔬 `physics/`
Contains the *reference Python physics models*, including:

- KESM-Lite (Laplacian terrain stability proxy)  
- Gradient & curvature helpers  
- Physical classification pipelines  
- Experimental physical models under development  

---

## 🤖 `vision/`
Contains the **TopoCLIP multimodal stack**:

- Terrain encoder  
- DistilBERT text encoder  
- Dataset sampling (256×256 patches)  
- Contrastive InfoNCE loss  
- Training loop  
- Embedding utilities  

This is where semantic modeling and representation learning live.

---

## ⚙️ `cpp/`  
The C++ backend providing:

- High-performance kernels  
- Potential future GPU acceleration  
- pybind11 Python bindings  
- Visual Studio + CMake build scripts  

Current artifacts (prebuilt `.pyd`) are also present for convenience.

---

## 🗂 `data/`
Not intended for production storage yet, but includes:

- `raw/` — input DEMs, often ADF/GRID or GeoTIFF  
- `processed/` — `.mft` tensors created by `ingest.py`  
- `biomes/` — experimental biome metadata and small example files  
- Intermediate data from development experiments  

This folder will be restructured in Alpha.

---

## 🧰 Top-level Python tools

### `ingest.py`
Full DEM → MFT pipeline:
- void fill  
- destriping  
- gradient smoothing  
- normals  
- PCA roughness  
- TPI / VRM  
- saves `.mft`

### `kesm.py`
Runs KESM-Lite terrain stability modeling.

### `diagnose.py`
Cross-sections, debug plots, QA checks.

### `viewer.py`
Napari-based multi-channel viewer.

### `vis.py`
Simple Matplotlib quick-look viewer.

---

## 📚 `docs/`
Includes:
- technical documentation (LaTeX)
- generated PDFs
- math derivations
- early experiments (Jupyter)
- manuals (Quick Start, Full Manual)

This will eventually become a full documentation website.

---

## 🧪 `tests/`
Currently a placeholder (pre-alpha).  
This will become the home for:

- ingest validation tests  
- physics correctness tests  
- manifold tensor invariants  
- TopoCLIP training regression checks  

---

## 🧱 Build Artifacts

The following directories are intentionally present in pre-alpha:

- `x64/`  
- `Release/`  
- `.pyd` compiled extension files  
- CMake intermediates  
- PyInstaller-style `view/` folder  

These will be removed or replaced with a cleaner build system in Alpha.

---

# 3. Planned Alpha Layout

The Alpha release will restructure everything into the following form:

```
manifold_dynamics/
    core/
    physics/
    vision/
    io/
    cpp/
scripts/
docs/
tests/
data/
```

…but **not yet** — pre-alpha is intentionally “open lab space.”

---

# 4. Notes

This structure is *valid and acceptable* for a pre-alpha research release.  
It communicates:
- active development  
- real experimental workflows  
- the presence of multiple subsystems  
- transparency about backend components

A cleanup pass will come later.

---

# ✔ End of File  
