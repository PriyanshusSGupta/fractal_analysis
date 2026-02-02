# 🌍 Seismic Fractal Analysis Dashboard V2.0

A modern, interactive web application for analyzing earthquake distributions using fractal dimension calculations. Compare seismicity patterns across different tectonic regions with real-time data fetching from USGS.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.14-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.53.1-red)

## ✨ Features

### 🎯 Core Capabilities
- **Robust Fractal Dimension Calculation**: Advanced box-counting method with statistical error analysis
- **Real-time Data Fetching**: Direct integration with USGS Earthquake Catalog API
- **Interactive Visualization**: Dynamic maps with magnitude-based sizing and color coding
- **Dataset Management**: Built-in registry system for organizing and managing earthquake datasets
- **Multi-page Dashboard**: Clean, intuitive interface with 5 specialized pages

### 🗺️ Enhanced Visualizations
- **Magnitude-based Bubble Maps**: Earthquake markers scale with magnitude (M4.0 → 2px, M7.0 → 8px)
- **Color-coded Seismicity**: Red (M≥6.0), Orange (M≥5.0), Purple (M<5.0)
- **Interactive Folium Maps**: Zoom, pan, and explore earthquake distributions
- **Temporal Evolution Charts**: Track fractal dimension changes over time

### 🎨 Modern UI
- **Theme-aware Design**: Fully responsive in both Light and Dark modes
- **Professional Styling**: Custom CSS with metric cards, gradient effects, and smooth animations
- **Mobile-friendly**: Optimized layouts for all screen sizes

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/PriyanshusSGupta/fractal_analysis.git
cd fractal_analysis

# Install dependencies
pip install -r requirements.txt
```

### Launch Dashboard

```bash
streamlit run app_v2.py
```

Access at: **http://localhost:8501**

## 📱 Dashboard Pages

### 1️⃣ Overview & Comparison
- Compare fractal dimensions between two datasets
- Side-by-side geographic distribution maps
- Box-counting log-log regression plots
- Statistical metrics with professional card layouts

### 2️⃣ Temporal Analysis
- Multi-dataset yearly evolution tracking
- Interactive time period selection
- Fractal dimension trends over time
- Event count statistics and correlations

### 3️⃣ Fetch New Data
- **Region Presets**:
  - 🏔️ Himalayas (Nepal/India Border)
  - 🌊 Andaman-Sumatra Subduction Zone
  - 🏝️ Japan (Complete Archipelago)
  - 🗾 Tohoku Region
  - 🌴 Haiti (2010 Earthquake Region)
  - ✏️ Custom Region (Define your own bounds)
- Adjustable date ranges and magnitude thresholds
- Automatic fractal dimension calculation
- Smart filename generation

### 4️⃣ Advanced Analysis
- Upload custom CSV datasets
- Adjustable box-counting parameters (5-50 scales)
- Geographic distribution visualization
- Detailed scale-by-scale analysis tables
- Temporal fractal evolution within datasets

### 5️⃣ Manage Datasets
- View all registered datasets in a clean table
- Show metadata: region, events, time period, fractal D
- **Delete datasets** with two-step confirmation
- Automatic cleanup of CSV files and registry entries

## 🔬 Scientific Background

### Fractal Dimension Calculation

The fractal dimension **D** quantifies the spatial complexity of earthquake distributions:

**D ≈ 1.2**: Linear, clustered patterns (e.g., collision zones)  
**D ≈ 1.5-1.6**: Complex, 3D distributed patterns (e.g., subduction zones)  
**D ≈ 2.0**: Uniform planar distribution

### Box-Counting Method

1. Overlay a grid of boxes (size **r**) on earthquake coordinates
2. Count non-empty boxes **N(r)**
3. Repeat for multiple box sizes
4. Fit linear regression: **log(N) = -D × log(r) + c**
5. Extract **D** as the negative slope

### Example Results

| Region | Fractal D | Interpretation |
|--------|-----------|----------------|
| **Himalayas** | 1.23 ± 0.05 | Linear thrust fault, continental collision |
| **Andaman-Sumatra** | 1.53 ± 0.04 | Complex subduction, 3D slab geometry |
| **Japan** | 1.48 ± 0.06 | Multiple fault systems, volcanic arc |

## 📁 Project Structure

```
fractal_analysis/
├── app_v2.py                  # Main Streamlit dashboard
├── fractal_engine.py          # Box-counting algorithm
├── get_data.py                # USGS API integration
├── data_registry.py           # Dataset management system
├── requirements.txt           # Python dependencies
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── scientific_discussion.md   # Tectonic interpretation
├── REGION_PRESETS.md         # Geographic region reference
└── README.md                  # This file
```

## 🛠️ Technical Stack

**Core Libraries:**
- `streamlit` - Web application framework
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `scipy` - Statistical analysis
- `plotly` - Interactive visualizations
- `folium` - Geographic maps
- `streamlit-folium` - Folium-Streamlit integration

**APIs:**
- USGS FDSNWS Earthquake Catalog

## 📊 API Reference

### `fractal_engine.box_counting()`

```python
from fractal_engine import box_counting

result = box_counting(
    latitudes=earthquake_lats,
    longitudes=earthquake_lons,
    min_box_size=0.1,      # degrees
    num_scales=20,
    return_details=True
)

print(f"D = {result['D']:.3f} ± {result['std_error']:.3f}")
print(f"R² = {result['r_squared']:.3f}")
```

### `get_data.download_earthquakes()`

```python
from get_data import download_earthquakes

download_earthquakes(
    start_date="2020-01-01",
    end_date="2026-02-02",
    min_latitude=26.0,
    max_latitude=31.0,
    min_longitude=80.0,
    max_longitude=88.0,
    min_magnitude=4.0,
    output_file="nepal_earthquakes.csv"
)
```

## 🎓 Academic Context

**Project Type**: B.Tech Final Year Project  
**Domain**: Seismotectonics, Computational Geophysics  
**Data Period**: 2010-2026  
**Data Source**: USGS Earthquake Catalog

## 🚀 Deployment

### Streamlit Community Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository: `PriyanshusSGupta/fractal_analysis`
4. Set main file: `app_v2.py`
5. Deploy!

### Docker (Optional)

```dockerfile
FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app_v2.py"]
```

## 📝 Citation

If you use this code in your research:

```
Seismic Fractal Analysis Dashboard V2.0 (2026)
Comparative Study of Earthquake Patterns Using Box-Counting Method
B.Tech Project - Computational Seismology
https://github.com/PriyanshusSGupta/fractal_analysis
```

## 🙏 Acknowledgments

- **Data**: USGS Earthquake Catalog
- **Scientific Foundation**: Turcotte (1997), Hirata (1989), Kagan (1991)
- **Framework**: Streamlit Community

## 📄 License

Academic/Educational Use

---

**Status**: ✅ Production Ready  
**Version**: 2.0  
**Last Updated**: February 2, 2026  
**Live Demo**: Coming soon to Streamlit Community Cloud
