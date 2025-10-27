"""
Tests for Boussinesq vertical stress calculations
"""
import pytest
import numpy as np
import os
import tempfile
from Tools import compute_rectangular_boussinesq, save_cache, load_cache, calc_circular_surcharge


def test_compute_rectangular_boussinesq_basic():
    """Test basic computation with modest parameters"""
    # Modest parameters for testing
    q = 100  # kPa
    Lx = 10  # m
    Ly = 10  # m
    Xmin, Xmax = -15, 15  # m
    Ymin, Ymax = -15, 15  # m
    Zmax = 20  # m
    Nx, Ny, Nz = 11, 11, 5
    
    X, Y, Z, sigma = compute_rectangular_boussinesq(
        q, Lx, Ly, Xmin, Xmax, Ymin, Ymax, Zmax, Nx, Ny, Nz
    )
    
    # Check output shapes
    assert X.shape == (Nx,), f"X shape mismatch: expected ({Nx},), got {X.shape}"
    assert Y.shape == (Ny,), f"Y shape mismatch: expected ({Ny},), got {Y.shape}"
    assert Z.shape == (Nz,), f"Z shape mismatch: expected ({Nz},), got {Z.shape}"
    assert sigma.shape == (Nz, Ny, Nx), f"sigma shape mismatch: expected ({Nz}, {Ny}, {Nx}), got {sigma.shape}"
    
    # Check coordinate ranges
    assert np.isclose(X[0], Xmin), f"X min mismatch: expected {Xmin}, got {X[0]}"
    assert np.isclose(X[-1], Xmax), f"X max mismatch: expected {Xmax}, got {X[-1]}"
    assert np.isclose(Y[0], Ymin), f"Y min mismatch: expected {Ymin}, got {Y[0]}"
    assert np.isclose(Y[-1], Ymax), f"Y max mismatch: expected {Ymax}, got {Y[-1]}"
    assert Z[0] > 0, f"Z should start above 0 to avoid singularity, got {Z[0]}"
    assert np.isclose(Z[-1], Zmax, rtol=0.01), f"Z max mismatch: expected ~{Zmax}, got {Z[-1]}"
    
    # Check that stress is non-negative for positive load
    assert np.all(sigma >= -1e-10), f"Stress should be non-negative, got min {sigma.min()}"
    
    # Check that stress decreases with depth (at center point)
    center_x_idx = Nx // 2
    center_y_idx = Ny // 2
    stress_profile = sigma[:, center_y_idx, center_x_idx]
    # Stress should generally decrease with depth under a surface load
    assert stress_profile[0] > stress_profile[-1], "Stress should decrease with depth"


def test_compute_rectangular_boussinesq_zero_load():
    """Test with zero load should give zero stress"""
    q = 0  # kPa
    Lx, Ly = 5, 5
    Xmin, Xmax = -10, 10
    Ymin, Ymax = -10, 10
    Zmax = 10
    Nx, Ny, Nz = 5, 5, 3
    
    X, Y, Z, sigma = compute_rectangular_boussinesq(
        q, Lx, Ly, Xmin, Xmax, Ymin, Ymax, Zmax, Nx, Ny, Nz
    )
    
    assert np.allclose(sigma, 0), "Zero load should produce zero stress"


def test_compute_rectangular_boussinesq_invalid_inputs():
    """Test that invalid inputs raise appropriate errors"""
    valid_params = {
        'q': 100, 'Lx': 10, 'Ly': 10,
        'Xmin': -10, 'Xmax': 10, 'Ymin': -10, 'Ymax': 10,
        'Zmax': 20, 'Nx': 5, 'Ny': 5, 'Nz': 5
    }
    
    # Negative load
    with pytest.raises(ValueError, match="non-negative"):
        params = valid_params.copy()
        params['q'] = -10
        compute_rectangular_boussinesq(**params)
    
    # Negative dimensions
    with pytest.raises(ValueError, match="positive"):
        params = valid_params.copy()
        params['Lx'] = -5
        compute_rectangular_boussinesq(**params)
    
    # Invalid domain
    with pytest.raises(ValueError, match="greater than"):
        params = valid_params.copy()
        params['Xmax'] = params['Xmin'] - 1
        compute_rectangular_boussinesq(**params)
    
    # Invalid grid size
    with pytest.raises(ValueError, match="at least 2"):
        params = valid_params.copy()
        params['Nx'] = 1
        compute_rectangular_boussinesq(**params)


