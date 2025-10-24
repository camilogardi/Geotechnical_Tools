"""
Test suite for Tools module
"""

import pytest
import numpy as np
from Tools.Tools import compute_rectangular_boussinesq, save_cache, load_cache
import os
import tempfile


def test_compute_rectangular_boussinesq_basic():
    """Test basic Boussinesq computation with modest parameters"""
    # Use modest parameters for testing
    X, Y, Z, sigma = compute_rectangular_boussinesq(
        q=100.0,
        Lx=2.0,
        Ly=3.0,
        Xmin=-3.0,
        Xmax=3.0,
        Ymin=-4.0,
        Ymax=4.0,
        Zmax=5.0,
        Nx=11,
        Ny=11,
        Nz=5
    )

    # Verify shapes
    assert X.shape == (11,), f"Expected X shape (11,), got {X.shape}"
    assert Y.shape == (11,), f"Expected Y shape (11,), got {Y.shape}"
    assert Z.shape == (5,), f"Expected Z shape (5,), got {Z.shape}"
    assert sigma.shape == (5, 11, 11), f"Expected sigma shape (5, 11, 11), got {sigma.shape}"

    # Verify sigma is non-negative for positive q
    assert np.all(sigma >= -1e-10), "Sigma should be non-negative for q > 0"

    # Verify stress decreases with depth (approximately)
    # Check at center point
    center_x_idx = 5
    center_y_idx = 5
    center_stresses = sigma[:, center_y_idx, center_x_idx]
    # Stress should generally decrease with depth, but not strictly monotonic
    # Just check that last is less than first
    assert center_stresses[-1] < center_stresses[0], \
        "Stress should generally decrease with depth"


def test_compute_rectangular_boussinesq_zero_load():
    """Test that zero load produces zero stress"""
    X, Y, Z, sigma = compute_rectangular_boussinesq(
        q=0.0,
        Lx=2.0,
        Ly=2.0,
        Xmin=-2.0,
        Xmax=2.0,
        Ymin=-2.0,
        Ymax=2.0,
        Zmax=3.0,
        Nx=5,
        Ny=5,
        Nz=3
    )

    assert np.allclose(sigma, 0.0), "Zero load should produce zero stress"


def test_compute_rectangular_boussinesq_invalid_inputs():
    """Test that invalid inputs raise ValueError"""
    # Negative load
    with pytest.raises(ValueError, match="q must be >= 0"):
        compute_rectangular_boussinesq(
            q=-10.0, Lx=2.0, Ly=2.0,
            Xmin=-2.0, Xmax=2.0, Ymin=-2.0, Ymax=2.0, Zmax=3.0,
            Nx=5, Ny=5, Nz=3
        )

    # Invalid Lx
    with pytest.raises(ValueError, match="Lx must be > 0"):
        compute_rectangular_boussinesq(
            q=100.0, Lx=-2.0, Ly=2.0,
            Xmin=-2.0, Xmax=2.0, Ymin=-2.0, Ymax=2.0, Zmax=3.0,
            Nx=5, Ny=5, Nz=3
        )

    # Invalid domain
    with pytest.raises(ValueError, match="Xmax .* must be > Xmin"):
        compute_rectangular_boussinesq(
            q=100.0, Lx=2.0, Ly=2.0,
            Xmin=2.0, Xmax=-2.0, Ymin=-2.0, Ymax=2.0, Zmax=3.0,
            Nx=5, Ny=5, Nz=3
        )

    # Invalid Nx
    with pytest.raises(ValueError, match="Nx must be >= 2"):
        compute_rectangular_boussinesq(
            q=100.0, Lx=2.0, Ly=2.0,
            Xmin=-2.0, Xmax=2.0, Ymin=-2.0, Ymax=2.0, Zmax=3.0,
            Nx=1, Ny=5, Nz=3
        )


def test_cache_save_and_load():
    """Test saving and loading cache files"""
    # Create temporary directory for cache
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_path = os.path.join(tmpdir, 'test_cache.npz')

        # Generate some data
        X, Y, Z, sigma = compute_rectangular_boussinesq(
            q=100.0, Lx=2.0, Ly=2.0,
            Xmin=-2.0, Xmax=2.0, Ymin=-2.0, Ymax=2.0, Zmax=3.0,
            Nx=5, Ny=5, Nz=3
        )

        # Save cache
        data = {'X': X, 'Y': Y, 'Z': Z, 'sigma': sigma}
        save_cache(cache_path, data)

        # Verify file exists
        assert os.path.exists(cache_path), "Cache file should exist"

        # Load cache
        loaded_data = load_cache(cache_path)

        # Verify loaded data matches
        assert np.allclose(loaded_data['X'], X), "Loaded X should match original"
        assert np.allclose(loaded_data['Y'], Y), "Loaded Y should match original"
        assert np.allclose(loaded_data['Z'], Z), "Loaded Z should match original"
        assert np.allclose(loaded_data['sigma'], sigma), "Loaded sigma should match original"


def test_cache_missing_file():
    """Test that loading non-existent cache raises error"""
    with pytest.raises(FileNotFoundError):
        load_cache('/nonexistent/path/to/cache.npz')


def test_cache_missing_keys():
    """Test that saving cache with missing keys raises error"""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_path = os.path.join(tmpdir, 'test_cache.npz')
        
        # Create data with missing key
        incomplete_data = {'X': np.array([1, 2, 3])}
        
        with pytest.raises(ValueError, match="Missing required keys"):
            save_cache(cache_path, incomplete_data)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
