import os
import numpy as np
from manifold.core.io import ManifoldTensor

def test_manifold_tensor_save_load(tmp_path):
    # Setup
    rows, cols = 50, 50
    t = ManifoldTensor(rows=rows, cols=cols, gsd=5.0, origin=(45.0, -120.0))
    t.elevation = np.random.rand(rows, cols).astype(np.float32)
    t.derived = np.random.rand(6, rows, cols).astype(np.float32)

    path = tmp_path / "test.mft"
    t.save(str(path))

    assert os.path.exists(path)

    # Load
    t2 = ManifoldTensor.load(str(path))

    assert t2.rows == rows
    assert t2.cols == cols
    assert t2.gsd == 5.0
    assert np.allclose(t2.elevation, t.elevation)
    assert np.allclose(t2.derived, t.derived)

def test_manifold_tensor_header_validation(tmp_path):
    path = tmp_path / "bad.mft"
    with open(path, 'wb') as f:
        f.write(b"BAD1" + b"\x00"*92)

    import pytest
    with pytest.raises(ValueError):
        ManifoldTensor.load(str(path))
