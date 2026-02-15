import numpy as np
import pytest
from manifold.physics.kesm import KESM_Lite
from manifold.core.io import ManifoldTensor

def test_kesm_stability(sample_tensor):
    # Setup
    solver = KESM_Lite(sample_tensor)

    stability = solver.compute_stability_index()

    assert stability.shape == sample_tensor.elevation.shape
    assert stability.dtype == np.float32

    # Test classification
    classification = solver.classify_terrain(stability, 0.1, -0.1)

    assert classification.shape == stability.shape
    assert classification.dtype == np.int8

    # Check values
    assert np.all(np.isin(classification, [-1, 0, 1]))
