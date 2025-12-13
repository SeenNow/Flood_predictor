import pandas as pd
import numpy as np
import config  # Import shared settings

def run():
    print("Starting Task A: Data Ingestion...")
    try:
        df = pd.read_csv(config.DATA_FILE)
        print(f"Loaded existing data: {len(df)} rows.")
    except FileNotFoundError:
        print("Generating dummy dataset for 2020-2025...")
        dates = pd.date_range(start='2020-01-01', end='2025-12-31', freq='D')
        data_list = []
        states = ['Kelantan', 'Johor', 'Pahang']
        
        for date in dates:
            for state in states:
                is_monsoon = date.month in [11, 12, 1]
                rain_base = 100 if is_monsoon else 20
                row = {
                    'Date_Time': date,
                    'State': state,
                    'Rainfall_mm': np.random.uniform(0, rain_base + 100),
                    'Humidity_pct': np.random.uniform(60, 100),
                    'Temperature_c': np.random.uniform(24, 34),
                    'Wind_speed_ms': np.random.uniform(0, 20),
                    'Water_level_m': np.random.uniform(0, 10 + (5 if is_monsoon else 0)),
                    'Flood_alert': np.random.choice([0, 1, 2], p=[0.8, 0.15, 0.05])
                }
                data_list.append(row)
        
        df = pd.DataFrame(data_list)
        df.to_csv(config.DATA_FILE, index=False)
        print(f"Ingested {len(df)} rows.")

if __name__ == "__main__":
    run()