def test_save_and_load_cache():
    """Test cache saving and loading functionality"""
    # Create test data
    X = np.linspace(0, 10, 5)
    Y = np.linspace(0, 10, 5)
    Z = np.linspace(0, 20, 3)
    sigma = np.random.rand(3, 5, 5) * 100
    
    data = {'X': X, 'Y': Y, 'Z': Z, 'sigma': sigma}
    
    # Use temporary file
    with tempfile.NamedTemporaryFile(suffix='.npz', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        # Save cache
        save_cache(tmp_path, data)
        assert os.path.exists(tmp_path), "Cache file was not created"
        
        # Load cache
        loaded_data = load_cache(tmp_path)
        
        # Verify loaded data
        assert 'X' in loaded_data and 'Y' in loaded_data and 'Z' in loaded_data and 'sigma' in loaded_data
        assert np.allclose(loaded_data['X'], X), "X data mismatch after load"
        assert np.allclose(loaded_data['Y'], Y), "Y data mismatch after load"
        assert np.allclose(loaded_data['Z'], Z), "Z data mismatch after load"
        assert np.allclose(loaded_data['sigma'], sigma), "sigma data mismatch after load"
        
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_load_cache_nonexistent():
    """Test that loading non-existent cache raises FileNotFoundError"""
    with pytest.raises(FileNotFoundError):
        load_cache('/nonexistent/path/to/cache.npz')


def test_stress_symmetry():
    """Test that stress field has expected symmetry for centered rectangular load"""
    q = 100
    Lx, Ly = 8, 8
    Xmin, Xmax = -12, 12
    Ymin, Ymax = -12, 12
    Zmax = 15
    Nx, Ny, Nz = 9, 9, 5  # Use odd number for symmetry test
    
    X, Y, Z, sigma = compute_rectangular_boussinesq(
        q, Lx, Ly, Xmin, Xmax, Ymin, Ymax, Zmax, Nx, Ny, Nz
    )
    
    center_x = Nx // 2
    center_y = Ny // 2
    
    # For a symmetric rectangular load, stress at symmetric points should be approximately equal
    # Check a few symmetric pairs (allowing for numerical tolerance)
    for iz in range(Nz):
        # Stress at (center+1, center) should equal stress at (center-1, center)
        if center_x > 0 and center_x < Nx - 1:
            stress_left = sigma[iz, center_y, center_x - 1]
            stress_right = sigma[iz, center_y, center_x + 1]
            assert np.isclose(stress_left, stress_right, rtol=0.1), \
                f"Symmetry violation in X at depth {iz}"


def test_calc_circular_surcharge_on_axis():
    """Test circular surcharge calculation on axis (r=0)"""
    q = 100  # kPa
    radius = 5  # m
    x_center = 0  # m (on axis)
    y_center = 0  # m (on axis)
    z_values = np.linspace(0.1, 30, 50)
    
    z_result, sigma = calc_circular_surcharge(q, radius, x_center, y_center, z_values)
    
    # Check output shapes
    assert z_result.shape == z_values.shape, "Z values shape mismatch"
    assert sigma.shape == z_values.shape, "Sigma shape mismatch"
    
    # Check that stress is non-negative
    assert np.all(sigma >= -1e-10), f"Stress should be non-negative, got min {sigma.min()}"
    
    # At surface (z→0), stress should approach q
    assert sigma[0] > 0.9 * q, f"Near-surface stress should be close to q, got {sigma[0]} vs {q}"
    
    # Stress should decrease with depth
    assert sigma[0] > sigma[-1], "Stress should decrease with depth"
    
    # At large depth, stress should approach zero
    assert sigma[-1] < 0.1 * q, f"Deep stress should be small, got {sigma[-1]}"


def test_calc_circular_surcharge_zero_load():
    """Test that zero load gives zero stress"""
    q = 0  # kPa
    radius = 5  # m
    x_center = 0
    y_center = 0
    z_values = np.linspace(0.1, 30, 20)
    
    z_result, sigma = calc_circular_surcharge(q, radius, x_center, y_center, z_values)
    
    assert np.allclose(sigma, 0), "Zero load should produce zero stress"


def test_calc_circular_surcharge_invalid_inputs():
    """Test that invalid inputs raise appropriate errors"""
    z_values = np.linspace(0.1, 30, 20)
    
    # Negative load
    with pytest.raises(ValueError, match="non-negative"):
        calc_circular_surcharge(q=-10, radius=5, x_center=0, y_center=0, z_values=z_values)
    
    # Negative radius
    with pytest.raises(ValueError, match="positive"):
        calc_circular_surcharge(q=100, radius=-5, x_center=0, y_center=0, z_values=z_values)
    
    # Invalid depth values (<=0)
    with pytest.raises(ValueError, match="positive"):
        z_bad = np.array([-1, 0, 1, 2])
        calc_circular_surcharge(q=100, radius=5, x_center=0, y_center=0, z_values=z_bad)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
