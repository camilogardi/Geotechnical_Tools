"""
Geotechnical Tools - Boussinesq stress computation module

This module implements vertical stress (sigma_z) calculations using Boussinesq's
theory for rectangular surface loads. The methodology uses superposition of
point load solutions over discretized sub-elements for accuracy.

References:
    Boussinesq, J. (1885). Application des potentiels à l'étude de l'équilibre
    et du mouvement des solides élastiques.
"""

import numpy as np
from typing import Tuple, Dict


def compute_rectangular_boussinesq(
    q: float,
    Lx: float,
    Ly: float,
    Xmin: float,
    Xmax: float,
    Ymin: float,
    Ymax: float,
    Zmax: float,
    Nx: int,
    Ny: int,
    Nz: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute vertical stress (sigma_z) distribution due to a rectangular
    surface load using Boussinesq theory with sub-element superposition.

    The rectangular load area is discretized into sub-elements (mx x my),
    and point load contributions are superposed at each evaluation point.
    This provides accurate stress distributions in the soil mass.

    Parameters
    ----------
    q : float
        Uniform surface load intensity in kPa (must be >= 0)
    Lx : float
        Length of rectangular load in X direction in meters (must be > 0)
    Ly : float
        Length of rectangular load in Y direction in meters (must be > 0)
    Xmin : float
        Minimum X coordinate for evaluation domain in meters
    Xmax : float
        Maximum X coordinate for evaluation domain in meters (must be > Xmin)
    Ymin : float
        Minimum Y coordinate for evaluation domain in meters
    Ymax : float
        Maximum Y coordinate for evaluation domain in meters (must be > Ymin)
    Zmax : float
        Maximum depth for evaluation in meters (must be > 0)
    Nx : int
        Number of points in X direction (must be >= 2)
    Ny : int
        Number of points in Y direction (must be >= 2)
    Nz : int
        Number of points in Z (depth) direction (must be >= 2)

    Returns
    -------
    X : np.ndarray
        1D array of length Nx with X coordinates in meters
    Y : np.ndarray
        1D array of length Ny with Y coordinates in meters
    Z : np.ndarray
        1D array of length Nz with Z coordinates (depth) in meters
    sigma : np.ndarray
        3D array with shape (Nz, Ny, Nx) containing vertical stress sigma_z
        in kPa at each point. Indexing: sigma[iz, iy, ix]

    Notes
    -----
    - Computational cost: O(Nx * Ny * Nz * mx * my) where mx, my are
      sub-element discretization (automatically chosen)
    - Recommended mx = my = min(40, max(4, max(Nx, Ny)))
    - To avoid singularity at z=0, evaluation starts at small offset (0.01m)
    - Load is assumed centered at origin (0, 0)
    - Positive Z is downward (depth increases)

    Raises
    ------
    ValueError
        If input parameters are invalid or inconsistent

    Examples
    --------
    >>> X, Y, Z, sigma = compute_rectangular_boussinesq(
    ...     q=100.0, Lx=2.0, Ly=3.0,
    ...     Xmin=-3.0, Xmax=3.0, Ymin=-4.0, Ymax=4.0, Zmax=5.0,
    ...     Nx=11, Ny=11, Nz=6
    ... )
    >>> sigma.shape
    (6, 11, 11)
    """
    # Input validation
    if q < 0:
        raise ValueError(f"Load q must be >= 0, got {q}")
    if Lx <= 0:
        raise ValueError(f"Lx must be > 0, got {Lx}")
    if Ly <= 0:
        raise ValueError(f"Ly must be > 0, got {Ly}")
    if Xmax <= Xmin:
        raise ValueError(f"Xmax ({Xmax}) must be > Xmin ({Xmin})")
    if Ymax <= Ymin:
        raise ValueError(f"Ymax ({Ymax}) must be > Ymin ({Ymin})")
    if Zmax <= 0:
        raise ValueError(f"Zmax must be > 0, got {Zmax}")
    if Nx < 2:
        raise ValueError(f"Nx must be >= 2, got {Nx}")
    if Ny < 2:
        raise ValueError(f"Ny must be >= 2, got {Ny}")
    if Nz < 2:
        raise ValueError(f"Nz must be >= 2, got {Nz}")

    # Create evaluation grids
    X = np.linspace(Xmin, Xmax, Nx)
    Y = np.linspace(Ymin, Ymax, Ny)
    # Start Z slightly below surface to avoid singularity
    Z = np.linspace(0.01, Zmax, Nz)

    # Determine sub-element discretization
    # Use finer discretization for better accuracy but limit for performance
    mx = min(40, max(4, max(Nx, Ny)))
    my = min(40, max(4, max(Nx, Ny)))

    # Discretize load area (centered at origin)
    x_load = np.linspace(-Lx/2, Lx/2, mx + 1)
    y_load = np.linspace(-Ly/2, Ly/2, my + 1)

    # Calculate sub-element centers and areas
    dx_load = Lx / mx
    dy_load = Ly / my
    dA = dx_load * dy_load  # Sub-element area
    dP = q * dA  # Point load for each sub-element

    x_centers = (x_load[:-1] + x_load[1:]) / 2
    y_centers = (y_load[:-1] + y_load[1:]) / 2

    # Initialize stress array: (Nz, Ny, Nx)
    sigma = np.zeros((Nz, Ny, Nx))

    # Compute stress at each point using Boussinesq point load solution
    # sigma_z = (3 * P * z^3) / (2 * pi * R^5)
    # where R = sqrt(x^2 + y^2 + z^2)
    for iz, z in enumerate(Z):
        for iy, y in enumerate(Y):
            for ix, x in enumerate(X):
                # Sum contributions from all sub-elements
                stress_sum = 0.0
                for xc in x_centers:
                    for yc in y_centers:
                        # Distance from load point to evaluation point
                        dx = x - xc
                        dy = y - yc
                        R = np.sqrt(dx**2 + dy**2 + z**2)

                        # Avoid division by zero
                        if R > 1e-10:
                            # Boussinesq point load formula
                            stress_sum += (3 * dP * z**3) / (2 * np.pi * R**5)

                sigma[iz, iy, ix] = stress_sum

    return X, Y, Z, sigma


def save_cache(path: str, data: Dict[str, np.ndarray]) -> None:
    """
    Save computed Boussinesq data to compressed numpy archive.

    Parameters
    ----------
    path : str
        File path for saving cache (should end with .npz)
    data : Dict[str, np.ndarray]
        Dictionary containing 'X', 'Y', 'Z', 'sigma' arrays

    Raises
    ------
    IOError
        If file cannot be written
    ValueError
        If required keys are missing from data

    Examples
    --------
    >>> data = {'X': X, 'Y': Y, 'Z': Z, 'sigma': sigma}
    >>> save_cache('Tools/cache/result.npz', data)
    """
    required_keys = {'X', 'Y', 'Z', 'sigma'}
    if not required_keys.issubset(data.keys()):
        missing = required_keys - set(data.keys())
        raise ValueError(f"Missing required keys: {missing}")

    np.savez_compressed(path, **data)


def load_cache(path: str) -> Dict[str, np.ndarray]:
    """
    Load computed Boussinesq data from numpy archive.

    Parameters
    ----------
    path : str
        File path to load cache from (.npz file)

    Returns
    -------
    Dict[str, np.ndarray]
        Dictionary containing 'X', 'Y', 'Z', 'sigma' arrays

    Raises
    ------
    FileNotFoundError
        If cache file does not exist
    ValueError
        If cache file is corrupted or missing required data

    Examples
    --------
    >>> data = load_cache('Tools/cache/result.npz')
    >>> X, Y, Z, sigma = data['X'], data['Y'], data['Z'], data['sigma']
    """
    try:
        archive = np.load(path)
        data = {key: archive[key] for key in archive.files}

        # Validate required keys
        required_keys = {'X', 'Y', 'Z', 'sigma'}
        if not required_keys.issubset(data.keys()):
            missing = required_keys - set(data.keys())
            raise ValueError(f"Cache file missing required keys: {missing}")

        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Cache file not found: {path}")
    except Exception as e:
        raise ValueError(f"Error loading cache file: {str(e)}")
