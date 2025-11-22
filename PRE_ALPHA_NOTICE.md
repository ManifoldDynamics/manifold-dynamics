# 🚧 Manifold Dynamics — Pre-Alpha Notice

Manifold Dynamics is currently in **pre-alpha**, and the repository reflects an
active research and development environment. The codebase is being released
early for transparency, community visibility, and to support collaboration with
researchers who want to explore or contribute to the core ideas.

Please read the following before using or evaluating the repository.

---

## ⚠️ Development Status

- Many modules are **incomplete**, **experimental**, or **actively changing**.
- APIs, file formats, function signatures, and directory layout **will change**.
- Several components (Python, C++, physics models, vision modules) are in
  various stages of integration.
- Pre-built binaries, compiled artifacts, and development files are present
  intentionally for ease of testing.
- Not all features have been tested across full datasets or OS configurations.

---

## 📁 Repository Structure

The repo includes a mixture of:
- Python modules (core, physics, vision)
- C++ backend code (CMake project, Visual Studio project files)
- Backend bindings (`*.pyd`, compiled solvers)
- Raw and processed terrain datasets
- Visualization tools and diagnostics
- Early documentation, LaTeX manuscripts, notebooks

This layout mirrors the internal development structure and will be reorganized
in future releases.

---

## 🧪 Experimental Components

The following high-level systems are **prototype-level**:

- **KESM-Lite** cold-air drainage physics  
- **TopoCLIP** terrain ↔ text multimodal model  
- **ManifoldTensor (.mft)** terrain representation  
- Structure-tensor roughness, normals, TPI, VRM computation  
- DEM ingest and destriping system  
- Visualization and patch extraction tools  

Expect inconsistencies, missing features, and rough edges.

---

## 📌 Pre-Alpha Goals

This early release is intended to:

- Share progress with the community early  
- Enable reproducibility of the core ideas  
- Allow contributors to experiment with the code  
- Prepare for a more stable **Alpha** release soon  
- Gather feedback before finalizing the architecture  

---

## 🚀 What’s Coming Soon

- Cleaned and standardized Python package  
- Fully documented API  
- Stable version of the C++ backend  
- Robust physics models and validation  
- Trained TopoCLIP weights and dataset  
- Significantly expanded documentation  
- Proper unit tests and CI/CD  
- Complete research paper and benchmarks  

---

## 🙏 Thank You

Thank you for checking out Manifold Dynamics in its earliest stage.
Your feedback, issues, and ideas are extremely valuable as the project
moves toward its first stable release.