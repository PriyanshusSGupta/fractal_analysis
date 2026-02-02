# Dashboard V2 - New Features Guide

## 🎉 What's New in V2?

### 1. Smart Filename Generation ✅
**Problem Solved**: No more generic timestamped files!

- **For Presets**: Auto-generated from region name
  - Example: `2010_Haiti_2020-01-01_to_2026-02-02.csv`
  - Format: `{Region}_{StartDate}_to_{EndDate}.csv`

- **For Custom Regions**: You provide the name
  - Prompted to enter descriptive name
  - Example: `My_Study_Area_2020-01-01_to_2026-02-02.csv`

- **Filename Preview**: See the exact filename before downloading

### 2. Data Registry System ✅
**Problem Solved**: Fetched data now automatically available everywhere!

- **Automatic Registration**: Every fetched dataset is saved to registry
- **Metadata Tracked**:
  - Region name, category, bounds
  - Time range, magnitude filter
  - Event count
  - Fractal D, R², standard error
  - Creation timestamp

- **Persistent Storage**: `data_registry.json` stores all dataset info
- **Smart Migration**: Existing files (query.csv, andaman_earthquakes.csv) auto-registered on first run

### 3. Enhanced Advanced Analysis ✅
**New Features Added**:

- **📍 Geographic Distribution Map**
  - Interactive folium map showing earthquake locations
  - Color-coded by magnitude (if available)
  - Sample up to 1000 events for performance

- **📈 Temporal Analysis**
  - Yearly fractal dimension evolution chart
  - Event count per year bar chart
  - Error bars showing uncertainty

- **Two Data Sources**:
  1. **From Registry**: Select any fetched dataset from dropdown
  2. **Upload Custom**: Upload your own CSV file

- **📋 Enhanced Results**:
  - Detailed scale analysis table
  - Downloadable CSV export
  - Better visualizations

### 4. Dynamic Overview & Comparison ✅
**Problem Solved**: No more hard-coded datasets!

- **Empty by Default**: Clean start for new users
- **Dataset Selectors**: Two dropdowns to choose any datasets
- **Smart Warnings**:
  - Need 2 datasets minimum for comparison
  - Helpful guidance if <2 datasets available
  
- **Full Comparison**:
  - Side-by-side metrics
  - Dual maps
  - Box-counting plots
  - Difference calculations

### 5. Dynamic Temporal Analysis ✅
**Problem Solved**: Compare any datasets you want!

- **Multi-Select**: Choose 1 or more datasets
- **On-Demand Calculation**: Yearly D calculated when needed
- **Year Range Slider**: Focus on specific time period
- **Multi-Line Plots**: Compare trends across datasets
- **Statistical Summary**: Mean, std dev, total events per dataset

## 📁 File Structure

```
btp/
├── app.py                    # Original dashboard (still works!)
├── app_v2.py                 # NEW Enhanced dashboard
├── data_registry.py          # NEW Registry system
├── data_registry.json        # AUTO-GENERATED metadata storage
├── fractal_engine.py         # Unchanged
├── compare_regions.py        # Unchanged  
├── get_data.py               # Previously fixed
├── REGION_PRESETS.md         # Region reference
└── [dataset].csv files       # Your data
```

## 🚀 How to Run V2

### Start the New Dashboard:
```bash
streamlit run app_v2.py
```

**Or** to run on specific port:
```bash
streamlit run app_v2.py --server.port 8503
```

### Keep Both Running:
```bash
# Terminal 1: Original
streamlit run app.py --server.port 8501

# Terminal 2: New V2
streamlit run app_v2.py --server.port 8502
```

## 🎯 Quick User Guide

### First Time Use:
1. **Start Dashboard**: `streamlit run app_v2.py`
2. **Fetch Data**: Go to "🔍 Fetch New Data"
3. **Select Region**: Choose from 69+ presets
4. **Download**: Click "Fetch Data and Calculate D"
5. **Auto-Registered**: Dataset immediately available!

### Comparing Datasets:
1. **Fetch 2+ Datasets** using "Fetch New Data"
2. **Go to Overview**: Select "📊 Overview & Comparison"
3. **Choose Datasets**: Pick 2 from dropdowns
4. **Compare**: Click "Compare Datasets"
5. **View Results**: Maps, metrics, plots automatically generated

### Advanced Analysis:
1. **Go to Advanced**: Select "⚙️ Advanced Analysis"
2. **Choose Source**: "From Registry" or "Upload Custom"
3. **Select Dataset**: Pick from dropdown
4. **Automatic Maps**: Geographic distribution shown
5. **Temporal Charts**: Yearly D evolution displayed
6. **Custom Box-Counting**: Adjust parameters and reanalyze

