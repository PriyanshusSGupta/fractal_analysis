# Dashboard Mockup Prompts for Napkin/Nano Banana

## Page 1: Overview & Comparison Page

### Prompt:
Create a modern web dashboard mockup for a seismic fractal analysis application. The page should have:

**Left Sidebar (dark blue-gray background)**:
- Logo/title "🌍 Navigation" at top
- Radio button menu with 4 options:
  * "📊 Overview & Comparison" (selected/highlighted)
  * "📈 Temporal Analysis"
  * "🔍 Fetch New Data"
  * "⚙️ Advanced Analysis"
- Info box showing "📊 Datasets Available: 3"
- Expandable section "📋 View Datasets" with 3 dataset names listed

**Main Content Area (white/light gray background)**:
- Header: Large blue text "🌍 Seismic Fractal Dimension Analysis V2"
- Subtitle: "Select Datasets to Compare"

- Two side-by-side dropdown selectors:
  * Left: "Dataset 1: [2010_Haiti_Earthquake ▼]"
  * Right: "Dataset 2: [Japan_Trench_Complete ▼]"

- Blue primary button: "🔍 Compare Datasets"

- Results section with 3 metric cards in a row:
  * Card 1: "📍 2010 Haiti" with large number "0.917" and smaller text "±0.045" and "R² = 0.869, 65 events"
  * Card 2: "📍 Japan Trench" with large number "1.532" and smaller text "±0.038" and "R² = 0.921, 1,245 events"
  * Card 3: "📊 Difference (ΔD)" with "0.615" and "67.1%" and "Japan Trench is more complex"

- Section titled "📍 Geographic Distribution" with two side-by-side placeholder maps:
  * Left map: Red dots scattered on light background labeled "2010 Haiti"
  * Right map: Blue dots scattered on light background labeled "Japan Trench"

- Section titled "📦 Box-Counting Analysis" with two side-by-side scatter plots showing log-log relationships with fitted lines

**Style**: Clean, modern, data science aesthetic with blue and orange accent colors, professional typography, subtle shadows on cards

---

## Page 2: Temporal Analysis Page

### Prompt:
Create a modern web dashboard mockup for temporal earthquake analysis. The page should have:

**Left Sidebar** (same as Page 1 but with "📈 Temporal Analysis" selected)

**Main Content Area**:
- Header: Large orange text "📈 Temporal Fractal Dimension Evolution"

- Section "🎯 Select Datasets for Temporal Analysis"
- Multi-select dropdown with checkboxes showing:
  * ☑ 2010_Haiti_Earthquake
  * ☑ Japan_Trench_Complete
  * ☐ Himalayas_Historical
  * ☐ Chile_Trench_2015

- Blue primary button: "📊 Analyze Temporal Evolution"

- Year range slider showing "Select year range: 2010 ━━━●━━━━━●━━━ 2026"

- Large line chart titled "Yearly Fractal Dimension Evolution":
  * Two colored lines (one red for Haiti, one blue for Japan)
  * X-axis: Years (2010-2026)
  * Y-axis: Fractal Dimension (D)
  * Error bars on data points
  * Legend showing dataset names
  * Gridlines and clean axes

- Section "📊 Statistical Summary" with 2 side-by-side cards:
  * Left card: "2010 Haiti" with metrics "Mean D: 0.921", "Std Dev: 0.084", "Total Events: 856"
  * Right card: "Japan Trench" with metrics "Mean D: 1.548", "Std Dev: 0.112", "Total Events: 12,450"

**Style**: Same clean design as Page 1, with emphasis on data visualization

---

## Page 3: Fetch New Data Page

### Prompt:
Create a modern web dashboard mockup for earthquake data fetching. The page should have:

**Left Sidebar** (same design but with "🔍 Fetch New Data" selected)

**Main Content Area**:
- Header: Large teal text "🔍 Fetch Earthquake Data"
- Subtitle: "Download earthquake data from USGS and calculate fractal dimension"

- Section "🌍 Region Selection":
  * Dropdown 1: "📂 Select Category: [⚡ Historic Major Earthquake Zones ▼]"
  * Dropdown 2: "🎯 Select Specific Region: [2010 Haiti ▼]"
  * Light blue info box: "2010 Haiti: M7.0 devastating"

- Section "📍 Geographic Boundaries":
  * Two columns of number inputs:
    - Left column: "Minimum Latitude: 17.50", "Maximum Latitude: 19.50"
    - Right column: "Minimum Longitude: -74.00", "Maximum Longitude: -72.00"

- Section "📅 Time Range":
  * Two date pickers side-by-side:
    - "Start Date: 2020-01-01"
    - "End Date: 2026-02-02"

- Section "⚙️ Filter Parameters":
  * Slider: "Minimum Magnitude: ▬▬▬●▬▬▬ 4.0"

- Gray info box showing: "📝 Output filename: `2010_Haiti_2020-01-01_to_2026-02-02.csv`"

- Large red primary button: "🚀 Fetch Data and Calculate D"

- Green success box showing: "✅ Data successfully downloaded! Downloaded 65 earthquakes"

