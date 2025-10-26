"""
Tests for calculation and visualization functions in calculations.py
"""
import pytest
import numpy as np
import hashlib
from calculations import (
    get_cache_hash,
    compute_boussinesq_cached,
    interpolate_value,
    create_xz_plot,
    create_yz_plot,
    create_depth_profile_plot,
    generate_pdf_report
)


def test_get_cache_hash():
    """Test that cache hash is generated correctly and consistently"""
    # Test with specific parameters
    hash1 = get_cache_hash(100, 10, 10, -20, 20, -20, 20, 30, 41, 41, 31)
    hash2 = get_cache_hash(100, 10, 10, -20, 20, -20, 20, 30, 41, 41, 31)

    # Hash should be consistent for same parameters
    assert hash1 == hash2, "Cache hash should be consistent for identical parameters"

    # Hash should be 8 characters long
    assert len(hash1) == 8, f"Cache hash should be 8 characters, got {len(hash1)}"

    # Hash should be different for different parameters
    hash3 = get_cache_hash(200, 10, 10, -20, 20, -20, 20, 30, 41, 41, 31)
    assert hash1 != hash3, "Cache hash should differ for different parameters"


def test_get_cache_hash_format():
    """Test that cache hash uses correct encoding"""
    q, Lx, Ly = 100, 10, 10
    Xmin, Xmax, Ymin, Ymax = -20, 20, -20, 20
    Zmax, Nx, Ny, Nz = 30, 41, 41, 31

    # Generate hash manually to verify implementation
    params_str = f"{q}_{Lx}_{Ly}_{Xmin}_{Xmax}_{Ymin}_{Ymax}_{Zmax}_{Nx}_{Ny}_{Nz}"
    expected_hash = hashlib.md5(params_str.encode()).hexdigest()[:8]

    actual_hash = get_cache_hash(q, Lx, Ly, Xmin, Xmax, Ymin, Ymax, Zmax, Nx, Ny, Nz)

    assert actual_hash == expected_hash, "Hash implementation should match expected format"


def test_compute_boussinesq_cached():
    """Test cached Boussinesq computation wrapper"""
    q = 100
    Lx, Ly = 10, 10
    Xmin, Xmax = -15, 15
    Ymin, Ymax = -15, 15
    Zmax = 20
    Nx, Ny, Nz = 11, 11, 5

    X, Y, Z, sigma = compute_boussinesq_cached(
        q, Lx, Ly, Xmin, Xmax, Ymin, Ymax, Zmax, Nx, Ny, Nz
    )

    # Check output shapes
    assert X.shape == (Nx,), "X shape mismatch"
    assert Y.shape == (Ny,), "Y shape mismatch"
    assert Z.shape == (Nz,), "Z shape mismatch"
    assert sigma.shape == (Nz, Ny, Nx), "sigma shape mismatch"

    # Check that stress is non-negative for positive load
    assert np.all(sigma >= -1e-10), "Stress should be non-negative"


def test_interpolate_value():
    """Test trilinear interpolation of stress values"""
    # Create simple test grid
    X = np.array([0, 10, 20])
    Y = np.array([0, 10, 20])
    Z = np.array([0, 10, 20])

    # Create simple stress field (constant value)
    sigma = np.ones((3, 3, 3)) * 100.0

    # Interpolate at grid point (should return exact value)
    result = interpolate_value(X, Y, Z, sigma, 10, 10, 10)
    assert np.isclose(result, 100.0), "Interpolation at grid point should return exact value"

    # Interpolate at midpoint between grid points
    result_mid = interpolate_value(X, Y, Z, sigma, 5, 5, 5)
    assert np.isclose(result_mid, 100.0), "Interpolation should work for midpoints"


def test_interpolate_value_gradient():
    """Test interpolation with a gradient stress field"""
    X = np.array([0, 10, 20])
    Y = np.array([0, 10, 20])
    Z = np.array([0, 10, 20])

    # Create stress field that increases with X
    sigma = np.zeros((3, 3, 3))
    for ix in range(3):
        sigma[:, :, ix] = X[ix]

    # Test interpolation
    result = interpolate_value(X, Y, Z, sigma, 5, 10, 10)
    assert 0 < result < 10, f"Interpolated value should be between boundary values, got {result}"


def test_create_xz_plot():
    """Test X-Z contour plot creation"""
    # Create simple test data
    X = np.linspace(-10, 10, 11)
    Y = np.linspace(-10, 10, 11)
    Z = np.linspace(1, 20, 10)
    sigma = np.random.rand(10, 11, 11) * 100

    # Create plot at y=0
    fig = create_xz_plot(X, Y, Z, sigma, y_val=0.0)

    # Check that figure is created
    assert fig is not None, "Figure should be created"
    assert hasattr(fig, 'data'), "Figure should have data attribute"
    assert len(fig.data) > 0, "Figure should contain plot data"

    # Check figure layout
    assert 'X-Z' in fig.layout.title.text, "Title should mention X-Z"
    assert 'X (m)' in fig.layout.xaxis.title.text, "X-axis should be labeled"
    assert 'Z (m)' in fig.layout.yaxis.title.text or 'Profundidad' in fig.layout.yaxis.title.text, \
        "Y-axis should indicate depth"


