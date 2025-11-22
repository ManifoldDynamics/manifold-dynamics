from setuptools import setup, find_namespace_packages

setup(
    name="manifold-engine",
    version="0.1.0-alpha",
    description="The Open Source Computational Geography Engine",
    author="Manifold Dynamics (R&D Division of Praetor Defense)",
    url="https://github.com/ManifoldDynamics/manifold-dynamics",
    license="Apache 2.0",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=[
        "numpy>=1.26.0",
        "scipy>=1.11.0",
        "gdal>=3.8.0",
        "matplotlib>=3.8.0",
    ],
    entry_points={
        "console_scripts": [
            "manifold-ingest=manifold.core.ingest:main",
        ],
    },
)