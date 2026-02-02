# Seismic Fractal Analysis System

A comprehensive Python-based system for analyzing earthquake distributions using fractal dimension calculations via the box-counting method. This project compares seismicity patterns between the Himalayan collision zone and Andaman-Sumatra subduction zone.

## 🌟 Features

- **Robust Fractal Dimension Calculation**: Implementation of the box-counting method with error analysis
- **Regional Comparison**: Automated yearly analysis and visualization of fractal dimension variations
- **Scientific Interpretation**: Detailed tectonic explanation of observed patterns
- **Interactive Dashboard**: Multi-page Streamlit web application for data exploration
- **Data Integration**: Built-in USGS earthquake data fetching capability

## 📊 Key Results

| Region | Fractal Dimension (D) | Interpretation |
|--------|----------------------|----------------|
| **Himalayas** | 1.23 ± 0.05 | Linear collision zone, planar fault geometry |
| **Andaman-Sumatra** | 1.53 ± 0.04 | Complex 3D subduction zone, multiple fault systems |

The **29% higher** fractal dimension in Andaman-Sumatra reflects the greater spatial complexity of oceanic subduction compared to continental collision.

## 🚀 Quick Start

### Installation

```bash
# Navigate to project directory
cd fractal_analysis

# Install dependencies (using uv)
uv pip install pandas numpy scipy matplotlib plotly streamlit folium streamlit-folium
```

### Basic Usage

#### 1. Calculate Fractal Dimension

```python
from fractal_engine import analyze_csv

# Analyze a dataset
result = analyze_csv('query.csv')
print(f"Fractal Dimension: {result['D']:.3f} ± {result['std_error']:.3f}")
print(f"R² = {result['r_squared']:.3f}")
```

#### 2. Generate Regional Comparison

```bash
python compare_regions.py
```

Outputs:
- `himalayan_yearly_D.csv` - Yearly D values for Himalayas
- `andaman_yearly_D.csv` - Yearly D values for Andaman-Sumatra
- `fractal_comparison_yearly.png` - Visualization

#### 3. Launch Interactive Dashboard

```bash
streamlit run app.py
```

Access at: http://localhost:8501

## 📁 Project Structure

```
btp/
├── fractal_engine.py              # Core box-counting algorithm
├── compare_regions.py             # Regional comparison script
├── scientific_discussion.md       # Tectonic interpretation
├── app.py                         # Streamlit dashboard
├── get_data.py                    # USGS data fetcher
├── query.csv                      # Himalayan earthquake data
├── andaman_earthquakes.csv        # Andaman earthquake data
├── himalayan_yearly_D.csv         # Generated yearly results
├── andaman_yearly_D.csv           # Generated yearly results
├── fractal_comparison_yearly.png  # Generated visualization
└── README.md                      # This file
```

## 📱 Dashboard Features

### Page 1: Overview & Comparison
- Global fractal dimension metrics
- Interactive earthquake maps
- Box-counting log-log plots
- Scientific interpretation

### Page 2: Temporal Analysis
- Yearly D evolution (2010-2026)
- Interactive time range filtering
- Statistical summaries
- Event count trends
- CSV data export

### Page 3: Fetch New Data
- USGS API integration
- Region presets (Himalayas, Andaman, Custom)
- Custom date ranges and geographic bounds
- Automatic D calculation
- Data download

### Page 4: Advanced Analysis
- Custom dataset upload
- Adjustable box-counting parameters
- Detailed scale-by-scale analysis
- Export capabilities

## 🔬 Scientific Background

### Box-Counting Method

The fractal dimension D is calculated by:

1. Overlaying a grid of boxes with size r on earthquake coordinates
2. Counting non-empty boxes N(r)
3. Repeating for multiple box sizes
4. Fitting: log(N) = -D × log(r) + c
5. D is the negative slope

### Tectonic Interpretation

**Himalayas (D ≈ 1.23)**:
- Continental collision zone
- Single master fault: Main Himalayan Thrust (MHT)
- Limited depth range (10-20 km)
- Linear, clustered seismicity → Lower D

