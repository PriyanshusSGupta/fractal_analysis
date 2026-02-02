# Dashboard Enhancement Implementation Plan

## Summary of Requested Changes

### 1. Smart Filename Generation ✅
**Current Issue**: Downloaded files have generic timestamps
**Solution**: 
- For **presets**: Auto-generate from region name (e.g., `2010_Haiti_2020-01-01_to_2026-02-02.csv`)
- For **custom regions**: Ask user for descriptive name or use coordinates

### 2. Enhanced Advanced Analysis Page
**Additions Needed**:
- Geographic distribution map (folium) showing earthquake locations
- Temporal analysis with yearly D calculations
- Better visualization similar to Overview page

### 3. Data Persistence & Management System
**Current Issue**: Fetched data not automatically available in other pages
**Solution**:
- Create `data_registry.py` - central registry tracking all analyzed datasets ✅
- Store metadata: name, filepath, region, bounds, dates, event count, D values
- Automatically register datasets when fetched
- Make registry available across all pages via session state

### 4. Dynamic Overview & Comparison Page
**Current Issue**: Hard-coded for Himalaya and Andaman only
**Solution**:
- Start with empty state or default presets
- Add dataset selector: dropdown to choose 2 datasets for comparison
- Dynamically load and compare any registered datasets
- Show message if <2 datasets available

### 5. Dynamic Temporal Analysis Page
**Current Issue**: Hard-coded for Himalaya and Andaman
**Solution**:
- Add dataset multi-selector
- Allow comparison of 1+ datasets
- Calculate yearly D on-demand or load from cache
- Dynamic plotting based on selected datasets

## Implementation Strategy

### Phase 1: Data Registry System
- [x] Create `data_registry.py` with JSON-based storage
- [ ] Integrate with Fetch Data page to auto-register
- [ ] Create helper UI functions for dataset selection

### Phase 2: Fetch Data Page Enhancement  
- [ ] Implement smart filename generation
- [ ] Add custom region naming dialog
- [ ] Auto-register fetched datasets
- [ ] Show success message with dataset name

### Phase 3: Advanced Analysis Enhancement
- [ ] Add geographic distribution map
- [ ] Add temporal D calculation
- [ ] Integrate with data registry for easy dataset loading
- [ ] Add dropdown to select from fetched datasets

### Phase 4: Overview Page Refactor
- [ ] Remove hard-coded data loading
- [ ] Add dual dataset selector UI
- [ ] Make comparison dynamic
- [ ] Handle edge cases (0, 1, or 2+ datasets)

### Phase 5: Temporal Analysis Refactor
- [ ] Add multi-dataset selector
- [ ] Dynamic yearly D calculation
- [ ] Update plots to handle variable datasets
- [ ] Maintain year range selector

## File Structure Changes

```
btp/
├── app.py (MODIFIED - major refactor)
├── data_registry.py (NEW)
├── data_registry.json (AUTO-GENERATED)
├── fractal_engine.py (unchanged)
├── compare_regions.py (unchanged)
├── get_data.py (unchanged - already fixed)
└── [dataset files].csv
```

## Key Technical Details

### Data Registry Schema
```json
{
  "datasets": [
    {
      "id": 1,
      "name": "2010_Haiti_2020-01-01_to_2026-02-02",
      "filepath": "2010_Haiti_2020-01-01_to_2026-02-02.csv",
      "region": "2010 Haiti",
      "category": "Historic Major Earthquake Zones",
      "bounds": {...},
      "time_range": {...},
      "event_count": 65,
      "fractal_analysis": {
        "D": 0.917,
        "r_squared": 0.869,
        "std_error": 0.045
      },
      "created_at": "2026-02-02T14:30:00"
    }
  ]
}
```

### Session State Management
Use Streamlit's `st.session_state` to:
- Cache loaded datasets
- Store selected comparisons
- Persist user choices across reruns

## UI/UX Improvements

### Fetch Data Page
- Show filename preview before download
- Success message: "Dataset '2010_Haiti...' saved and ready for analysis!"
- Link to Advanced Analysis page

### Overview Page (New Design)
```
[Compare Datasets]
Dataset 1: [Dropdown: Select dataset...]
Dataset 2: [Dropdown: Select dataset...]
[Compare Button]

[Results display area]
```

### Advanced Analysis Page (Enhanced)
```
[Select Dataset]
Source: [Fetched Datasets ▼] | [Upload Custom ▼]
Dataset: [2010_Haiti... ▼]

[Geographic Distribution Map]
[Temporal Analysis Charts]
[Box-Counting Parameters]
[Results]
```

## Testing Checklist
- [ ] Fetch data with preset → auto-named file
- [ ] Fetch custom region → prompted for name
- [ ] Dataset appears in registry
- [ ] Can select dataset in Advanced Analysis
- [ ] Can compare 2 datasets in Overview
- [ ] Temporal analysis works with selected datasets
- [ ] Maps render correctly
- [ ] No hard-coded datasets remain

## Migration Notes

**Backward Compatibility**:
- Existing `query.csv` and `andaman_earthquakes.csv` should be auto-registered on first run
- Create migration function to scan directory for CSV files and add to registry

**User Communication**:
- Add info box explaining new data management system  
- Show count of available datasets in sidebar
