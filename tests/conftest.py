import pytest
import numpy as np
import os
from manifold.core.io import ManifoldTensor

@pytest.fixture
def sample_tensor():
    rows, cols = 100, 100
    gsd = 10.0
    tensor = ManifoldTensor(rows=rows, cols=cols, gsd=gsd, origin=(0.0, 0.0))
    # Fill with some data
    tensor.elevation = np.random.rand(rows, cols).astype(np.float32) * 1000
    tensor.derived = np.random.rand(6, rows, cols).astype(np.float32)
    return tensor

@pytest.fixture
def sample_geotiff_path(tmp_path):
    import rasterio
    from rasterio.transform import from_origin

    path = tmp_path / "test.tif"
    arr = (np.random.rand(100, 100) * 1000).astype(np.float32)
    transform = from_origin(0, 0, 10, 10)

    with rasterio.open(
        path,
        'w',
        driver='GTiff',
        height=arr.shape[0],
        width=arr.shape[1],
        count=1,
        dtype=arr.dtype,
        crs='+proj=latlong',
        transform=transform,
    ) as dst:
        dst.write(arr, 1)

    return str(path)