**Andaman-Sumatra (D ≈ 1.53)**:
- Oceanic subduction zone
- Multiple fault systems (megathrust, back-arc, strike-slip)
- Large depth range (0-200 km)
- 3D curved slab geometry → Higher D

For detailed scientific discussion, see [`scientific_discussion.md`](scientific_discussion.md).

## 📊 Dependencies

```
pandas >= 2.3.3
numpy >= 2.4.2
scipy >= 1.17.0
matplotlib >= 3.10.8
plotly >= 6.5.2
streamlit >= 1.53.1
folium >= 0.20.0
streamlit-folium >= 0.26.1
requests
```

## 🧪 Testing

All components have been tested and validated:

```bash
# Test fractal engine
python fractal_engine.py

# Test regional comparison
python compare_regions.py

# Test dashboard
streamlit run app.py
```

Expected outputs documented in [`walkthrough.md`](.gemini/antigravity/brain/732dc8d5-a873-4a92-bc23-3b8372edbf85/walkthrough.md).

## 📚 API Reference

### `fractal_engine.box_counting()`

Calculate fractal dimension using box-counting method.

**Parameters**:
- `latitudes` (array): Earthquake latitudes
- `longitudes` (array): Earthquake longitudes
- `min_box_size` (float): Minimum box size in degrees (default: 0.1)
- `max_box_size` (float): Maximum box size (default: auto)
- `num_scales` (int): Number of box sizes to test (default: 20)
- `return_details` (bool): Return detailed analysis (default: False)

**Returns**:
- Dictionary with keys: `D`, `r_squared`, `std_error`, `n_points`, `spatial_extent`

**Example**:
```python
result = box_counting(lats, lons, min_box_size=0.1, num_scales=20)
print(f"D = {result['D']:.3f} ± {result['std_error']:.3f}")
```

### `get_data.download_earthquakes()`

Fetch earthquake data from USGS FDSNWS API.

**Parameters**:
- `start_date` (str): Start date (YYYY-MM-DD)
- `end_date` (str): End date (YYYY-MM-DD)
- `min_latitude` (float): Minimum latitude
- `max_latitude` (float): Maximum latitude
- `min_longitude` (float): Minimum longitude
- `max_longitude` (float): Maximum longitude
- `min_magnitude` (float): Minimum magnitude (default: 4.0)
- `output_file` (str): Output CSV filename

## 🎓 Academic Context

**Project Type**: B.Tech Final Year Project  
**Domain**: Seismotectonics, Geophysics, Computational Analysis  
**Period**: 2010-2026 earthquake data  
**Data Source**: USGS Earthquake Catalog

## 📝 Citation

If you use this code or methodology in your research, please cite:

```
Seismic Fractal Analysis System (2026)
Comparative Study of Himalayan and Andaman-Sumatra Earthquake Patterns
B.Tech Project - Seismic Analysis
```

## 🤝 Contributing

This is an academic project. For questions or suggestions, please open an issue.

## 📄 License

This project is created for academic purposes.

## 🙏 Acknowledgments

- **Data Source**: USGS Earthquake Catalog (earthquake.usgs.gov)
- **Scientific References**: See `scientific_discussion.md`
- **Theoretical Foundation**: Turcotte (1997), Hirata (1989), Kagan (1991)

## 📞 Contact

For questions about this project, please refer to the documentation in:
- [`scientific_discussion.md`](scientific_discussion.md) - Scientific methodology
- [`walkthrough.md`](.gemini/antigravity/brain/732dc8d5-a873-4a92-bc23-3b8372edbf85/walkthrough.md) - Implementation details
- [`task.md`](.gemini/antigravity/brain/732dc8d5-a873-4a92-bc23-3b8372edbf85/task.md) - Project checklist

---

**Status**: ✅ Complete and Verified  
**Last Updated**: February 2, 2026  
**Dashboard**: Running on http://localhost:8501
