# 🚀 Manifold Dynamics: Quick Start Guide

This guide will help you get up and running with Manifold Dynamics.

## 1. Installation

Prerequisites:
- Python 3.9+
- GDAL (optional, but recommended for `rasterio`)

### Step 1: Clone the Repository
```bash
git clone https://github.com/ManifoldDynamics/manifold-dynamics.git
cd manifold-dynamics
```

### Step 2: Install Dependencies
We recommend using a virtual environment.
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in editable mode with test dependencies
pip install -e .[test]
```

## 2. Ingesting Terrain Data

Manifold Dynamics uses a custom tensor format (`.mft`). You first need to convert your raw DEM (GeoTIFF) into this format.

```bash
# Command Line Interface
manifold-ingest path/to/input.tif path/to/output.mft
```

Example:
```bash
manifold-ingest data/raw/smokies.tif data/processed/smokies.mft
```

This process will:
- Fill voids
- Destripe the terrain
- Compute normals, roughness, TPI, and VRM
- Save the 7-channel tensor

## 3. Running Physics Simulations (KESM-Lite)

The KESM-Lite module simulates cold-air drainage physics.

```bash
python -m manifold.physics.kesm data/processed/smokies.mft
```

If you have `napari` installed (included in dependencies), this will open a 3D viewer showing the terrain, flux potential, and classified sinks/peaks.

## 4. Training TopoCLIP (Multimodal Learning)

Train the multimodal terrain-text model.

```bash
python -m manifold.vision.topo_clip_train data/processed/smokies.mft --epochs 5 --lr 1e-4
```

This will run a training loop using the specified MFT file.

## 5. Running Tests

To verify your installation works correctly:

```bash
pytest tests/
```

## Troubleshooting

- **ImportError: No module named 'manifold'**: Make sure you installed with `pip install -e .` and your virtual environment is active.
- **GDAL errors**: Install GDAL system dependencies (e.g., `libgdal-dev` on Linux, or use conda).

For more details, see `README.md` and `docs/`.
