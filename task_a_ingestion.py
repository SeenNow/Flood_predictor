import requests
import pandas as pd
import numpy as np
import config
import time
from datetime import datetime, timedelta

# Open-Meteo Historical API Endpoint
HISTORICAL_API_URL = "https://archive-api.open-meteo.com/v1/archive"

# Coordinates for Malaysian Towns (Lat, Lon)
LOCATIONS = {
    'Kota Bharu': {'lat': 6.1254, 'lon': 102.2381},
    'Johor Bahru': {'lat': 1.4927, 'lon': 103.7414},
    'Kuantan': {'lat': 3.8077, 'lon': 103.3260},
    'Kuala Lumpur': {'lat': 3.1390, 'lon': 101.6869},
    'George Town': {'lat': 5.4117, 'lon': 100.3327},
    'Ipoh': {'lat': 4.5975, 'lon': 101.0901},
    'Shah Alam': {'lat': 3.0733, 'lon': 101.5185},
    'Malacca City': {'lat': 2.1896, 'lon': 102.2501},
    'Alor Setar': {'lat': 6.1248, 'lon': 100.3678},
    'Kuala Terengganu': {'lat': 5.3302, 'lon': 103.1408},
    'Petaling Jaya': {'lat': 3.1073, 'lon': 101.6067},
    'Seremban': {'lat': 2.7258, 'lon': 101.9424},
    'Kota Kinabalu': {'lat': 5.9804, 'lon': 116.0735},
    'Kuching': {'lat': 1.5535, 'lon': 110.3593},
}

def fetch_historical_data(start_year=2020):
    """
    Fetches real historical weather data from Open-Meteo.
    Automatically adjusts end_date to avoid 'Future Date' errors.
    """
    # Dynamic End Date: Today minus 7 days (to account for Archive API delay)
    end_date_obj = datetime.now() - timedelta(days=7)
    end_date_str = end_date_obj.strftime('%Y-%m-%d')
    start_date_str = f"{start_year}-01-01"

    print(f"Fetching historical data ({start_date_str} to {end_date_str})...")
    
    all_data = []

    for town, coords in LOCATIONS.items():
        print(f" - Querying data for {town}...")
        
        params = {
            'latitude': coords['lat'],
            'longitude': coords['lon'],
            'start_date': start_date_str,
            'end_date': end_date_str,
            # 'daily' variables must be valid for the Archive API
            'daily': 'precipitation_sum,temperature_2m_mean,wind_speed_10m_max', 
            'timezone': 'Asia/Singapore' 
        }
        
        try:
            response = requests.get(HISTORICAL_API_URL, params=params, timeout=20)
            
            # If error, print the exact reason from the API
            if response.status_code != 200:
                print(f"   Error: API returned {response.status_code}")
                print(f"   Reason: {response.text}")
                continue

            data = response.json()
            
            # Process the Daily Data
            daily = data.get('daily', {})
            dates = daily.get('time', [])
            rain = daily.get('precipitation_sum', [])
            temp = daily.get('temperature_2m_mean', [])
            wind = daily.get('wind_speed_10m_max', [])
            # Humidity is often missing in some Archive models, so we simulate it if needed
            # or calculate it from other params if strictly required. 
            # For robustness, we will simulate it here to avoid 400 errors on specific models.
            
            for i in range(len(dates)):
                r_val = rain[i] if rain[i] is not None else 0.0
                
                # --- Labeling Logic (Ground Truth Approximation) ---
                flood_label = 0
                if r_val > 60: flood_label = 1
                if r_val > 100: flood_label = 2
                
                # Water Level Simulation
                water_level = 2.0 + (r_val * 0.05) + np.random.normal(0, 0.2)
                
                row = {
                    'Date_Time': dates[i],
                    'State': town,
                    'Rainfall_mm': r_val,
                    'Temperature_c': temp[i] if temp[i] is not None else 28.0,
                    'Wind_speed_ms': wind[i] if wind[i] is not None else 5.0,
                    'Humidity_pct': np.random.uniform(70, 95), # Fallback for stability
                    'Water_level_m': max(0, water_level),
                    'Flood_alert': flood_label
                }
                all_data.append(row)
            
            # Respect API Rate Limits
            time.sleep(1) 
            
        except Exception as e:
            print(f"   Exception fetching {town}: {e}")
            
    return pd.DataFrame(all_data)

def run():
    # 1. Fetch Real History
    df_history = fetch_historical_data(2020)
    
    if df_history.empty:
        print("CRITICAL ERROR: No historical data fetched. Creating dummy data to prevent crash.")
        # Create minimal dummy data so downstream tasks don't fail
        df_history = pd.DataFrame([{
            'Date_Time': '2024-01-01', 'State': 'Kota Bharu', 
            'Rainfall_mm': 0, 'Temperature_c': 30, 'Wind_speed_ms': 5, 
            'Humidity_pct': 80, 'Water_level_m': 2, 'Flood_alert': 0
        }])

    # 2. Generate Future Placeholder (2026-2027) for Prediction Testing
    print("Projecting future scenarios for 2026-2027...")
    future_data = []
    
    # Use the last available year's data as a baseline
    last_year = df_history['Date_Time'].max()[:4] # Get year string
    df_last_year = df_history[df_history['Date_Time'].str.startswith(last_year)]
    
    for year in [2026, 2027]:
        temp_df = df_last_year.copy()
        # Update year string
        temp_df['Date_Time'] = temp_df['Date_Time'].str.replace(last_year, str(year))
        
        # Add slight climate variation
        temp_df['Rainfall_mm'] = temp_df['Rainfall_mm'] * np.random.uniform(0.9, 1.2)
        
        temp_df['Flood_alert'] = temp_df['Rainfall_mm'].apply(
            lambda x: 2 if x > 100 else (1 if x > 60 else 0)
        )
        future_data.append(temp_df)
        
    df_future = pd.concat(future_data) if future_data else pd.DataFrame()
    
    # 3. Combine and Save
    df_final = pd.concat([df_history, df_future])
    df_final.to_csv(config.DATA_FILE, index=False)
    print(f"Ingestion complete. Saved {len(df_final)} rows to {config.DATA_FILE}.")

if __name__ == "__main__":
    run()