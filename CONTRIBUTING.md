# 🤝 Contributing to Manifold Dynamics

Thank you for your interest in contributing to **Manifold Dynamics**.  
This repository is currently in **pre-alpha**, and the codebase is evolving
quickly. Contributions are welcome, but please read the guidelines below to
understand the current development state, expectations, and workflow.

---

# 🚧 Project Status: Pre-Alpha

Because this is an early-stage research codebase:

- APIs are unstable  
- Directory layout may change  
- Some modules are incomplete or experimental  
- Several files exist only as prototypes  
- The C++ backend is partially implemented  
- Documentation is still being written  

Contributions are welcome **as long as you understand that the underlying
infrastructure is shifting**.

---

# 🧭 Ways You Can Contribute

### ✔ Code contributions
- Bug fixes  
- Improvements to ingest / physics / vision modules  
- Better error handling  
- Backend enhancements (C++ solvers, bindings)  
- Performance optimizations  
- GPU acceleration (PyTorch / CUDA)  

### ✔ Documentation contributions
- Fixing unclear sections  
- Improving the README, Quick Start, or full manual  
- Adding examples or diagrams  
- Expanding docstrings  

### ✔ Data contributions
- Providing open DEMs or derived terrain datasets  
- Writing dataset loaders  

### ✔ Research & design contributions
- Proposing new terrain metrics  
- Suggesting physical models  
- Improving TopoCLIP training strategy  
- Benchmarks & validation approaches  

---

# 🛠 Development Setup

Clone the repository:

```bash
git clone <your-repo-url>
cd manifold-dynamics
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

(Optional) Build the C++ backend:

```bash
cd cpp
mkdir build && cd build
cmake ..
make -j$(nproc)
```

---

# 🧪 Adding New Code

Follow these guidelines:

- Use **clear, descriptive function names**  
- Keep modules focused (physics, vision, ingest, io)  
- Document new functions with docstrings  
- Add example usage when possible  
- Avoid breaking existing imports unless necessary  
- Use small, atomic pull requests  

---

# 🔄 Pull Request Process

1. **Fork** the repository  
2. Create a feature branch:  
   ```bash
   git checkout -b feature/my-improvement
   ```
3. Make your changes  
4. Run local tests (if applicable)  
5. Submit a **Pull Request** with:  
   - Clear explanation of what changed  
   - Motivation  
   - Any known side effects or limitations  

Pull requests do not need to be perfect — this is pre-alpha — but they must be **readable**.

---

# 🗂 Code Style

This project is not strict yet. Recommended:

- PEP8 where reasonable  
- Small, focused modules  
- Avoid long functions (>150 lines)  
- Keep imports clean  
- Prefer pure Python unless performance requires C++  

---

# 🐛 Reporting Issues

Please include:

- Steps to reproduce  
- OS + Python version  
- Dataset used (if applicable)  
- Screenshots or logs  
- Expected vs. observed behavior  

Issues are *not* required to be perfectly formatted. Even rough notes help.

---

# 🔐 Licensing

By submitting a PR, you agree that your contribution is released under the
project’s open-source license (MIT or equivalent once finalized).

---

# 💬 Communication

Use GitHub Issues for:

- Questions  
- Suggestions  
- Bug reports  
- Design discussions  

A Discord or forum may be added later depending on interest.

---

# 🙏 Thank You

Manifold Dynamics is an ambitious project blending:

- terrain physics  
- geomorphometry  
- multimodal models  
- C++ solvers  
- and scientific visualization  

Your contributions — even small ones — help push the field forward.

