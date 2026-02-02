"""
Enhanced Seismic Fractal Analysis Dashboard V2
Multi-page Streamlit application with dynamic data management

New Features:
- Smart filename generation
- Data registry tracking all analyzed datasets
- Dynamic dataset selection across all pages
- Enhanced Advanced Analysis with maps and temporal charts

Author: Seismic Analysis Team
Date: February 2026
Version: 2.0
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import folium_static
from datetime import datetime, timedelta
import os
import glob

# Import our custom modules
from fractal_engine import box_counting
from get_data import download_earthquakes
from data_registry import (
    load_registry, add_dataset, get_all_datasets, 
    generate_filename, update_dataset_analysis
)

# Page configuration
st.set_page_config(
    page_title="Seismic Fractal Analysis V2",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS matching the mockup
st.markdown("""
<style>
    /* Global Settings - Adaptive to Theme */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling - Constant Dark */
    [data-testid="stSidebar"] {
        background-color: #1e2530;
    }
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] div, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h2 {
        color: white !important;
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }
    [data-testid="stSidebarNav"] {
        background-color: #1e2530;
    }
    
    /* Main Content Background - Theme Aware */
    .stApp {
        background-color: var(--background-color);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1f77b4; /* Brighter blue for visibility */
        font-weight: 700;
    }
    
    /* Metric Cards - Theme Aware */
    .metric-card-container {
        background-color: var(--secondary-background-color);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-top: 4px solid #ccc;
        height: 100%;
        color: var(--text-color);
    }
    
    .card-blue { border-top-color: #1f77b4; }
    .card-orange { border-top-color: #ff7f0e; }
    .card-purple { border-top-color: #9467bd; }
    .card-red { border-top-color: #d62728; }
    .card-green { border-top-color: #2ca02c; }
    .card-teal { border-top-color: #17a2b8; }
    
    .metric-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-color);
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 5px;
    }
    
    .value-blue { color: #1f77b4; }
    .value-orange { color: #ff7f0e; }
    .value-purple { color: #9467bd; }
    .value-red { color: #d62728; }
    .value-green { color: #2ca02c; }
    .value-teal { color: #17a2b8; }
    
    .metric-sub {
        font-size: 0.85rem;
        color: var(--text-color);
        opacity: 0.8;
        line-height: 1.4;
    }
    
    /* Content Containers - Theme Aware */
    .content-box {
        background-color: var(--secondary-background-color);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 20px;
        margin-bottom: 20px;
        color: var(--text-color);
    }
    
    /* Section Headers in Containers */
    .box-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-color);
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Selectboxes and Labels - Theme Aware */
    .stSelectbox label, .stRadio label, .stNumberInput label {
        color: var(--text-color) !important;
        font-weight: 600;
    }
    
    /* Main Headers forced visibility */
    .main-header {
        color: var(--text-color) !important;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #1f77b4;
        color: white !important;
        font-weight: 600;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #165a8c;
        color: white !important;
    }
    
    /* Custom Alert Boxes (Info/Status) - Theme Aware */
    .info-box {
        background-color: var(--secondary-background-color);
        padding: 12px 15px;
        border-radius: 6px;
        border-left: 5px solid #17a2b8;
        margin: 10px 0;
        color: var(--text-color);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .filename-box {
        background-color: var(--secondary-background-color);
        padding: 10px;
        border-radius: 5px;
        font-family: monospace;
        color: var(--text-color);
        border: 1px solid #ced4da;
        margin-bottom: 10px;
    }
    
    .registry-info {
        background-color: #2c3e50; /* Keep dark as it was intended as a dark feature */
        padding: 10px;
        border-radius: 8px;
        color: white;
        border: 1px solid #3e5060;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'datasets_loaded' not in st.session_state:
    st.session_state.datasets_loaded = False
    st.session_state.available_datasets = []

# Load datasets from registry
def refresh_datasets():
    """Refresh the list of available datasets."""
    datasets = get_all_datasets()
    st.session_state.available_datasets = datasets
    st.session_state.datasets_loaded = True
    return datasets

# Auto-register existing CSV files on first run
def auto_register_existing_files():
    """Scan directory for CSV files and add to registry if not present."""
    registry = load_registry()
    existing_names = [ds['name'] for ds in registry.get('datasets', [])]
    
    # Known datasets to register
    known_files = [
        {'file': 'query.csv', 'name': 'Himalayas_Historical', 'region': 'Himalayas', 'category': 'Continental Collision Zones'},
        {'file': 'andaman_earthquakes.csv', 'name': 'Andaman-Sumatra_Historical', 'region': 'Andaman-Sumatra', 'category': 'Major Subduction Zones'}
    ]
    
    for kf in known_files:
        if os.path.exists(kf['file']) and kf['name'] not in existing_names:
            try:
                df = pd.read_csv(kf['file'])
                add_dataset(
                    name=kf['name'],
                    filepath=kf['file'],
                    region=kf['region'],
                    category=kf['category'],
                    min_lat=df['latitude'].min(),
                    max_lat=df['latitude'].max(),
                    min_lon=df['longitude'].min(),
                    max_lon=df['longitude'].max(),
                    start_date=df['time'].min() if 'time' in df.columns else "Unknown",
                    end_date=df['time'].max() if 'time' in df.columns else "Unknown",
                    min_magnitude=df['mag'].min() if 'mag' in df.columns else 0,
                    event_count=len(df)
                )
            except:
                pass

# Run auto-registration
auto_register_existing_files()
available_datasets = refresh_datasets()

# Sidebar matching mockup
with st.sidebar:
    st.markdown("## 🌍 Navigation")
    
    page = st.radio(
        "",
        ["📊 Overview & Comparison", "📈 Temporal Analysis", "🔍 Fetch New Data", "⚙️ Advanced Analysis"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Dataset counter styled like mockup
    st.markdown(f"""
    <div style="background-color: #2c3e50; padding: 10px; border-radius: 8px; color: white; border: 1px solid #3e5060; margin-bottom: 20px;">
        <span style="color: #4CAF50; font-size: 1.2rem;">📊</span> 
        <span style="font-weight: 600;">Datasets Available: {len(available_datasets)}</span>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📋 View Datasets", expanded=True):
        if len(available_datasets) > 0:
            for idx, ds in enumerate(available_datasets[:5]):
                st.caption(f"{idx+1}. {ds['name']}")
            if len(available_datasets) > 5:
                st.caption(f"...and {len(available_datasets)-5} more")
        else:
            st.caption("No datasets yet")

# Helper functions
@st.cache_data
def load_dataset(filepath):
    """Load earthquake data from CSV."""
    df = pd.read_csv(filepath)
    if 'time' in df.columns:
        df['timestamp'] = pd.to_datetime(df['time'])
        df['year'] = df['timestamp'].dt.year
    return df

@st.cache_data
def calculate_fractal_d(latitudes, longitudes):
    """Calculate fractal dimension."""
    return box_counting(latitudes, longitudes, return_details=True)

@st.cache_data
def calculate_yearly_d(df, name):
    """Calculate yearly fractal dimensions."""
    if 'year' not in df.columns:
        return None
    
    results = []
    years = sorted(df['year'].unique())
    
    for year in years:
        year_data = df[df['year'] == year]
        if len(year_data) >= 10:
            try:
                result = box_counting(
                    year_data['latitude'].values,
                    year_data['longitude'].values,
                    min_box_size=0.1,
                    num_scales=15
                )
                results.append({
                    'year': year,
                    'D': result['D'],
                    'std_error': result['std_error'],
                    'r_squared': result['r_squared'],
                    'n_events': result['n_points']
                })
            except:
                pass
    
    return pd.DataFrame(results) if results else None


# ========================================
# PAGE 1: Overview & Comparison
# ========================================
# ========================================
# PAGE 1: Overview & Comparison
# ========================================
if page == "📊 Overview & Comparison":
    # Custom Header
    st.markdown('<div class="main-header">🌍 Seismic Fractal Dimension Analysis V2</div>', unsafe_allow_html=True)
    
    if len(available_datasets) < 2:
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown(f"""
        **⚠️ Comparison Requires 2 Datasets**
        
        Currently available: {len(available_datasets)} dataset(s)
        
        To use this page:
        1. Go to **"🔍 Fetch New Data"** page
        2. Download earthquake data for different regions
        3. Return here to compare them
        
        Or use **"⚙️ Advanced Analysis"** to analyze individual datasets.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if len(available_datasets) == 1:
            st.info(f"💡 You have 1 dataset ({available_datasets[0]['name']}). Fetch one more to enable comparison!")
    else:
        st.markdown("### 🎯 Select Datasets to Compare")
        
        col1, col2 = st.columns(2)
        dataset_names = [ds['name'] for ds in available_datasets]
        
        with col1:
            ds1_name = st.selectbox("Dataset 1:", dataset_names, key='ds1')
        with col2:
            ds2_name = st.selectbox("Dataset 2:", dataset_names, index=min(1, len(dataset_names)-1), key='ds2')
            
        # Full width button using columns to center or stretch
        if st.button("🔍 Compare Datasets", type="primary", use_container_width=True):
            if ds1_name == ds2_name:
                st.error("Please select two different datasets.")
            else:
                # Load logic
                ds1 = next(ds for ds in available_datasets if ds['name'] == ds1_name)
                ds2 = next(ds for ds in available_datasets if ds['name'] == ds2_name)
                
                data1 = load_dataset(ds1['filepath'])
                data2 = load_dataset(ds2['filepath'])
                
                res1 = calculate_fractal_d(data1['latitude'], data1['longitude'])
                res2 = calculate_fractal_d(data2['latitude'], data2['longitude'])
                
                # Metrics Row with Custom Cards
                cols = st.columns(3)
                
                # Diff calculation
                diff = res2['D'] - res1['D']
                pct = abs(diff / res1['D']) * 100
                comparison_text = f"{ds2['region']} is more complex" if diff > 0 else f"{ds1['region']} is more complex"
                
                with cols[0]:
                    st.markdown(f"""
                    <div class="metric-card-container card-blue">
                        <div class="metric-title">📍 {ds1['region']}</div>
                        <div class="metric-value value-blue">{res1['D']:.3f}</div>
                        <div class="metric-sub">
                            ±{res1['std_error']:.3f} (Error Est.)<br>
                            R² = {res1['r_squared']:.3f}, {res1['n_points']} events
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with cols[1]:
                    st.markdown(f"""
                    <div class="metric-card-container card-orange">
                        <div class="metric-title">📍 {ds2['region']}</div>
                        <div class="metric-value value-orange">{res2['D']:.3f}</div>
                        <div class="metric-sub">
                            ±{res2['std_error']:.3f} (Error Est.)<br>
                            R² = {res2['r_squared']:.3f}, {res2['n_points']} events
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with cols[2]:
                    st.markdown(f"""
                    <div class="metric-card-container card-purple">
                        <div class="metric-title">📊 Difference (ΔD)</div>
                        <div class="metric-value value-purple">{abs(diff):.3f}</div>
                        <div class="metric-sub">
                            {pct:.1f}% relative diff.<br>
                            {comparison_text}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Maps Container
                st.markdown('<div class="content-box">', unsafe_allow_html=True)
                st.markdown('<div class="box-header">📍 Geographic Distribution</div>', unsafe_allow_html=True)
                
                mcols = st.columns(2)
                with mcols[0]:
                    st.markdown(f"**{ds1['region']}**")
                    center1 = [data1['latitude'].mean(), data1['longitude'].mean()]
                    map1 = folium.Map(location=center1, zoom_start=5, height=300)
                    # Add sample points
                    sample1 = data1.sample(min(500, len(data1)))
                    for _, r in sample1.iterrows():
                        folium.CircleMarker([r['latitude'], r['longitude']], radius=2, color='#1f77b4', fill=True).add_to(map1)
                    folium_static(map1, width=None, height=300)
                    
                with mcols[1]:
                    st.markdown(f"**{ds2['region']}**")
                    center2 = [data2['latitude'].mean(), data2['longitude'].mean()]
                    map2 = folium.Map(location=center2, zoom_start=5, height=300)
                    sample2 = data2.sample(min(500, len(data2)))
                    for _, r in sample2.iterrows():
                        folium.CircleMarker([r['latitude'], r['longitude']], radius=2, color='#ff7f0e', fill=True).add_to(map2)
                    folium_static(map2, width=None, height=300)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Box Counting Container
                st.markdown('<div class="content-box">', unsafe_allow_html=True)
                st.markdown('<div class="box-header">📦 Box-Counting Analysis</div>', unsafe_allow_html=True)
                
                fig = make_subplots(rows=1, cols=2, subplot_titles=(f"{ds1['region']}: Log-Log Plot", f"{ds2['region']}: Log-Log Plot"))
                
                # Plot 1
                log_r1, log_N1 = np.log10(res1['box_sizes']), np.log10(res1['counts'])
                fig.add_trace(go.Scatter(x=log_r1, y=log_N1, mode='markers', marker=dict(color='#1f77b4'), name=ds1['region']), row=1, col=1)
                z1 = np.polyfit(log_r1, log_N1, 1)
                fig.add_trace(go.Scatter(x=log_r1, y=np.poly1d(z1)(log_r1), mode='lines', line=dict(color='#1f77b4'), name='Fit'), row=1, col=1)
                fig.add_annotation(x=log_r1[-1], y=log_N1[-1], text=f"D={-z1[0]:.3f}", showarrow=False, font=dict(color='#1f77b4'), row=1, col=1)

                # Plot 2
                log_r2, log_N2 = np.log10(res2['box_sizes']), np.log10(res2['counts'])
                fig.add_trace(go.Scatter(x=log_r2, y=log_N2, mode='markers', marker=dict(color='#ff7f0e'), name=ds2['region']), row=1, col=2)
                z2 = np.polyfit(log_r2, log_N2, 1)
                fig.add_trace(go.Scatter(x=log_r2, y=np.poly1d(z2)(log_r2), mode='lines', line=dict(color='#ff7f0e'), name='Fit'), row=1, col=2)
                fig.add_annotation(x=log_r2[-1], y=log_N2[-1], text=f"D={-z2[0]:.3f}", showarrow=False, font=dict(color='#ff7f0e'), row=1, col=2)
                
                fig.update_layout(height=400, showlegend=False, margin=dict(l=20, r=20, t=40, b=20))
                fig.update_xaxes(title_text="log(Box Size)")
                fig.update_yaxes(title_text="log(Count)")
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)


# ========================================
# PAGE 2: Temporal Analysis
# ========================================
# ========================================
# PAGE 2: Temporal Analysis
# ========================================
elif page == "📈 Temporal Analysis":
    # Custom Header
    st.markdown('<div class="main-header" style="color: #e67e22;">📈 Temporal Fractal Dimension Evolution</div>', unsafe_allow_html=True)
    
    if len(available_datasets) == 0:
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("""
        **⚠️ No Datasets Available**
        
        Go to **"🔍 Fetch New Data"** to download earthquake data first.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="box-header">🎯 Select Datasets for Temporal Analysis</div>', unsafe_allow_html=True)
        
        dataset_names = [ds['name'] for ds in available_datasets]
        
        selected_datasets = st.multiselect(
            "Choose one or more datasets:",
            dataset_names,
            default=[dataset_names[0]] if len(dataset_names) > 0 else [],
            label_visibility="collapsed"
        )
        
        if len(selected_datasets) == 0:
            st.info("👆 Select at least one dataset to begin analysis")
        elif st.button("📊 Analyze Temporal Evolution", type="primary", use_container_width=True):
            with st.spinner("Analyzing datasets..."):
                datasets_analysis = []
                
                # Pre-defined colors for consistency
                colors = ['#d62728', '#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd']
                
                for idx, ds_name in enumerate(selected_datasets):
                    ds = next(d for d in available_datasets if d['name'] == ds_name)
                    data = load_dataset(ds['filepath'])
                    yearly_df = calculate_yearly_d(data, ds_name)
                    
                    if yearly_df is not None and len(yearly_df) > 0:
                        datasets_analysis.append({
                            'name': ds['region'],
                            'data': yearly_df,
                            'color': colors[idx % len(colors)],
                            'total_events': ds['event_count']
                        })
            
            if len(datasets_analysis) == 0:
                st.error("❌ No temporal data available for selected datasets")
            else:
                # Time range selector
                all_years = []
                for da in datasets_analysis:
                    all_years.extend(da['data']['year'].tolist())
                
                min_year = int(min(all_years))
                max_year = int(max(all_years))
                
                st.markdown("<br>", unsafe_allow_html=True)
                year_range = st.slider(
                    "Select year range:",
                    min_year, max_year, (min_year, max_year)
                )
                
                # Main plot in Content Box
                st.markdown('<div class="content-box">', unsafe_allow_html=True)
                st.markdown('<div class="box-header" style="text-align: center; justify-content: center;">Yearly Fractal Dimension Evolution</div>', unsafe_allow_html=True)
                
                fig = go.Figure()
                
                for da in datasets_analysis:
                    filtered = da['data'][(da['data']['year'] >= year_range[0]) & 
                                         (da['data']['year'] <= year_range[1])]
                    
                    fig.add_trace(go.Scatter(
                        x=filtered['year'], y=filtered['D'],
                        error_y=dict(type='data', array=filtered['std_error']),
                        mode='markers+lines',
                        name=da['name'],
                        marker=dict(size=8, color=da['color']),
                        line=dict(width=2, color=da['color'])
                    ))
                
                fig.update_layout(
                    xaxis_title="Years",
                    yaxis_title="Fractal Dimension (D)",
                    hovermode='x unified',
                    height=400,
                    margin=dict(l=20, r=20, t=20, b=20),
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Statistics with Custom Cards matching Mockup
                st.markdown("### 📊 Statistical Summary")
                
                cols = st.columns(len(datasets_analysis))
                for idx, da in enumerate(datasets_analysis):
                    with cols[idx]:
                        filtered = da['data'][(da['data']['year'] >= year_range[0]) & 
                                             (da['data']['year'] <= year_range[1])]
                        mean_d = filtered['D'].mean()
                        std_dev = filtered['D'].std()
                        total_events = filtered['n_events'].sum()
                        
                        # Determine card color based on assigned plot color
                        color_hex = da['color']
                        card_class = "card-blue" # Default
                        val_class = "value-blue"
                        
                        if color_hex == '#d62728': # Red
                            card_class = "card-red"
                            val_class = "value-red"
                        elif color_hex == '#ff7f0e': # Orange
                            card_class = "card-orange"
                            val_class = "value-orange"
                        elif color_hex == '#9467bd': # Purple
                            card_class = "card-purple"
                            val_class = "value-purple"
                        elif color_hex == '#2ca02c': # Green
                            card_class = "card-green"
                            val_class = "value-green"
                        
                        # Mockup-style card
                        st.markdown(f"""
                        <div class="metric-card-container {card_class}">
                            <div class="metric-title">
                                <span>📍</span> {da['name']}
                            </div>
                            <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                                <div>
                                    <div style="font-size: 0.85rem; color: #666; font-weight: 600;">Mean D:</div>
                                    <div class="metric-value {val_class}" style="font-size: 1.8rem;">{mean_d:.3f}</div>
                                </div>
                                <div style="border-left: 1px solid #eee; margin: 0 10px;"></div>
                                <div>
                                    <div style="font-size: 0.85rem; color: #666; font-weight: 600;">Std Dev:</div>
                                    <div class="metric-value {val_class}" style="font-size: 1.8rem;">{std_dev:.3f}</div>
                                </div>
                                <div style="border-left: 1px solid #eee; margin: 0 10px;"></div>
                                <div>
                                    <div style="font-size: 0.85rem; color: #666; font-weight: 600;">Total Events:</div>
                                    <div class="metric-value {val_class}" style="font-size: 1.8rem;">{total_events:,}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)


# ========================================
# PAGE 3: Fetch New Data
# ========================================
# ========================================
# PAGE 3: Fetch New Data
# ========================================
elif page == "🔍 Fetch New Data":
    # Custom Header
    st.markdown('<div class="main-header" style="color: #17a2b8;">🔍 Fetch Earthquake Data</div>', unsafe_allow_html=True)
    st.markdown("### Download earthquake data from USGS and calculate fractal dimension")
    
    # Region presets (keeping the existing comprehensive list)
    REGION_PRESETS = {
        "🌋 Major Subduction Zones": {
            "Andaman-Sumatra": {"lat": (-5.0, 10.0), "lon": (92.0, 100.0), "desc": "Indian Ocean megathrust"},
            "Japan Trench": {"lat": (30.0, 45.0), "lon": (135.0, 147.0), "desc": "Pacific-Philippine subduction"},
            "Cascadia": {"lat": (40.0, 50.0), "lon": (-130.0, -121.0), "desc": "Juan de Fuca subduction"},
            "Alaska-Aleutian": {"lat": (50.0, 65.0), "lon": (-180.0, -130.0), "desc": "Pacific-North American"},
            "Chile Trench": {"lat": (-45.0, -17.0), "lon": (-76.0, -66.0), "desc": "Nazca-South American"},
            "Peru-Ecuador": {"lat": (-18.0, 2.0), "lon": (-82.0, -75.0), "desc": "Andean subduction"},
            "Tonga-Kermadec": {"lat": (-37.0, -15.0), "lon": (-180.0, -173.0), "desc": "Pacific-Australian"},
            "Kamchatka": {"lat": (50.0, 61.0), "lon": (155.0, 167.0), "desc": "Pacific-Okhotsk"},
            "Central America": {"lat": (8.0, 18.0), "lon": (-95.0, -83.0), "desc": "Cocos-Caribbean subduction"},
            "Philippines": {"lat": (5.0, 21.0), "lon": (118.0, 127.0), "desc": "Philippine Mobile Belt"},
            "Solomon Islands": {"lat": (-12.0, -5.0), "lon": (154.0, 163.0), "desc": "Pacific-Australian"},
            "New Zealand": {"lat": (-47.0, -34.0), "lon": (165.0, 179.0), "desc": "Hikurangi subduction"},
        },
        
        "⛰️ Continental Collision Zones": {
            "Himalayas": {"lat": (26.0, 36.0), "lon": (70.0, 95.0), "desc": "India-Eurasia collision"},
            "Zagros Mountains (Iran)": {"lat": (25.0, 39.0), "lon": (44.0, 58.0), "desc": "Arabia-Eurasia"},
            "Alps-Apennines": {"lat": (42.0, 48.0), "lon": (5.0, 15.0), "desc": "Africa-Eurasia"},
            "Caucasus": {"lat": (38.0, 44.0), "lon": (38.0, 50.0), "desc": "Arabia-Eurasia"},
            "Hindu Kush": {"lat": (34.0, 38.0), "lon": (68.0, 73.0), "desc": "Deep intermediate-depth"},
            "Papua New Guinea": {"lat": (-11.0, -2.0), "lon": (140.0, 152.0), "desc": "Australia-Pacific"},
        },
        
        "🔀 Transform Fault Systems": {
            "San Andreas (California)": {"lat": (32.0, 40.0), "lon": (-123.0, -115.0), "desc": "Right-lateral strike-slip"},
            "North Anatolian (Turkey)": {"lat": (38.0, 42.0), "lon": (26.0, 45.0), "desc": "Right-lateral strike-slip"},
            "Dead Sea Transform": {"lat": (29.0, 38.0), "lon": (34.0, 39.0), "desc": "Left-lateral strike-slip"},
            "Alpine Fault (New Zealand)": {"lat": (-46.0, -42.0), "lon": (168.0, 172.0), "desc": "Oblique strike-slip"},
            "Sagaing Fault (Myanmar)": {"lat": (16.0, 26.0), "lon": (94.0, 98.0), "desc": "Right-lateral"},
            "Great Sumatra Fault": {"lat": (-6.0, 6.0), "lon": (95.0, 102.0), "desc": "Right-lateral strike-slip"},
        },
        
        "🌊 Mid-Ocean Ridges": {
            "East Pacific Rise": {"lat": (-55.0, 25.0), "lon": (-115.0, -100.0), "desc": "Fast-spreading ridge"},
            "Mid-Atlantic Ridge (N)": {"lat": (0.0, 60.0), "lon": (-45.0, -10.0), "desc": "Slow-spreading"},
            "Mid-Atlantic Ridge (S)": {"lat": (-60.0, 0.0), "lon": (-40.0, 20.0), "desc": "Slow-spreading"},
            "Southwest Indian Ridge": {"lat": (-55.0, -25.0), "lon": (20.0, 70.0), "desc": "Ultra-slow spreading"},
            "Red Sea Rift": {"lat": (12.0, 30.0), "lon": (32.0, 43.0), "desc": "Continental rifting"},
        },
        
        "🏔️ Rift Valleys": {
            "East African Rift": {"lat": (-15.0, 15.0), "lon": (28.0, 42.0), "desc": "Continental rift"},
            "Baikal Rift (Russia)": {"lat": (50.0, 56.0), "lon": (103.0, 112.0), "desc": "Intercontinental rift"},
            "Basin and Range (USA)": {"lat": (31.0, 42.0), "lon": (-120.0, -107.0), "desc": "Extensional province"},
            "Rhine Graben": {"lat": (47.0, 51.0), "lon": (7.0, 9.0), "desc": "Continental rift"},
        },
        
        "🔥 Volcanic Arcs": {
            "Ring of Fire (Pacific)": {"lat": (-60.0, 60.0), "lon": (100.0, -60.0), "desc": "Circum-Pacific belt"},
            "Indonesian Arc": {"lat": (-12.0, 6.0), "lon": (95.0, 135.0), "desc": "Volcanic island arc"},
            "Aleutian Arc": {"lat": (51.0, 55.0), "lon": (-180.0, -160.0), "desc": "Volcanic arc"},
            "Lesser Antilles": {"lat": (12.0, 19.0), "lon": (-62.0, -60.0), "desc": "Caribbean volcanic arc"},
            "Mariana Arc": {"lat": (11.0, 25.0), "lon": (140.0, 148.0), "desc": "Deepest trench"},
        },
        
        "🌍 Countries & Regions": {
            "Japan (Complete)": {"lat": (24.0, 46.0), "lon": (122.0, 148.0), "desc": "Island arc nation"},
            "California (USA)": {"lat": (32.0, 42.0), "lon": (-125.0, -114.0), "desc": "Transform margin"},
            "Alaska (USA)": {"lat": (54.0, 71.0), "lon": (-170.0, -130.0), "desc": "Subduction zone"},
            "Italy": {"lat": (36.0, 47.0), "lon": (6.0, 19.0), "desc": "Collision + subduction"},
            "Greece": {"lat": (34.0, 42.0), "lon": (19.0, 29.0), "desc": "Hellenic subduction"},
            "Turkey": {"lat": (36.0, 42.0), "lon": (26.0, 45.0), "desc": "Multiple fault systems"},
            "Iran": {"lat": (25.0, 40.0), "lon": (44.0, 63.0), "desc": "Continental collision"},
            "Indonesia": {"lat": (-11.0, 6.0), "lon": (95.0, 141.0), "desc": "Complex subduction"},
            "Mexico": {"lat": (14.0, 33.0), "lon": (-118.0, -86.0), "desc": "Subduction + transform"},
            "Chile": {"lat": (-56.0, -17.0), "lon": (-76.0, -66.0), "desc": "Nazca subduction"},
            "Taiwan": {"lat": (21.0, 26.0), "lon": (118.0, 122.0), "desc": "Arc-continent collision"},
            "Iceland": {"lat": (63.0, 67.0), "lon": (-25.0, -13.0), "desc": "Mid-Atlantic Ridge"},
            "Nepal": {"lat": (26.0, 31.0), "lon": (80.0, 88.0), "desc": "Himalayan collision"},
            "Pakistan": {"lat": (23.0, 37.0), "lon": (60.0, 77.0), "desc": "Collision zone"},
            "Afghanistan": {"lat": (29.0, 38.0), "lon": (60.0, 75.0), "desc": "Collision + Hindu Kush"},
            "Myanmar (Burma)": {"lat": (10.0, 28.0), "lon": (92.0, 101.0), "desc": "Subduction + Sagaing"},
            "Papua New Guinea": {"lat": (-12.0, -1.0), "lon": (140.0, 156.0), "desc": "Complex collision"},
        },
        
        "⚡ Historic Major Earthquake Zones": {
            "2011 Tohoku Region (Japan)": {"lat": (35.0, 42.0), "lon": (138.0, 145.0), "desc": "M9.1 megathrust"},
            "2004 Indian Ocean (Sumatra)": {"lat": (0.0, 15.0), "lon": (92.0, 100.0), "desc": "M9.1 tsunami"},
            "1960 Chile Earthquake": {"lat": (-46.0, -36.0), "lon": (-76.0, -71.0), "desc": "M9.5 largest recorded"},
            "1964 Alaska Earthquake": {"lat": (58.0, 63.0), "lon": (-153.0, -147.0), "desc": "M9.2 Good Friday"},
            "2010 Haiti": {"lat": (17.5, 19.5), "lon": (-74.0, -72.0), "desc": "M7.0 devastating"},
            "1906 San Francisco": {"lat": (36.0, 39.0), "lon": (-123.5, -121.5), "desc": "M7.9 San Andreas"},
            "2015 Nepal (Gorkha)": {"lat": (27.0, 29.0), "lon": (84.0, 86.0), "desc": "M7.8 Himalayan"},
            "1999 Turkey (Izmit)": {"lat": (40.0, 41.0), "lon": (29.0, 31.0), "desc": "M7.6 North Anatolian"},
            "2011 Christchurch (NZ)": {"lat": (-44.0, -43.0), "lon": (171.0, 173.0), "desc": "M6.3 shallow"},
        },
        
        "🌐 Global & Multi-Regional": {
            "Pacific Ring of Fire": {"lat": (-60.0, 70.0), "lon": (100.0, -60.0), "desc": "90% of earthquakes"},
            "Alpine-Himalayan Belt": {"lat": (25.0, 48.0), "lon": (-10.0, 140.0), "desc": "Collision belt"},
            "World (Global)": {"lat": (-90.0, 90.0), "lon": (-180.0, 180.0), "desc": "All earthquakes"},
            "Northern Hemisphere": {"lat": (0.0, 90.0), "lon": (-180.0, 180.0), "desc": "NH only"},
            "Southern Hemisphere": {"lat": (-90.0, 0.0), "lon": (-180.0, 180.0), "desc": "SH only"},
        }
    }
    
    # Region selection with Content Box styling
    st.markdown("### 🌍 Region Selection")
    
    col_cat, col_reg = st.columns(2)
    
    with col_cat:
        category = st.selectbox(
            "📂 Select Category:",
            list(REGION_PRESETS.keys()) + ["🔧 Custom Region"]
        )
    
    if category != "🔧 Custom Region":
        region_names = list(REGION_PRESETS[category].keys())
        with col_reg:
            region_preset = st.selectbox(
                "🎯 Select Specific Region:",
                region_names,
                help="Choose from pre-configured earthquake zones"
            )
        
        region_data = REGION_PRESETS[category][region_preset]
        default_minlat, default_maxlat = region_data["lat"]
        default_minlon, default_maxlon = region_data["lon"]
        
        st.markdown(f"""
        <div class="info-box">
               ℹ️ <strong>{region_preset}</strong>: {region_data['desc']}
        </div>
        """, unsafe_allow_html=True)
        
        is_custom = False
        selected_region = region_preset
        selected_category = category
    else:
        st.info("🔧 **Custom Region**: Define your own geographic boundaries")
        with col_reg:
            # Placeholder in column 2 just to balance layout if needed or put info
            st.empty()
            
        default_minlat, default_maxlat = -90.0, 90.0
        default_minlon, default_maxlon = -180.0, 180.0
        is_custom = True
        selected_region = "Custom"
        selected_category = "Custom"
        
        # Ask for custom name
        custom_name = st.text_input(
            "Enter a descriptive name for this region:",
            placeholder="e.g., My_Study_Area or Southern_California",
            help="This name will be used in the filename and dataset registry"
        )
        if custom_name:
            selected_region = custom_name
    
    # Geographic bounds
    st.markdown("### 📍 Geographic Boundaries")
    col1, col2 = st.columns(2)
    
    with col1:
        minlat = st.number_input("Minimum Latitude", -90.0, 90.0, default_minlat)
        maxlat = st.number_input("Maximum Latitude", -90.0, 90.0, default_maxlat)
    
    with col2:
        minlon = st.number_input("Minimum Longitude", -180.0, 180.0, default_minlon)
        maxlon = st.number_input("Maximum Longitude", -180.0, 180.0, default_maxlon)
    
    # Time range
    st.markdown("### 📅 Time Range")
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Start Date", value=datetime(2020, 1, 1))
    
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    
    # Additional parameters
    st.markdown("### ⚙️ Filter Parameters")
    min_magnitude = st.slider("Minimum Magnitude", 0.0, 9.0, 4.0, 0.1)
    
    # Generate filename preview
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    filename_base = generate_filename(selected_region, selected_category, start_str, end_str, is_custom)
    output_filename = f"{filename_base}.csv"
    
    st.markdown("---")
    st.markdown(f"""
    <div class="filename-box">
        📝 Output filename: `{output_filename}`
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Fetch button - Red style
    if st.button("🚀 Fetch Data and Calculate D", type="primary", use_container_width=True):
        if is_custom and not custom_name:
            st.error("❌ Please enter a name for your custom region")
        else:
            with st.spinner("Fetching earthquake data from USGS..."):
                try:
                    success = download_earthquakes(
                        start_date=start_str,
                        end_date=end_str,
                        min_latitude=minlat,
                        max_latitude=maxlat,
                        min_longitude=minlon,
                        max_longitude=maxlon,
                        min_magnitude=min_magnitude,
                        output_file=output_filename
                    )
                    
                    if success:
                        # Load and analyze
                        fetched_data = pd.read_csv(output_filename)
                        event_count = len(fetched_data)
                        
                        st.markdown(f'<div class="success-box">✅ Data successfully downloaded! Downloaded {event_count} earthquakes</div>', unsafe_allow_html=True)
                        
                        if event_count >= 10:
                            # Calculate fractal dimension
                            with st.spinner("Calculating fractal dimension..."):
                                result = box_counting(
                                    fetched_data['latitude'].values,
                                    fetched_data['longitude'].values,
                                    return_details=True
                                )
                            
                            # Register dataset
                            add_dataset(
                                name=filename_base,
                                filepath=output_filename,
                                region=selected_region,
                                category=selected_category,
                                min_lat=minlat,
                                max_lat=maxlat,
                                min_lon=minlon,
                                max_lon=maxlon,
                                start_date=start_str,
                                end_date=end_str,
                                min_magnitude=min_magnitude,
                                event_count=event_count,
                                fractal_d=result['D'],
                                r_squared=result['r_squared'],
                                std_error=result['std_error']
                            )
                            
                            # Refresh datasets
                            refresh_datasets()
                            
                            # Display results with new card style
                            st.markdown("### 📊 Analysis Results")
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.markdown(f"""
                                <div class="metric-card-container card-teal">
                                    <div class="metric-title">Fractal Dimension (D)</div>
                                    <div class="metric-value value-teal">{result['D']:.3f}</div>
                                    <div class="metric-sub">±{result['std_error']:.3f}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col2:
                                st.markdown(f"""
                                <div class="metric-card-container card-green" style="border-top-color: #6c757d;">
                                    <div class="metric-title">R² (Goodness of Fit)</div>
                                    <div class="metric-value" style="color: #333;">{result['r_squared']:.3f}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col3:
                                st.markdown(f"""
                                <div class="metric-card-container card-green" style="border-top-color: #6c757d;">
                                    <div class="metric-title">Number of Events</div>
                                    <div class="metric-value" style="color: #333;">{event_count}</div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                            # Download button
                            st.markdown("<br>", unsafe_allow_html=True)
                            csv = fetched_data.to_csv(index=False)
                            st.download_button(
                                "💾 Download Full Dataset",
                                csv,
                                output_filename,
                                "text/csv",
                                key='download-csv'
                            )
                        else:
                            st.warning(f"Only {event_count} earthquakes found. Need at least 10 for fractal analysis.")
                    else:
                        st.error("Failed to download data. Check parameters and try again.")
                        
                except Exception as e:
                    st.error(f"Error fetching data: {str(e)}")


# ========================================
# PAGE 4: Advanced Analysis
# ========================================
# ========================================
# PAGE 4: Advanced Analysis
# ========================================
elif page == "⚙️ Advanced Analysis":
    # Custom Header
    st.markdown('<div class="main-header" style="color: #9467bd;">⚙️ Advanced Fractal Analysis</div>', unsafe_allow_html=True)
    st.markdown("### Detailed box-counting analysis and parameter sensitivity testing")
    
    # Data selection with layout matching mockup
    st.markdown("---")
    st.markdown("### 📁 Select Dataset")
    
    # Layout: Selection inputs (left) | Info Cards (right)
    col_sel, col_info = st.columns([1.5, 2.5])
    
    data = None
    dataset_name = None
    
    with col_sel:
        source_type = st.radio(
            "Data Source:",
            ["📊 From Registry", "📤 Upload Custom File"],
            label_visibility="collapsed"
        )
        
        if source_type == "📊 From Registry":
            if len(available_datasets) == 0:
                st.warning("⚠️ No datasets in registry")
            else:
                dataset_names = [ds['name'] for ds in available_datasets]
                selected_name = st.selectbox("Select Dataset:", dataset_names, label_visibility="collapsed")
                
                selected_ds = next(ds for ds in available_datasets if ds['name'] == selected_name)
                data = load_dataset(selected_ds['filepath'])
                dataset_name = selected_ds['region'] 
                
                # Show Info Cards (Region, Events, Global D) in the right column
                with col_info:
                    c1, c2, c3 = st.columns(3)
                    with c1:
                         st.markdown(f"""
                        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; border-left: 4px solid #d62728; background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                            <div style="font-size: 0.8rem; color: #666; font-weight: bold;">📍 Region:</div>
                            <div style="font-size: 1.1rem; font-weight: bold; color: #333; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{selected_ds['region']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with c2:
                         st.markdown(f"""
                        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; border-left: 4px solid #e67e22; background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                            <div style="font-size: 0.8rem; color: #666; font-weight: bold;">🏆 Events:</div>
                            <div style="font-size: 1.2rem; font-weight: bold; color: #333;">{selected_ds['event_count']:,}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with c3:
                         st.markdown(f"""
                        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; border-left: 4px solid #9467bd; background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                            <div style="font-size: 0.8rem; color: #666; font-weight: bold;">🌐 Global D:</div>
                            <div style="font-size: 1.2rem; font-weight: bold; color: #333;">{selected_ds.get('fractal_d', 0):.3f}</div>
                        </div>
                        """, unsafe_allow_html=True)

        else:
            uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
            if uploaded_file is not None:
                data = pd.read_csv(uploaded_file)
                dataset_name = "Custom Upload"
                if 'latitude' not in data.columns or 'longitude' not in data.columns:
                    st.error("CSV must contain 'latitude' and 'longitude' columns")
                    data = None
    
    if data is not None:
        # Layout: Map (Left) vs Temporal Charts (Right)
        st.markdown("<br>", unsafe_allow_html=True)
        row1_col1, row1_col2 = st.columns([1, 1])
        
        with row1_col1:
            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            st.markdown('<div class="box-header">📍 Geographic Distribution</div>', unsafe_allow_html=True)
            
            # Map logic
            center = [data['latitude'].mean(), data['longitude'].mean()]
            m = folium.Map(location=center, zoom_start=6, height=350)
            
            # Sample if too large
            if len(data) > 1000:
                plot_data = data.sample(1000)
                caption_text = f"Showing 1,000 sampled points from {len(data):,} events"
            else:
                plot_data = data
                caption_text = f"Showing {len(data)} earthquake epicenters"
                
            for idx, row in plot_data.iterrows():
                # Color by magnitude if available
                color = '#9467bd' # Purple default
                if 'mag' in row:
                    if row['mag'] >= 6: color = '#d62728' # Red
                    elif row['mag'] >= 5: color = '#ff7f0e' # Orange
                
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=3,
                    color=color,
                    fill=True,
                    fillOpacity=0.7
                ).add_to(m)
            
            folium_static(m, width=None, height=350) 
            st.caption(caption_text)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with row1_col2:
            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            st.markdown('<div class="box-header">📈 Temporal Analysis</div>', unsafe_allow_html=True)
            
            if 'time' in data.columns:
                data_temp = data.copy()
                data_temp['timestamp'] = pd.to_datetime(data_temp['time'])
                data_temp['year'] = data_temp['timestamp'].dt.year
                
                yearly_d = calculate_yearly_d(data_temp, dataset_name)
                
                # Create subplots strictly side-by-side inside this column
                fig_temp = make_subplots(rows=1, cols=2, subplot_titles=("Fractal Dim. (D)", "Events per Year"))
                
                if yearly_d is not None and not yearly_d.empty:
                    # Line chart
                    fig_temp.add_trace(
                        go.Scatter(x=yearly_d['year'], y=yearly_d['D'], error_y=dict(type='data', array=yearly_d['std_error']),
                                   mode='lines+markers', line=dict(color='#9467bd'), marker=dict(size=4), name='D'),
                        row=1, col=1
                    )
                    
                    # Bar chart
                    if 'year' in data_temp.columns:
                        year_counts = data_temp['year'].value_counts().sort_index()
                        fig_temp.add_trace(
                            go.Bar(x=year_counts.index, y=year_counts.values, marker_color='#9467bd', name='Events'),
                            row=1, col=2
                        )
                    
                    fig_temp.update_layout(height=350, showlegend=False, margin=dict(l=20, r=20, t=40, b=20))
                    # Small font for subplots to fit
                    fig_temp.update_annotations(font_size=10)
                    
                    st.plotly_chart(fig_temp, use_container_width=True)
                else:
                    st.info("Insufficient temporal data for fractal analysis")
            else:
                st.warning("No time information available in dataset")
            st.markdown('</div>', unsafe_allow_html=True)

        # Advanced Parameters Section
        st.markdown("### 🎛️ Box-Counting Parameters")
        
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            min_box = st.number_input("Minimum Box Size (deg):", value=0.1, format="%.1f")
        with p_col2:
            max_box = st.number_input("Maximum Box Size (deg):", value=10.0, format="%.1f")
            
        num_scales = st.slider("Number of Scales:", 5, 50, 20)
        
        if st.button("🔬 Perform Box-Counting Analysis", type="primary", use_container_width=True):
            with st.spinner("Running advanced box-counting..."):
                try:
                    result = box_counting(
                        data['latitude'].values,
                        data['longitude'].values,
                        min_box_size=min_box,
                        max_box_size=max_box,
                        num_scales=num_scales,
                        return_details=True
                    )
                    
                    # Results
                    st.markdown("---")
                    st.markdown("### 📊 Results")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("D", f"{result['D']:.4f}")
                    with col2:
                        st.metric("Std Error", f"{result['std_error']:.4f}")
                    with col3:
                        st.metric("R²", f"{result['r_squared']:.4f}")
                    with col4:
                        st.metric("Events", result['n_points'])
                    
                    # Log-log plot
                    st.markdown("### 📈 Box-Counting Log-Log Plot")
                    
                    log_r = np.log10(result['box_sizes'])
                    log_N = np.log10(result['counts'])
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=log_r, y=log_N,
                        mode='markers',
                        marker=dict(size=10, color='purple'),
                        name='Data Points'
                    ))
                    
                    z = np.polyfit(log_r, log_N, 1)
                    p = np.poly1d(z)
                    fig.add_trace(go.Scatter(
                        x=log_r, y=p(log_r),
                        mode='lines',
                        line=dict(color='orange', dash='dash', width=3),
                        name=f'Linear Fit (slope={-z[0]:.4f})'
                    ))
                    
                    fig.update_layout(
                        title=f"Box-Counting Analysis: D = {result['D']:.4f} ± {result['std_error']:.4f}",
                        xaxis_title="log₁₀(Box Size)",
                        yaxis_title="log₁₀(Box Count)",
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Detailed data table
                    st.markdown("### 📋 Detailed Scale Analysis")
                    
                    scale_df = pd.DataFrame({
                        'Box Size (deg)': result['box_sizes'],
                        'Box Count': result['counts'],
                        'log₁₀(Box Size)': log_r,
                        'log₁₀(Box Count)': log_N
                    })
                    
                    st.dataframe(scale_df)
                    
                    # Export
                    csv_export = scale_df.to_csv(index=False)
                    st.download_button(
                        "💾 Download Scale Analysis",
                        csv_export,
                        f"{dataset_name}_box_counting_analysis.csv",
                        "text/csv"
                    )
                    
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")


# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>Seismic Fractal Analysis Dashboard V2.0</strong></p>
    <p>Enhanced with Dynamic Data Management | {len(available_datasets)} Dataset(s) Available</p>
    <p>B.Tech Project | February 2026 | Data Source: USGS Earthquake Catalog</p>
</div>
""", unsafe_allow_html=True)
