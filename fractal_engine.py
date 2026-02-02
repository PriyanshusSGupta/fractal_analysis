"""
Fractal Dimension Calculation Engine for Seismic Data Analysis
Uses the Box-Counting Method to compute fractal dimension of earthquake distributions.

Author: Seismic Analysis Team
Date: February 2026
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Tuple, Optional, Dict
import warnings


def validate_data(latitudes: np.ndarray, longitudes: np.ndarray) -> None:
    """
    Validate input earthquake coordinate data.
    
    Parameters:
    -----------
    latitudes : np.ndarray
        Array of latitude values
    longitudes : np.ndarray
        Array of longitude values
        
    Raises:
    -------
    ValueError: If data is invalid
    """
    if len(latitudes) == 0 or len(longitudes) == 0:
        raise ValueError("Coordinate arrays cannot be empty")
    
    if len(latitudes) != len(longitudes):
        raise ValueError("Latitude and longitude arrays must have same length")
    
    if not np.all(np.isfinite(latitudes)) or not np.all(np.isfinite(longitudes)):
        raise ValueError("Coordinates contain NaN or infinite values")
    
    if np.any(np.abs(latitudes) > 90):
        raise ValueError("Latitude values must be between -90 and 90")
    
    if np.any(np.abs(longitudes) > 180):
        raise ValueError("Longitude values must be between -180 and 180")


def get_box_counts(latitudes: np.ndarray, longitudes: np.ndarray, box_size: float) -> int:
    """
    Count number of boxes (grid cells) that contain at least one earthquake.
    
    Parameters:
    -----------
    latitudes : np.ndarray
        Array of earthquake latitudes
    longitudes : np.ndarray
        Array of earthquake longitudes
    box_size : float
        Size of each box/grid cell in degrees
        
    Returns:
    --------
    int : Number of non-empty boxes
    """
    # Create grid boundaries
    lat_min, lat_max = latitudes.min(), latitudes.max()
    lon_min, lon_max = longitudes.min(), longitudes.max()
    
    # Calculate grid dimensions
    lat_bins = np.arange(lat_min, lat_max + box_size, box_size)
    lon_bins = np.arange(lon_min, lon_max + box_size, box_size)
    
    # Use 2D histogram to count boxes
    hist, _, _ = np.histogram2d(latitudes, longitudes, bins=[lat_bins, lon_bins])
    
    # Count non-empty boxes
    non_empty_boxes = np.sum(hist > 0)
    
    return non_empty_boxes


def calculate_fractal_dimension(box_sizes: np.ndarray, counts: np.ndarray) -> Tuple[float, float, float, float]:
    """
    Calculate fractal dimension using linear regression on log-log plot.
    
    The fractal dimension D is the negative slope of the relationship:
    log(N) = -D * log(r) + c
    where N is the number of boxes and r is the box size.
    
    Parameters:
    -----------
    box_sizes : np.ndarray
        Array of box sizes used
    counts : np.ndarray
        Array of corresponding box counts
        
    Returns:
    --------
    Tuple[float, float, float, float]:
        - D: Fractal dimension
        - r_squared: Coefficient of determination (goodness of fit)
        - std_err: Standard error of the slope
        - intercept: Y-intercept of the fit
    """
    # Convert to log scale
    log_r = np.log10(box_sizes)
    log_N = np.log10(counts)
    
    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(log_r, log_N)
    
    # Fractal dimension is negative slope
    D = -slope
    r_squared = r_value ** 2
    
    return D, r_squared, std_err, intercept


def box_counting(
    latitudes: np.ndarray,
    longitudes: np.ndarray,
    min_box_size: float = 0.1,
    max_box_size: Optional[float] = None,
    num_scales: int = 20,
    return_details: bool = False
) -> Dict:
    """
    Calculate fractal dimension of earthquake distribution using box-counting method.
    
    This is the main function that implements the box-counting algorithm:
    1. Creates a grid of different box sizes (log-spaced)
    2. For each box size, counts how many boxes contain earthquakes
    3. Fits a line to log(count) vs log(box_size)
    4. The negative slope is the fractal dimension D
    
    Parameters:
    -----------
    latitudes : np.ndarray or list
        Earthquake latitude coordinates
    longitudes : np.ndarray or list
        Earthquake longitude coordinates
    min_box_size : float, optional (default=0.1)
        Minimum box size in degrees
    max_box_size : float, optional
        Maximum box size in degrees. If None, uses 1/4 of spatial extent
    num_scales : int, optional (default=20)
        Number of different box sizes to test
    return_details : bool, optional (default=False)
        If True, returns detailed analysis including box sizes and counts
        
    Returns:
    --------
    Dict containing:
        - 'D': Fractal dimension
        - 'r_squared': Goodness of fit (R²)
        - 'std_error': Standard error of D estimate
        - 'n_points': Number of earthquake events analyzed
        - 'spatial_extent': Geographic extent (lat_range, lon_range)
        If return_details=True, also includes:
            - 'box_sizes': Array of box sizes used
            - 'counts': Array of box counts
            - 'intercept': Regression intercept
            
    Example:
    --------
    >>> import pandas as pd
    >>> data = pd.read_csv('earthquakes.csv')
    >>> result = box_counting(data['latitude'], data['longitude'])
    >>> print(f"Fractal Dimension: {result['D']:.3f} ± {result['std_error']:.3f}")
    >>> print(f"R² = {result['r_squared']:.3f}")
    """
    # Convert to numpy arrays
    latitudes = np.array(latitudes)
    longitudes = np.array(longitudes)
    
    # Validate input data
    validate_data(latitudes, longitudes)
    
    # Calculate spatial extent
    lat_range = latitudes.max() - latitudes.min()
    lon_range = longitudes.max() - longitudes.min()
    
    # Set max_box_size if not provided (use 1/4 of spatial extent)
    if max_box_size is None:
        max_box_size = min(lat_range, lon_range) / 4.0
    
    # Ensure min_box_size < max_box_size
    if min_box_size >= max_box_size:
        raise ValueError(f"min_box_size ({min_box_size}) must be less than max_box_size ({max_box_size})")
    
    # Generate logarithmically-spaced box sizes
    box_sizes = np.logspace(
        np.log10(min_box_size),
        np.log10(max_box_size),
        num=num_scales
    )
    
    # Calculate box counts for each size
    counts = np.array([
        get_box_counts(latitudes, longitudes, box_size)
        for box_size in box_sizes
    ])
    
    # Filter out zero counts (can occur if box size is too small)
    valid_mask = counts > 0
    if np.sum(valid_mask) < 3:
        warnings.warn("Too few valid box sizes for reliable D estimation. Try adjusting min/max box sizes.")
    
    box_sizes_valid = box_sizes[valid_mask]
    counts_valid = counts[valid_mask]
    
    # Calculate fractal dimension
    D, r_squared, std_err, intercept = calculate_fractal_dimension(box_sizes_valid, counts_valid)
    
    # Prepare results
    results = {
        'D': D,
        'r_squared': r_squared,
        'std_error': std_err,
        'n_points': len(latitudes),
        'spatial_extent': {
            'lat_range': lat_range,
            'lon_range': lon_range
        }
    }
    
    if return_details:
        results.update({
            'box_sizes': box_sizes_valid,
            'counts': counts_valid,
            'intercept': intercept
        })
    
    return results


def analyze_csv(
    csv_path: str,
    lat_col: str = 'latitude',
    lon_col: str = 'longitude',
    **kwargs
) -> Dict:
    """
    Convenience function to analyze fractal dimension directly from CSV file.
    
    Parameters:
    -----------
    csv_path : str
        Path to CSV file containing earthquake data
    lat_col : str, optional (default='latitude')
        Name of latitude column
    lon_col : str, optional (default='longitude')
        Name of longitude column
    **kwargs : dict
        Additional arguments passed to box_counting()
        
    Returns:
    --------
    Dict : Results from box_counting()
    
    Example:
    --------
    >>> result = analyze_csv('query.csv')
    >>> print(f"Himalayan Fractal Dimension: {result['D']:.2f}")
    """
    # Load data
    data = pd.read_csv(csv_path)
    
    # Extract coordinates
    latitudes = data[lat_col].dropna().values
    longitudes = data[lon_col].dropna().values
    
    # Ensure equal length
    min_len = min(len(latitudes), len(longitudes))
    latitudes = latitudes[:min_len]
    longitudes = longitudes[:min_len]
    
    # Calculate fractal dimension
    return box_counting(latitudes, longitudes, **kwargs)


if __name__ == "__main__":
    """
    Example usage and testing
    """
    print("=" * 60)
    print("Seismic Fractal Dimension Analysis")
    print("=" * 60)
    
    # Test 1: Analyze Himalayan earthquakes
    print("\n1. Analyzing Himalayan earthquakes (query.csv)...")
    try:
        himalayan_results = analyze_csv('query.csv', return_details=True)
        print(f"   ✓ Fractal Dimension D = {himalayan_results['D']:.3f} ± {himalayan_results['std_error']:.3f}")
        print(f"   ✓ R² (goodness of fit) = {himalayan_results['r_squared']:.3f}")
        print(f"   ✓ Number of events = {himalayan_results['n_points']}")
        print(f"   ✓ Spatial extent: Lat {himalayan_results['spatial_extent']['lat_range']:.1f}°, Lon {himalayan_results['spatial_extent']['lon_range']:.1f}°")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 2: Analyze Andaman-Sumatra earthquakes
    print("\n2. Analyzing Andaman-Sumatra earthquakes (andaman_earthquakes.csv)...")
    try:
        andaman_results = analyze_csv('andaman_earthquakes.csv', return_details=True)
        print(f"   ✓ Fractal Dimension D = {andaman_results['D']:.3f} ± {andaman_results['std_error']:.3f}")
        print(f"   ✓ R² (goodness of fit) = {andaman_results['r_squared']:.3f}")
        print(f"   ✓ Number of events = {andaman_results['n_points']}")
        print(f"   ✓ Spatial extent: Lat {andaman_results['spatial_extent']['lat_range']:.1f}°, Lon {andaman_results['spatial_extent']['lon_range']:.1f}°")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)
