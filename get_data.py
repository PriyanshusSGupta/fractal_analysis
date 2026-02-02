import requests
import argparse
from datetime import datetime

def download_earthquakes(start_date, end_date, output_file, 
                         min_latitude=0, max_latitude=15, 
                         min_longitude=90, max_longitude=98,
                         min_magnitude=2.5):
    """
    Download earthquake data from USGS FDSNWS API
    
    Parameters:
    -----------
    start_date : str
        Start date in YYYY-MM-DD format
    end_date : str
        End date in YYYY-MM-DD format
    output_file : str
        Output CSV filename
    min_latitude : float, optional
        Minimum latitude (default: 0 for Andaman)
    max_latitude : float, optional
        Maximum latitude (default: 15 for Andaman)
    min_longitude : float, optional
        Minimum longitude (default: 90 for Andaman)
    max_longitude : float, optional
        Maximum longitude (default: 98 for Andaman)
    min_magnitude : float, optional
        Minimum magnitude (default: 2.5)
    """
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    
    # Build parameters
    params = {
        'starttime': start_date,
        'endtime': end_date,
        'minlatitude': min_latitude,
        'maxlatitude': max_latitude,
        'minlongitude': min_longitude,
        'maxlongitude': max_longitude,
        'minmagnitude': min_magnitude,
        'format': 'csv',
        'limit': 20000
    }
    
    print(f"Requesting earthquake data from {start_date} to {end_date}...")
    print(f"Region: Lat [{min_latitude}, {max_latitude}], Lon [{min_longitude}, {max_longitude}]")
    print(f"Min Magnitude: {min_magnitude}")
    
    try:
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            with open(output_file, 'w') as f:
                f.write(response.text)
            print(f"✓ Data downloaded successfully: {output_file}")
            print(f"  -> Retrieved {len(response.text.splitlines())-1} earthquake records")
            return True
        else:
            print(f"✗ Error: HTTP {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Failed to connect: {e}")
        return False

if __name__ == "__main__":
    # Same time range as your Himalayan study for consistency
    download_earthquakes(
        start_date='2010-01-01', 
        end_date='2026-02-02', 
        output_file='andaman_earthquakes.csv'
    )