- Section "📊 Analysis Results" with 3 metric cards:
  * "Fractal Dimension (D): 0.917 ±0.045"
  * "R² (Goodness of Fit): 0.869"
  * "Number of Events: 65"

**Style**: Form-focused design with clear sections, input fields, and success feedback

---

## Page 4: Advanced Analysis Page

### Prompt:
Create a modern web dashboard mockup for advanced earthquake analysis. The page should have:

**Left Sidebar** (same design but with "⚙️ Advanced Analysis" selected)

**Main Content Area**:
- Header: Large purple text "⚙️ Advanced Fractal Analysis"

- Section "📁 Select Dataset":
  * Radio buttons: "📊 From Registry (Fetched Datasets)" (selected) and "📤 Upload Custom File"
  * Dropdown: "Select Dataset: [2010_Haiti_2020-01-01_to_2026-02-02 ▼]"
  * Three info cards showing: "Region: 2010 Haiti", "Events: 65", "Global D: 0.917"

- Section "📍 Geographic Distribution":
  * Large interactive map placeholder showing purple dots representing earthquake locations
  * Map centered on Haiti region with coastlines visible
  * Caption: "Showing 65 earthquake epicenters"

- Section "📈 Temporal Analysis":
  * Line chart showing yearly fractal dimension over time (2020-2026)
  * Purple line with error bars
  * Title: "Yearly Fractal Dimension Evolution - 2010_Haiti_2020-01-01_to_2026-02-02"
  
  * Bar chart showing event count per year
  * Purple bars
  * Title: "Number of Earthquakes per Year"

- Section "🎛️ Box-Counting Parameters":
  * Three number inputs in a row:
    - "Minimum Box Size (deg): 0.1"
    - "Maximum Box Size (deg): 10.0"
    - Slider: "Number of Scales: 20"

- Purple primary button: "🔬 Perform Box-Counting Analysis"

- Section "📊 Results" with 4 metrics in a row:
  * "D: 0.9174"
  * "Std Error: 0.0451"
  * "R²: 0.8692"
  * "Events: 65"

- Section "📈 Box-Counting Log-Log Plot":
  * Scatter plot with purple points and orange dashed trend line
  * X-axis: "log₁₀(Box Size)"
  * Y-axis: "log₁₀(Box Count)"
  * Title showing D value and error

**Style**: Analysis-focused with emphasis on visualizations, purple accent color scheme

---

## General Design Guidelines for All Pages:

### Color Scheme:
- **Primary Blues**: #1f77b4 (main), #4a90e2 (light)
- **Accent Colors**: 
  * Orange: #ff7f0e
  * Purple: #9467bd
  * Teal: #17a2b8
  * Red: #dc3545
  * Green: #28a745
- **Backgrounds**: 
  * Sidebar: #2c3e50 (dark blue-gray)
  * Main: #ffffff (white)
  * Cards: #f8f9fa (light gray)
- **Text**: #333333 (dark gray)

### Typography:
- **Headers**: Bold, 2.5rem, blue
- **Subheaders**: Bold, 1.5rem, orange
- **Body**: Regular, 1rem, dark gray
- **Metrics**: Bold, 2rem for values, 1rem for labels

### Component Styles:
- **Buttons**: 
  * Primary: Blue background, white text, rounded corners
  * Hover: Slightly darker blue
  * Action buttons (red): For important actions
- **Cards**: 
  * Light gray background
  * Subtle shadow
  * Left border (5px) in accent color
  * Rounded corners
- **Info Boxes**:
  * Success: Light green background, green left border
  * Info: Light blue background, blue left border
  * Warning: Light yellow background, yellow left border
- **Dropdowns**: 
  * White background
  * Border: 1px solid light gray
  * Down arrow icon on right
- **Sliders**: 
  * Blue track and thumb
  * Gray background

### Layout:
- **Sidebar Width**: 250px
- **Main Content**: Remaining width with 2rem padding
- **Max Content Width**: 1400px centered
- **Spacing**: 1-2rem between sections
- **Grid**: 12-column responsive grid

### Icons:
Use emojis as shown in the prompts for a friendly, modern look

---

## Tips for Creating Mockups:

1. **Use these prompts directly** in Napkin AI, Figma AI, or similar tools
2. **Iterate**: Generate multiple versions and pick the best
3. **Consistency**: Keep sidebar and header consistent across all pages
4. **Real-ish Data**: Use the sample values provided for realistic look
5. **Export**: Save as PNG at 1920x1080 or higher resolution
6. **Presentations**: Great for project demos and documentation

---

## Example Use Case:

**For Project Report/Presentation**:
1. Generate all 4 page mockups
2. Add them to your presentation slides
3. Use to explain workflow before showing live demo
4. Helps reviewers understand UI before seeing real app

**For Documentation**:
1. Include mockups in README.md
2. Show expected interface design
3. Guide future developers/users

---

**Created**: February 2, 2026  
**Dashboard Version**: V2.0  
**Mockup Tool**: Napkin AI / Nano Banana / Figma AI Compatible
