"""
Interactive Seismic Fractal Analysis Dashboard
Multi-page Streamlit application for exploring earthquake fractal dimensions

Author: Seismic Analysis Team
Date: February 2026
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
import requests
from io import StringIO

# Import our custom modules
from fractal_engine import box_counting, analyze_csv
from get_data import download_earthquakes

# Page configuration
st.set_page_config(
    page_title="Seismic Fractal Analysis",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ff7f0e;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 0.3rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        padding: 1rem;
        border-radius: 0.3rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Sidebar navigation
st.sidebar.title("🌍 Navigation")
page = st.sidebar.radio(
    "Select a page:",
    ["📊 Overview & Comparison", "📈 Temporal Analysis", "🔍 Fetch New Data", "⚙️ Advanced Analysis"]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**About**: This dashboard analyzes earthquake distributions using fractal dimension calculations.

**Regions**:
- 🏔️ Himalayas (Collision Zone)
- 🌊 Andaman-Sumatra (Subduction Zone)
""")


# Helper functions
@st.cache_data
def load_data(file_path):
    """Load earthquake data from CSV."""
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['time'])
    df['year'] = df['timestamp'].dt.year
    return df


@st.cache_data
def calculate_global_d(latitudes, longitudes):
    """Calculate overall fractal dimension."""
    return box_counting(latitudes, longitudes, return_details=True)


@st.cache_data
def load_yearly_results():
    """Load pre-calculated yearly D values."""
    try:
        him_df = pd.read_csv('himalayan_yearly_D.csv')
        and_df = pd.read_csv('andaman_yearly_D.csv')
        return him_df, and_df
    except:
        return None, None


