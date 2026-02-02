"""
Regional Comparison: Yearly Fractal Dimension Variation
Compares Himalayan vs Andaman-Sumatra earthquake patterns over time.

Author: Seismic Analysis Team
Date: February 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from fractal_engine import box_counting
from typing import Dict, Tuple
import warnings
warnings.filterwarnings('ignore')


def load_earthquake_data(csv_path: str) -> pd.DataFrame:
    """Load and parse earthquake CSV data."""
    df = pd.read_csv(csv_path)
    
    # Parse timestamp and extract year
    df['timestamp'] = pd.to_datetime(df['time'])
    df['year'] = df['timestamp'].dt.year
    
    return df


def calculate_yearly_fractal_dimensions(df: pd.DataFrame, region_name: str) -> pd.DataFrame:
    """
    Calculate fractal dimension for each year in the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Earthquake data with 'latitude', 'longitude', and 'year' columns
    region_name : str
        Name of the region for labeling
        
    Returns:
    --------
    pd.DataFrame with columns: year, D, std_error, r_squared, n_events
    """
    results = []
    
    years = sorted(df['year'].unique())
    
    for year in years:
        year_data = df[df['year'] == year]
        
        # Skip if too few events (need at least 10 for reliable D)
        if len(year_data) < 10:
            continue
        
        try:
            # Calculate fractal dimension for this year
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
        except Exception as e:
            print(f"  Warning: Could not calculate D for {region_name} year {year}: {e}")
            continue
    
    return pd.DataFrame(results)


def create_comparison_plot(himalayan_df: pd.DataFrame, andaman_df: pd.DataFrame, save_path: str = 'fractal_comparison_yearly.png'):
    """
    Create comprehensive comparison visualization.
    
    Creates a multi-panel figure showing:
    1. D vs Year for both regions
    2. D difference over time
    3. Statistical summary
    """
    # Set up the figure with GridSpec for flexible layout
    fig = plt.figure(figsize=(16, 10))
    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    # Color scheme
    himalayan_color = '#E74C3C'  # Red
    andaman_color = '#3498DB'    # Blue
    
    # ========== Panel 1: Main comparison plot ==========
    ax1 = fig.add_subplot(gs[0:2, :])
    
    # Plot Himalayan data
    ax1.errorbar(himalayan_df['year'], himalayan_df['D'], 
                 yerr=himalayan_df['std_error'],
                 marker='o', markersize=8, linewidth=2, capsize=5,
                 color=himalayan_color, label='Himalayas', alpha=0.8)
    
    # Plot Andaman data
    ax1.errorbar(andaman_df['year'], andaman_df['D'], 
                 yerr=andaman_df['std_error'],
                 marker='s', markersize=8, linewidth=2, capsize=5,
                 color=andaman_color, label='Andaman-Sumatra', alpha=0.8)
    
    # Add trend lines
    if len(himalayan_df) > 2:
        z_h = np.polyfit(himalayan_df['year'], himalayan_df['D'], 1)
        p_h = np.poly1d(z_h)
        ax1.plot(himalayan_df['year'], p_h(himalayan_df['year']), 
                '--', color=himalayan_color, alpha=0.5, linewidth=1.5,
                label=f'Himalayan trend: {z_h[0]:.4f}/year')
    
    if len(andaman_df) > 2:
        z_a = np.polyfit(andaman_df['year'], andaman_df['D'], 1)
        p_a = np.poly1d(z_a)
        ax1.plot(andaman_df['year'], p_a(andaman_df['year']), 
                '--', color=andaman_color, alpha=0.5, linewidth=1.5,
                label=f'Andaman trend: {z_a[0]:.4f}/year')
    
    ax1.set_xlabel('Year', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Fractal Dimension (D)', fontsize=14, fontweight='bold')
    ax1.set_title('Yearly Fractal Dimension Evolution: Himalayas vs Andaman-Sumatra', 
                  fontsize=16, fontweight='bold', pad=20)
    ax1.legend(loc='best', fontsize=12, framealpha=0.9)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_ylim(0.8, 1.8)
    
    # ========== Panel 2: D Difference ==========
    ax2 = fig.add_subplot(gs[2, 0])
    
    # Find common years
    common_years = set(himalayan_df['year']) & set(andaman_df['year'])
    if len(common_years) > 0:
        common_years = sorted(common_years)
        differences = []
        
        for year in common_years:
            d_him = himalayan_df[himalayan_df['year'] == year]['D'].values[0]
            d_and = andaman_df[andaman_df['year'] == year]['D'].values[0]
            differences.append(d_and - d_him)
        
        ax2.bar(common_years, differences, color='#9B59B6', alpha=0.7, edgecolor='black')
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax2.set_ylabel('ΔD (Andaman - Himalaya)', fontsize=12, fontweight='bold')
        ax2.set_title('Fractal Dimension Difference', fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
    
    # ========== Panel 3: Statistics Summary ==========
    ax3 = fig.add_subplot(gs[2, 1])
    ax3.axis('off')
    
    # Calculate statistics
    stats_text = "Statistical Summary\n" + "="*40 + "\n\n"
    
    stats_text += "HIMALAYAS:\n"
    stats_text += f"  Mean D: {himalayan_df['D'].mean():.3f} ± {himalayan_df['D'].std():.3f}\n"
    stats_text += f"  Range: [{himalayan_df['D'].min():.3f}, {himalayan_df['D'].max():.3f}]\n"
    stats_text += f"  Total events: {himalayan_df['n_events'].sum()}\n"
    stats_text += f"  Years analyzed: {len(himalayan_df)}\n\n"
    
    stats_text += "ANDAMAN-SUMATRA:\n"
    stats_text += f"  Mean D: {andaman_df['D'].mean():.3f} ± {andaman_df['D'].std():.3f}\n"
    stats_text += f"  Range: [{andaman_df['D'].min():.3f}, {andaman_df['D'].max():.3f}]\n"
    stats_text += f"  Total events: {andaman_df['n_events'].sum()}\n"
    stats_text += f"  Years analyzed: {len(andaman_df)}\n\n"
    
    if len(common_years) > 0:
        mean_diff = np.mean(differences)
        stats_text += "COMPARISON:\n"
        stats_text += f"  Mean ΔD: {mean_diff:.3f}\n"
        stats_text += f"  Andaman D is {abs(mean_diff)/himalayan_df['D'].mean()*100:.1f}% "
        stats_text += f"{'higher' if mean_diff > 0 else 'lower'}\n"
    
    ax3.text(0.1, 0.9, stats_text, fontsize=11, family='monospace',
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Add overall title
    fig.suptitle('Seismic Fractal Dimension Analysis: Comparative Study', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # Save figure
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Comparison plot saved as: {save_path}")
    
    return fig


def main():
    """Main analysis workflow."""
    print("="*70)
    print("Regional Seismic Fractal Dimension Comparison")
    print("="*70)
    
    # Load data
    print("\n1. Loading earthquake datasets...")
    himalayan_data = load_earthquake_data('query.csv')
    andaman_data = load_earthquake_data('andaman_earthquakes.csv')
    print(f"   ✓ Himalayan data: {len(himalayan_data)} events from "
          f"{himalayan_data['year'].min()} to {himalayan_data['year'].max()}")
    print(f"   ✓ Andaman data: {len(andaman_data)} events from "
          f"{andaman_data['year'].min()} to {andaman_data['year'].max()}")
    
    # Calculate yearly D values
    print("\n2. Calculating yearly fractal dimensions...")
    print("   Processing Himalayas...")
    himalayan_yearly = calculate_yearly_fractal_dimensions(himalayan_data, "Himalayas")
    print(f"   ✓ Completed {len(himalayan_yearly)} years")
    
    print("   Processing Andaman-Sumatra...")
    andaman_yearly = calculate_yearly_fractal_dimensions(andaman_data, "Andaman-Sumatra")
    print(f"   ✓ Completed {len(andaman_yearly)} years")
    
    # Display summary
    print("\n3. Summary Statistics:")
    print(f"   Himalayas: Mean D = {himalayan_yearly['D'].mean():.3f} ± {himalayan_yearly['D'].std():.3f}")
    print(f"   Andaman:   Mean D = {andaman_yearly['D'].mean():.3f} ± {andaman_yearly['D'].std():.3f}")
    print(f"   Difference: ΔD = {andaman_yearly['D'].mean() - himalayan_yearly['D'].mean():.3f}")
    
    # Create visualization
    print("\n4. Creating comparison visualization...")
    create_comparison_plot(himalayan_yearly, andaman_yearly)
    
    # Save detailed results
    print("\n5. Saving detailed results...")
    himalayan_yearly.to_csv('himalayan_yearly_D.csv', index=False)
    print("   ✓ himalayan_yearly_D.csv")
    andaman_yearly.to_csv('andaman_yearly_D.csv', index=False)
    print("   ✓ andaman_yearly_D.csv")
    
    print("\n" + "="*70)
    print("Analysis Complete!")
    print("="*70)


if __name__ == "__main__":
    main()