def test_create_yz_plot():
    """Test Y-Z contour plot creation"""
    # Create simple test data
    X = np.linspace(-10, 10, 11)
    Y = np.linspace(-10, 10, 11)
    Z = np.linspace(1, 20, 10)
    sigma = np.random.rand(10, 11, 11) * 100

    # Create plot at x=0
    fig = create_yz_plot(X, Y, Z, sigma, x_val=0.0)

    # Check that figure is created
    assert fig is not None, "Figure should be created"
    assert hasattr(fig, 'data'), "Figure should have data attribute"
    assert len(fig.data) > 0, "Figure should contain plot data"

    # Check figure layout
    assert 'Y-Z' in fig.layout.title.text, "Title should mention Y-Z"
    assert 'Y (m)' in fig.layout.xaxis.title.text, "X-axis should be labeled"
    assert 'Z (m)' in fig.layout.yaxis.title.text or 'Profundidad' in fig.layout.yaxis.title.text, \
        "Y-axis should indicate depth"


def test_create_depth_profile_plot():
    """Test depth profile plot creation"""
    # Create simple test data
    X = np.linspace(-10, 10, 11)
    Y = np.linspace(-10, 10, 11)
    Z = np.linspace(1, 20, 10)
    sigma = np.random.rand(10, 11, 11) * 100

    # Create depth profile at (0, 0)
    fig = create_depth_profile_plot(X, Y, Z, sigma, x_point=0.0, y_point=0.0)

    # Check that figure is created
    assert fig is not None, "Figure should be created"
    assert hasattr(fig, 'data'), "Figure should have data attribute"
    assert len(fig.data) > 0, "Figure should contain plot data"

    # Check figure layout
    assert 'Perfil' in fig.layout.title.text or 'Esfuerzo' in fig.layout.title.text, \
        "Title should mention profile or stress"
    assert 'σz' in fig.layout.xaxis.title.text or 'kPa' in fig.layout.xaxis.title.text, \
        "X-axis should indicate stress"
    assert 'Z (m)' in fig.layout.yaxis.title.text or 'Profundidad' in fig.layout.yaxis.title.text, \
        "Y-axis should indicate depth"


def test_generate_pdf_report():
    """Test PDF report generation"""
    # Create test parameters
    params = {
        'q': 100,
        'Lx': 10,
        'Ly': 10,
        'Xmin': -20,
        'Xmax': 20,
        'Ymin': -20,
        'Ymax': 20,
        'Zmax': 30,
        'Nx': 41,
        'Ny': 41,
        'Nz': 31
    }

    # Create test data
    X = np.linspace(-20, 20, 41)
    Y = np.linspace(-20, 20, 41)
    Z = np.linspace(1, 30, 31)
    sigma = np.random.rand(31, 41, 41) * 100

    # Create test plot configuration
    plots_config = [
        {'type': 'Corte X-Z', 'y_val': 0.0},
        {'type': 'Corte Y-Z', 'x_val': 0.0}
    ]

    # Generate PDF
    pdf_bytes = generate_pdf_report(params, plots_config, X, Y, Z, sigma)

    # Check that PDF is generated
    assert pdf_bytes is not None, "PDF should be generated"
    assert isinstance(pdf_bytes, bytes), "PDF should be returned as bytes"
    assert len(pdf_bytes) > 0, "PDF should not be empty"

    # Check PDF header (PDF files start with %PDF-)
    assert pdf_bytes[:4] == b'%PDF', "Should be a valid PDF file"


def test_generate_pdf_report_no_plots():
    """Test PDF report generation without plots"""
    params = {
        'q': 100,
        'Lx': 10,
        'Ly': 10,
        'Xmin': -20,
        'Xmax': 20,
        'Ymin': -20,
        'Ymax': 20,
        'Zmax': 30,
        'Nx': 41,
        'Ny': 41,
        'Nz': 31
    }

    X = np.linspace(-20, 20, 41)
    Y = np.linspace(-20, 20, 41)
    Z = np.linspace(1, 30, 31)
    sigma = np.random.rand(31, 41, 41) * 100

    # Generate PDF with no plots
    pdf_bytes = generate_pdf_report(params, [], X, Y, Z, sigma)

    # Check that PDF is still generated
    assert pdf_bytes is not None, "PDF should be generated even without plots"
    assert isinstance(pdf_bytes, bytes), "PDF should be returned as bytes"
    assert len(pdf_bytes) > 0, "PDF should not be empty"
    assert pdf_bytes[:4] == b'%PDF', "Should be a valid PDF file"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
