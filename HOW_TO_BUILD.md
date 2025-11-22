# 🛠️ How to Build Manifold Dynamics (Pre-Alpha)

This guide explains how to install dependencies, run the Python version, build
the C++ backend, and verify the installation. Because the repository is in
pre-alpha, multiple build flows are supported and some modules have partial or
experimental build pipelines.

---

# 1. Python-Only Quick Start (Recommended)

If you just want to run the ingest pipeline, KESM physics, TopoCLIP, or the
viewers, the Python-only route requires **no compilation**.

## Install dependencies
```bash
pip install -r requirements.txt
```

Recommended extras:
```bash
pip install torch transformers rasterio scipy napari matplotlib numpy
```

You are now ready to run:

```bash
python ingest.py
python vis.py
python diagnose.py
python viewer.py
```

---

# 2. Optional: Using the Prebuilt C++ Backend (Windows)

The repository includes a **precompiled `.pyd` backend** located in:

```
cpp/_manifold_backend.cp312-win_amd64.pyd
```

Python will import this automatically if present:

```python
import _manifold_backend
```

No compilation is required.

---

# 3. Building the C++ Backend From Source (Advanced)

If you want to build the backend manually (recommended for Linux/macOS), use the
CMake build system included in `/cpp`.

## Requirements
- CMake ≥ 3.16  
- MSVC / Clang / GCC  
- Python ≥ 3.10 development headers  
- pybind11 (header-only)

---

# 3.1 Windows Build Instructions (Visual Studio)

```bash
cd cpp
mkdir build
cd build
cmake .. -A x64
cmake --build . --config Release
```

The resulting `.pyd` will appear in:

```
cpp/build/Release/
```

Copy it into your Python package directory:

```
manifold/core/
```

---

# 3.2 Linux Build Instructions

```bash
cd cpp
mkdir build
cd build
cmake ..
make -j$(nproc)
```

Output:

```
./_manifold_backend*.so
```

Move to your Python package:

```bash
cp _manifold_backend*.so ../../manifold/core/
```

---

# 3.3 macOS Build Instructions

```bash
cd cpp
mkdir build
cd build
cmake -DCMAKE_OSX_ARCHITECTURES="arm64;x86_64" ..
make -j$(sysctl -n hw.ncpu)
```

Copy resulting `.so`:

```bash
cp _manifold_backend*.so ../../manifold/core/
```

---

# 4. Validating the Backend

```bash
python - <<EOF
import _manifold_backend
print(_manifold_backend.__doc__)
EOF
```

If it imports without error, the build succeeded.

---

# 5. Building the Full System (Python + C++)

### Step 1 — Install Python packages
```bash
pip install -r requirements.txt
```

### Step 2 — Build backend (optional)
See section 3.

### Step 3 — Test ingest + physics
```bash
python ingest.py
python kesm.py
```

### Step 4 — Train TopoCLIP
```bash
python topo_clip_train.py
```

---

# 6. File Paths & Assumptions

### Python modules:
```
manifold/core/
manifold/physics/
manifold/vision/
```

### C++ backend sources:
```
cpp/*.cpp
cpp/*.h
cpp/CMakeLists.txt
```

### Dataset layout:
```
data/raw/
data/processed/
data/biomes/
```

---

# 7. Cleaning Build Output

### Windows:
```bash
rm -r cpp/build
rm -r x64
rm -r Release
```

### Linux/macOS:
```bash
rm -r cpp/build
```

---

# 8. Troubleshooting

### CMake cannot locate Python
```bash
cmake .. -DPython_EXECUTABLE=$(which python3)
```

### pybind11 not found
```bash
pip install pybind11
```

Or specify manually:

```bash
cmake .. -DPYBIND11_INCLUDE_DIR=/path/to/pybind11/include
```

### ImportError: cannot load compiled extension
Ensure extension is placed inside:

```
manifold/core/
```

---

# 9. Notes About Pre-Alpha State

- C++ backend is partially implemented.
- Linux/macOS builds may require patching.
- Python is the reference implementation.
- APIs and directory layout will change.
- Backend compilation is optional for most features.

---

# 10. Coming for Alpha Release

- Unified Python + C++ build with `pyproject.toml`
- Automated manylinux wheel generation
- Complete CI/CD
- Stronger backend integration
- Full documentation site

---
