"""
Space Weather Data Collection Module
Fetches real-time data from NOAA and NASA APIs
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class SpaceWeatherDataCollector:
    """
    Collects real-time and historical space weather data from multiple sources
    """
    
    def __init__(self):
        self.noaa_base_url = "https://services.swpc.noaa.gov/json"
        self.nasa_donki_url = "https://api.nasa.gov/DONKI"
        self.nasa_api_key = "DEMO_KEY"  # Replace with your NASA API key from https://api.nasa.gov/
        
    def get_solar_wind_data(self):
        """Fetch real-time solar wind data (7-day history)"""
        try:
            url = f"{self.noaa_base_url}/plasma-7-day.json"
            response = requests.get(url, timeout=10)
            data = response.json()
            df = pd.DataFrame(data)
            df['time_tag'] = pd.to_datetime(df['time_tag'])
            
            # Convert numeric columns
            numeric_cols = ['density', 'speed', 'temperature']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            return df
        except Exception as e:
            print(f"Error fetching solar wind data: {e}")
            return None
    
    def get_geomagnetic_data(self):
        """Fetch geomagnetic K-index data"""
        try:
            url = f"{self.noaa_base_url}/planetary_k_index_1m.json"
            response = requests.get(url, timeout=10)
            data = response.json()
            df = pd.DataFrame(data)
            df['time_tag'] = pd.to_datetime(df['time_tag'])
            df['kp_index'] = pd.to_numeric(df['kp_index'], errors='coerce')
            return df
        except Exception as e:
            print(f"Error fetching geomagnetic data: {e}")
            return None
    
    def get_solar_flares(self, start_date, end_date):
        """Fetch solar flare events from NASA DONKI"""
        try:
            url = f"{self.nasa_donki_url}/FLR"
            params = {
                'startDate': start_date.strftime('%Y-%m-%d'),
                'endDate': end_date.strftime('%Y-%m-%d'),
                'api_key': self.nasa_api_key
            }
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            return pd.DataFrame(data) if data else None
        except Exception as e:
            print(f"Error fetching solar flares: {e}")
            return None
    
    def get_cme_data(self, start_date, end_date):
        """Fetch Coronal Mass Ejection data"""
        try:
            url = f"{self.nasa_donki_url}/CME"
            params = {
                'startDate': start_date.strftime('%Y-%m-%d'),
                'endDate': end_date.strftime('%Y-%m-%d'),
                'api_key': self.nasa_api_key
            }
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            return pd.DataFrame(data) if data else None
        except Exception as e:
            print(f"Error fetching CME data: {e}")
            return None
    
    def get_xray_flux(self):
        """Fetch X-ray flux data (GOES satellite)"""
        try:
            url = f"{self.noaa_base_url}/goes/primary/xrays-7-day.json"
            response = requests.get(url, timeout=10)
            data = response.json()
            df = pd.DataFrame(data)
            df['time_tag'] = pd.to_datetime(df['time_tag'])
            
            # Convert flux values
            if 'flux' in df.columns:
                df['flux'] = pd.to_numeric(df['flux'], errors='coerce')
            
            return df
        except Exception as e:
            print(f"Error fetching X-ray flux: {e}")
            return None
    
    def get_proton_flux(self):
        """Fetch proton flux data"""
        try:
            url = f"{self.noaa_base_url}/goes/primary/integral-protons-plot-6-hour.json"
            response = requests.get(url, timeout=10)
            data = response.json()
            df = pd.DataFrame(data)
            df['time_tag'] = pd.to_datetime(df['time_tag'])
            return df
        except Exception as e:
            print(f"Error fetching proton flux: {e}")
            return None
    
    def get_magnetometer_data(self):
        """Fetch magnetometer data"""
        try:
            url = f"{self.noaa_base_url}/goes/primary/magnetometers-7-day.json"
            response = requests.get(url, timeout=10)
            data = response.json()
            df = pd.DataFrame(data)
            df['time_tag'] = pd.to_datetime(df['time_tag'])
            return df
        except Exception as e:
            print(f"Error fetching magnetometer data: {e}")
            return None
    
    def collect_all_data(self):
        """Collect all available data sources"""
        print("Collecting space weather data from multiple sources...\n")
        
        data_dict = {}
        
        # Real-time data
        data_dict['solar_wind'] = self.get_solar_wind_data()
        data_dict['geomagnetic'] = self.get_geomagnetic_data()
        data_dict['xray'] = self.get_xray_flux()
        data_dict['proton'] = self.get_proton_flux()
        data_dict['magnetometer'] = self.get_magnetometer_data()
        
        # Historical events (last 30 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        data_dict['flares'] = self.get_solar_flares(start_date, end_date)
        data_dict['cme'] = self.get_cme_data(start_date, end_date)
        
        # Print summary
        for key, df in data_dict.items():
            if df is not None:
                print(f"✓ {key.upper()}: {len(df)} records")
            else:
                print(f"✗ {key.upper()}: No data available")
        
        return data_dict

if __name__ == "__main__":
    collector = SpaceWeatherDataCollector()
    all_data = collector.collect_all_data()
