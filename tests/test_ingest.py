import numpy as np
import os
import pytest
from manifold.core.ingest import (
    calculate_normals,
    calculate_vrm,
    calculate_tpi,
    compute_eigen_roughness,
    destripe_terrain,
    ingest_geotiff
)

def test_normals():
    elev = np.zeros((10, 10), dtype=np.float32)
    # create a slope
    for i in range(10):
        elev[i, :] = i

    gsd = 1.0
    normals = calculate_normals(elev, gsd, None)

    # slope is 1 in y (actually x in numpy gradient order is rows, cols)
    # gradient(z, gsd) returns dy, dx
    # dy should be 1, dx should be 0

    assert normals.shape == (3, 10, 10)
    # checking rough values
    # nz should be positive (up)
    assert np.all(normals[2] > 0)

def test_tpi():
    elev = np.ones((20, 20), dtype=np.float32) * 100
    elev[10, 10] = 110 # peak

    tpi = calculate_tpi(elev)
    assert tpi[10, 10] > 0 # positive for peak

def test_full_ingest(sample_geotiff_path, tmp_path):
    output_path = tmp_path / "output.mft"

    ingest_geotiff(str(sample_geotiff_path), str(output_path))

    assert os.path.exists(output_path)

    from manifold.core.io import ManifoldTensor
    t = ManifoldTensor.load(str(output_path))
    assert t.derived.shape[0] == 6
    assert not np.isnan(t.elevation).all()