### Temporal Evolution:
1. **Go to Temporal**: Select "📈 Temporal Analysis"
2. **Multi-Select**: Choose 1 or more datasets
3. **Analyze**: Click "Analyze Temporal Evolution"
4. **Filter Years**: Use slider to focus on range
5. **Compare Trends**: See all selected datasets on one chart

## 🆚 V1 vs V2 Comparison

| Feature | V1 (app.py) | V2 (app_v2.py) |
|---------|-------------|----------------|
| **Filenames** | Generic timestamps | Smart, descriptive names |
| **Data Persistence** | Manual file selection | Auto-registered, dropdown selection |
| **Overview Page** | Hard-coded (Himalaya/Andaman) | Dynamic (any 2 datasets) |
| **Temporal Page** | Hard-coded (Himalaya/Andaman) | Dynamic (any datasets) |
| **Advanced Maps** | ❌ Not included | ✅ Full geographic distribution |
| **Advanced Temporal** | ❌ Not included | ✅ Yearly D charts |
| **Dataset Count Display** | ❌ No | ✅ Shown in sidebar |
| **Registry System** | ❌ No | ✅ Full metadata tracking |
| **Custom Region Names** | ❌ No | ✅ User-provided names |
| **Migration** | N/A | ✅ Auto-registers existing CSVs |

## 💡 Tips & Best Practices

### Naming Custom Regions:
- Use descriptive names: `Southern_California`, `My_Research_Area`
- Avoid spaces (use underscores): `My_Area` not `My Area`
- Be specific: `Gujarat_2001_Aftershocks` better than `Study1`

### Dataset Management:
- **Registry Location**: `data_registry.json` in project folder
- **Edit Registry**: Edit JSON manually if needed (backup first!)
- **Delete Dataset**: Remove from registry + delete CSV file
- **Refresh**: Restart dashboard to reload registry

### Performance:
- **Large Datasets**: Maps sample 500-1000 events for speed
- **Many Datasets**: Registry handles 100+ datasets easily
- **Cache**: St.cache_data speeds up repeated analyses

### Troubleshooting:
- **Dataset Not Showing**: Check `data_registry.json` exists
- **Old Datasets Missing**: Run V2 once to auto-register
- **Wrong Coordinates**: Edit bounds in registry JSON
- **Duplicate Names**: Registry prevents duplicates

## 📊 Example Workflow

### Research Scenario: Compare Earthquake Zones

```
Day 1: Data Collection
→ Fetch "2011 Tohoku Region"
→ Fetch "2010 Haiti"  
→ Fetch "San Andreas (California)"

Day 2: Analysis
→ Overview: Compare Tohoku vs Haiti
  - Tohoku: D ≈ 1.5 (complex subduction)
  - Haiti: D ≈ 0.9 (simple strike-slip)
  
→ Temporal: All 3 datasets
  - See how D changes over years
  - Identify aftershock patterns

→ Advanced: Deep dive on Tohoku
  - Geographic clustering
  - Temporal evolution
  - Custom box-counting

Day 3: Report
→ Export all charts
→ Download scale analysis
→ Write conclusions
```

## 🔮 Future Enhancements (Ideas)

- **Bulk Delete**: Remove multiple datasets at once
- **Export Registry**: Download as CSV
- **Import Registry**: Share with collaborators
- **Favorite Datasets**: Star frequently used ones
- **Tags**: Categorize datasets (research, teaching, etc.)
- **Search**: Find datasets by name/region
- **Compare 3+**: More than 2 datasets in Overview

## 📞 Support

If you encounter issues:
1. Check `data_registry.json` is valid JSON
2. Verify CSV files have `latitude` and `longitude` columns
3. Restart Streamlit server
4. Check terminal for error messages

## ✅ Migration Checklist

- [x] `data_registry.py` created
- [x] `app_v2.py` created
- [x] Smart filename generation
- [x] Auto-registration system
- [x] Dynamic Overview page
- [x] Dynamic Temporal page
- [x] Enhanced Advanced Analysis
- [x] Maps in Advanced Analysis
- [x] Temporal charts in Advanced  
- [x] Multi-dataset selection
- [x] Existing file migration
- [x] Documentation complete

**Status**: ✅ **V2 READY FOR USE!**

---

**Last Updated**: February 2, 2026  
**Version**: 2.0  
**Compatibility**: Requires same dependencies as V1
