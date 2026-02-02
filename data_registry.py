"""
Data Registry for Seismic Fractal Analysis Dashboard
Manages analyzed datasets and their metadata
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

REGISTRY_FILE = "data_registry.json"

def load_registry() -> Dict:
    """Load the data registry from file."""
    if os.path.exists(REGISTRY_FILE):
        try:
            with open(REGISTRY_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"datasets": []}
    return {"datasets": []}

def save_registry(registry: Dict):
    """Save the data registry to file."""
    with open(REGISTRY_FILE, 'w') as f:
        json.dump(registry, f, indent=2)

def add_dataset(
    name: str,
    filepath: str,
    region: str,
    category: str,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    start_date: str,
    end_date: str,
    min_magnitude: float,
    event_count: int,
    fractal_d: Optional[float] = None,
    r_squared: Optional[float] = None,
    std_error: Optional[float] = None
):
    """Add a new dataset to the registry."""
    registry = load_registry()
    
    dataset = {
        "id": len(registry["datasets"]) + 1,
        "name": name,
        "filepath": filepath,
        "region": region,
        "category": category,
        "bounds": {
            "min_lat": min_lat,
            "max_lat": max_lat,
            "min_lon": min_lon,
            "max_lon": max_lon
        },
        "time_range": {
            "start": start_date,
            "end": end_date
        },
        "min_magnitude": min_magnitude,
        "event_count": event_count,
        "fractal_analysis": {
            "D": fractal_d,
            "r_squared": r_squared,
            "std_error": std_error
        },
        "created_at": datetime.now().isoformat()
    }
    
    registry["datasets"].append(dataset)
    save_registry(registry)
    return dataset

def get_all_datasets() -> List[Dict]:
    """Get all datasets from registry."""
    registry = load_registry()
    return registry.get("datasets", [])

def get_dataset_by_name(name: str) -> Optional[Dict]:
    """Get a specific dataset by name."""
    datasets = get_all_datasets()
    for ds in datasets:
        if ds["name"] == name:
            return ds
    return None

def update_dataset_analysis(name: str, fractal_d: float, r_squared: float, std_error: float):
    """Update fractal analysis results for a dataset."""
    registry = load_registry()
    for ds in registry["datasets"]:
        if ds["name"] == name:
            ds["fractal_analysis"] = {
                "D": fractal_d,
                "r_squared": r_squared,
                "std_error": std_error
            }
            save_registry(registry)
            return True
    return False

def delete_dataset(name: str):
    """Remove a dataset from registry."""
    registry = load_registry()
    registry["datasets"] = [ds for ds in registry["datasets"] if ds["name"] != name]
    save_registry(registry)

def generate_filename(region: str, category: str, start_date: str, end_date: str, is_custom: bool = False) -> str:
    """
    Generate a descriptive filename for downloaded data.
    
    Returns filename without extension (e.g., "Haiti_2010_Earthquake_2020-01-01_to_2026-02-02")
    """
    # Clean region name
    region_clean = region.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "-")
    
    # Shorten date format
    start_short = start_date[:10]  # YYYY-MM-DD
    end_short = end_date[:10]
    
    if is_custom:
        # For custom regions, use coordinates-based name
        return f"Custom_Region_{start_short}_to_{end_short}"
    else:
        # For presets, use region name
        return f"{region_clean}_{start_short}_to_{end_short}"