# ========================================
# PAGE 1: Overview & Comparison
# ========================================
if page == "📊 Overview & Comparison":
    st.markdown('<div class="main-header">🌍 Seismic Fractal Dimension Analysis</div>', unsafe_allow_html=True)
    st.markdown("### Comparative Study: Himalayan vs Andaman-Sumatra Earthquake Patterns")
    
    # Load data
    with st.spinner("Loading earthquake datasets..."):
        himalayan_data = load_data('query.csv')
        andaman_data = load_data('andaman_earthquakes.csv')
    
    # Calculate global D values
    with st.spinner("Calculating fractal dimensions..."):
        him_result = calculate_global_d(himalayan_data['latitude'], himalayan_data['longitude'])
        and_result = calculate_global_d(andaman_data['latitude'], andaman_data['longitude'])
    
    # Display key metrics
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🏔️ Himalayan D", f"{him_result['D']:.3f}", f"±{him_result['std_error']:.3f}")
        st.caption(f"R² = {him_result['r_squared']:.3f}")
        st.caption(f"{him_result['n_points']:,} events")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🌊 Andaman-Sumatra D", f"{and_result['D']:.3f}", f"±{and_result['std_error']:.3f}")
        st.caption(f"R² = {and_result['r_squared']:.3f}")
        st.caption(f"{and_result['n_points']:,} events")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        diff = and_result['D'] - him_result['D']
        pct = (diff / him_result['D']) * 100
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📊 Difference (ΔD)", f"{diff:.3f}", f"{pct:.1f}%")
        st.caption("Andaman - Himalaya")
        st.caption(f"Higher complexity →")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Interpretation
    st.markdown("---")
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    **🔬 Scientific Interpretation:**
    
    The **Andaman-Sumatra** region shows a significantly higher fractal dimension (~24% higher), reflecting:
    - 🔹 **3D slab geometry** with curved subduction interface
    - 🔹 **Multiple fault systems** (megathrust, back-arc, strike-slip)
    - 🔹 **Greater depth range** (0-200 km) compared to Himalayas (0-20 km)
    - 🔹 **Complex stress regimes** from oceanic subduction
    
    The **Himalayas** show lower D, characteristic of:
    - 🔸 **Linear fault alignment** along Main Himalayan Thrust
    - 🔸 **Quasi-planar seismicity** with limited depth variation
    - 🔸 **Concentrated deformation** on fewer major fault systems
    - 🔸 **Continental collision** creating more clustered patterns
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Interactive maps
    st.markdown("---")
    st.markdown('<div class="sub-header">📍 Geographic Distribution</div>', unsafe_allow_html=True)
    
    map_col1, map_col2 = st.columns(2)
    
    with map_col1:
        st.markdown("**🏔️ Himalayan Earthquakes**")
        # Create folium map
        him_center = [himalayan_data['latitude'].mean(), himalayan_data['longitude'].mean()]
        him_map = folium.Map(location=him_center, zoom_start=6, tiles='OpenStreetMap')
        
        # Sample data for performance (plot every 10th point if too many)
        sample_size = min(500, len(himalayan_data))
        sample_indices = np.random.choice(len(himalayan_data), sample_size, replace=False)
        
        for idx in sample_indices:
            row = himalayan_data.iloc[idx]
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius = 2 + row.get('mag', 4) * 0.5 if 'mag' in himalayan_data.columns else 2,
                color='red',
                fill=True,
                fillOpacity=0.6
            ).add_to(him_map)
        
        folium_static(him_map, width=400, height=400)
    
    with map_col2:
        st.markdown("**🌊 Andaman-Sumatra Earthquakes**")
        # Create folium map
        and_center = [andaman_data['latitude'].mean(), andaman_data['longitude'].mean()]
        and_map = folium.Map(location=and_center, zoom_start=6, tiles='OpenStreetMap')
        
        # Sample data
        sample_size = min(500, len(andaman_data))
        sample_indices = np.random.choice(len(andaman_data), sample_size, replace=False)
        
        for idx in sample_indices:
            row = andaman_data.iloc[idx]
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=2 + row.get('mag', 4) * 0.5 if 'mag' in andaman_data.columns else 2,
                color='blue',
                fill=True,
                fillOpacity=0.6
            ).add_to(and_map)
        
        folium_static(and_map, width=400, height=400)
    
    # Box-counting visualization
    st.markdown("---")
    st.markdown('<div class="sub-header">📦 Box-Counting Analysis</div>', unsafe_allow_html=True)
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Himalayas', 'Andaman-Sumatra'),
        x_title='log₁₀(Box Size)',
        y_title='log₁₀(Box Count)'
    )
    
    # Himalayan log-log plot
    log_r_him = np.log10(him_result['box_sizes'])
    log_N_him = np.log10(him_result['counts'])
    fig.add_trace(
        go.Scatter(x=log_r_him, y=log_N_him, mode='markers', 
                   marker=dict(size=8, color='red'), name='Himalayas'),
        row=1, col=1
    )
    # Fit line
    z_him = np.polyfit(log_r_him, log_N_him, 1)
    p_him = np.poly1d(z_him)
    fig.add_trace(
        go.Scatter(x=log_r_him, y=p_him(log_r_him), mode='lines',
                   line=dict(color='darkred', dash='dash'), 
                   name=f'Fit: D={-z_him[0]:.3f}', showlegend=True),
        row=1, col=1
    )
    
    # Andaman log-log plot
    log_r_and = np.log10(and_result['box_sizes'])
    log_N_and = np.log10(and_result['counts'])
    fig.add_trace(
        go.Scatter(x=log_r_and, y=log_N_and, mode='markers',
                   marker=dict(size=8, color='blue'), name='Andaman'),
        row=1, col=2
    )
    # Fit line
    z_and = np.polyfit(log_r_and, log_N_and, 1)
    p_and = np.poly1d(z_and)
    fig.add_trace(
        go.Scatter(x=log_r_and, y=p_and(log_r_and), mode='lines',
                   line=dict(color='darkblue', dash='dash'),
                   name=f'Fit: D={-z_and[0]:.3f}', showlegend=True),
        row=1, col=2
    )
    
    fig.update_layout(height=500, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption("""
    **Interpretation**: The steeper negative slope for Andaman-Sumatra indicates higher fractal dimension,
    meaning earthquakes fill space more uniformly across multiple scales.
    """)


# ========================================
# PAGE 2: Temporal Analysis
# ========================================
elif page == "📈 Temporal Analysis":
    st.markdown('<div class="main-header">📈 Temporal Fractal Dimension Evolution</div>', unsafe_allow_html=True)
    
    # Load yearly data
    him_yearly, and_yearly = load_yearly_results()
    
    if him_yearly is None or and_yearly is None:
        st.warning("Yearly analysis data not found. Running analysis...")
        
        with st.spinner("Calculating yearly fractal dimensions... This may take a moment."):
            import subprocess
            subprocess.run(["python", "compare_regions.py"], cwd="/home/ancientai/Documents/8sem/btp")
            him_yearly, and_yearly = load_yearly_results()
    
    if him_yearly is not None and and_yearly is not None:
        # Time range selector
        st.markdown("### 🎯 Time Range Selection")
        min_year = int(min(him_yearly['year'].min(), and_yearly['year'].min()))
        max_year = int(max(him_yearly['year'].max(), and_yearly['year'].max()))
        
        year_range = st.slider(
            "Select year range:",
            min_year, max_year, (min_year, max_year)
        )
        
        # Filter data
        him_filtered = him_yearly[(him_yearly['year'] >= year_range[0]) & (him_yearly['year'] <= year_range[1])]
        and_filtered = and_yearly[(and_yearly['year'] >= year_range[0]) & (and_yearly['year'] <= year_range[1])]
        
        # Main time series plot
        st.markdown("---")
        st.markdown('<div class="sub-header">📊 Fractal Dimension Over Time</div>', unsafe_allow_html=True)
        
        fig = go.Figure()
        
        # Himalayan trace
        fig.add_trace(go.Scatter(
            x=him_filtered['year'], y=him_filtered['D'],
            error_y=dict(type='data', array=him_filtered['std_error']),
            mode='markers+lines',
            name='Himalayas',
            marker=dict(size=10, color='red', symbol='circle'),
            line=dict(width=2, color='red')
        ))
        
        # Andaman trace
        fig.add_trace(go.Scatter(
            x=and_filtered['year'], y=and_filtered['D'],
            error_y=dict(type='data', array=and_filtered['std_error']),
            mode='markers+lines',
            name='Andaman-Sumatra',
            marker=dict(size=10, color='blue', symbol='square'),
            line=dict(width=2, color='blue')
        ))
        
        fig.update_layout(
            title="Yearly Fractal Dimension Evolution",
            xaxis_title="Year",
            yaxis_title="Fractal Dimension (D)",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistics
        st.markdown("---")
        st.markdown('<div class="sub-header">📊 Statistical Summary</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🏔️ Himalayas**")
            st.metric("Mean D", f"{him_filtered['D'].mean():.3f}")
            st.metric("Std Dev", f"{him_filtered['D'].std():.3f}")
            st.metric("Range", f"[{him_filtered['D'].min():.3f}, {him_filtered['D'].max():.3f}]")
            st.metric("Total Events", f"{him_filtered['n_events'].sum():,}")
        
        with col2:
            st.markdown("**🌊 Andaman-Sumatra**")
            st.metric("Mean D", f"{and_filtered['D'].mean():.3f}")
            st.metric("Std Dev", f"{and_filtered['D'].std():.3f}")
            st.metric("Range", f"[{and_filtered['D'].min():.3f}, {and_filtered['D'].max():.3f}]")
            st.metric("Total Events", f"{and_filtered['n_events'].sum():,}")
        
        # Event count over time
        st.markdown("---")
        st.markdown('<div class="sub-header">📉 Event Count Trends</div>', unsafe_allow_html=True)
        
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=him_filtered['year'], y=him_filtered['n_events'],
            name='Himalayas', marker_color='red', opacity=0.7
        ))
        fig2.add_trace(go.Bar(
            x=and_filtered['year'], y=and_filtered['n_events'],
            name='Andaman', marker_color='blue', opacity=0.7
        ))
        
        fig2.update_layout(
            title="Number of Earthquakes per Year",
            xaxis_title="Year",
            yaxis_title="Event Count",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Download results
        st.markdown("---")
        st.markdown("### 💾 Download Data")
        col1, col2 = st.columns(2)
        
        with col1:
            csv_him = him_filtered.to_csv(index=False)
            st.download_button(
                "Download Himalayan Data (CSV)",
                csv_him,
                "himalayan_yearly_D_filtered.csv",
                "text/csv"
            )
        
        with col2:
            csv_and = and_filtered.to_csv(index=False)
            st.download_button(
                "Download Andaman Data (CSV)",
                csv_and,
                "andaman_yearly_D_filtered.csv",
                "text/csv"
            )


# ========================================
# PAGE 3: Fetch New Data
# ========================================
elif page == "🔍 Fetch New Data":
    st.markdown('<div class="main-header">🔍 Fetch Earthquake Data</div>', unsafe_allow_html=True)
    st.markdown("### Download earthquake data from USGS and calculate fractal dimension")
    
    # Comprehensive region presets database
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
    
    # Region preset selection
    st.markdown("---")
    st.markdown("### 🌍 Region Selection")
    
    # Category selection
    category = st.selectbox(
        "📂 Select Category:",
        list(REGION_PRESETS.keys()) + ["🔧 Custom Region"]
    )
    
    if category != "🔧 Custom Region":
        # Region selection within category
        region_names = list(REGION_PRESETS[category].keys())
        region_preset = st.selectbox(
            "🎯 Select Specific Region:",
            region_names,
            help="Choose from pre-configured earthquake zones"
        )
        
        # Get coordinates and description
        region_data = REGION_PRESETS[category][region_preset]
        default_minlat, default_maxlat = region_data["lat"]
        default_minlon, default_maxlon = region_data["lon"]
        
        # Display region info
        st.info(f"**{region_preset}**: {region_data['desc']}")
        
    else:
        # Custom region
        st.info("🔧 **Custom Region**: Define your own geographic boundaries")
        default_minlat, default_maxlat = -90.0, 90.0
        default_minlon, default_maxlon = -180.0, 180.0
    
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
        start_date = st.date_input(
            "Start Date",
            value=datetime(2020, 1, 1)
        )
    
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now()
        )
    
    # Additional parameters
    st.markdown("### ⚙️ Filter Parameters")
    min_magnitude = st.slider("Minimum Magnitude", 0.0, 9.0, 4.0, 0.1)
    
    # Fetch button
    st.markdown("---")
    if st.button("🚀 Fetch Data and Calculate D", type="primary"):
        with st.spinner("Fetching earthquake data from USGS..."):
            try:
                # Call the download function
                output_filename = f"fetched_earthquakes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                
                download_earthquakes(
                    start_date=start_date.strftime("%Y-%m-%d"),
                    end_date=end_date.strftime("%Y-%m-%d"),
                    min_latitude=minlat,
                    max_latitude=maxlat,
                    min_longitude=minlon,
                    max_longitude=maxlon,
                    min_magnitude=min_magnitude,
                    output_file=output_filename
                )
                
                st.markdown('<div class="success-box">✅ Data successfully downloaded!</div>', unsafe_allow_html=True)
                
                # Load and analyze
                fetched_data = pd.read_csv(output_filename)
                st.success(f"Downloaded {len(fetched_data)} earthquakes")
                
                if len(fetched_data) >= 10:
                    # Calculate fractal dimension
                    with st.spinner("Calculating fractal dimension..."):
                        result = box_counting(
                            fetched_data['latitude'].values,
                            fetched_data['longitude'].values,
                            return_details=True
                        )
                    
                    # Display results
                    st.markdown("---")
                    st.markdown("### 📊 Analysis Results")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Fractal Dimension (D)", f"{result['D']:.3f}", f"±{result['std_error']:.3f}")
                    with col2:
                        st.metric("R² (Goodness of Fit)", f"{result['r_squared']:.3f}")
                    with col3:
                        st.metric("Number of Events", result['n_points'])
                    
                    # Show data
                    st.markdown("### 📄 Downloaded Data Preview")
                    st.dataframe(fetched_data.head(20))
                    
                    # Download button
                    csv = fetched_data.to_csv(index=False)
                    st.download_button(
                        "💾 Download Full Dataset",
                        csv,
                        output_filename,
                        "text/csv",
                        key='download-csv'
                    )
                    
                else:
                    st.warning(f"Only {len(fetched_data)} earthquakes found. Need at least 10 for fractal analysis.")
                
            except Exception as e:
                st.error(f"Error fetching data: {str(e)}")
                st.info("Please check your parameters and try again.")


# ========================================
# PAGE 4: Advanced Analysis
# ========================================
elif page == "⚙️ Advanced Analysis":
    st.markdown('<div class="main-header">⚙️ Advanced Fractal Analysis</div>', unsafe_allow_html=True)
    st.markdown("### Custom parameter exploration and detailed analysis")
    
    # Data selection
    st.markdown("---")
    st.markdown("### 📁 Select Dataset")
    
    dataset_choice = st.radio(
        "Choose dataset:",
        ["Himalayas (query.csv)", "Andaman (andaman_earthquakes.csv)", "Upload Custom Data"]
    )
    
    if dataset_choice == "Upload Custom Data":
        uploaded_file = st.file_uploader("Upload CSV file with 'latitude' and 'longitude' columns", type=['csv'])
        if uploaded_file:
            data = pd.read_csv(uploaded_file)
        else:
            data = None
    elif dataset_choice == "Himalayas (query.csv)":
        data = load_data('query.csv')
    else:
        data = load_data('andaman_earthquakes.csv')
    
    if data is not None:
        st.success(f"Loaded {len(data)} earthquakes")
        
        # Parameter controls
        st.markdown("---")
        st.markdown("### 🎛️ Box-Counting Parameters")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            min_box = st.number_input("Minimum Box Size (deg)", 0.01, 10.0, 0.1, 0.01)
        
        with col2:
            max_box = st.number_input("Maximum Box Size (deg)", min_box, 50.0, 10.0, 0.1)
        
        with col3:
            num_scales = st.slider("Number of Scales", 5, 50, 20)
        
        # Calculate button
        if st.button("🔬 Perform Analysis", type="primary"):
            with st.spinner("Calculating fractal dimension with custom parameters..."):
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
                    
                    # Fit line
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
                        "box_counting_analysis.csv",
                        "text/csv"
                    )
                    
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
                    st.info("Try adjusting the box size parameters or check your data format.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>Seismic Fractal Analysis Dashboard</strong></p>
    <p>B.Tech Project | February 2026 | Data Source: USGS Earthquake Catalog</p>
</div>
""", unsafe_allow_html=True)
