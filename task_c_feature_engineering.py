import pandas as pd
import config

def run():
    print("Starting Task C: Feature Engineering...")
    df = pd.read_csv(config.CLEAN_FILE)
    
    # Create derived features
    df['Rainfall_Intensity'] = df['Rainfall_mm'] / 24.0
    df['Water_Rise_Rate'] = df['Water_level_m'] * 1.1
    
    df.to_csv(config.FEATURE_FILE, index=False)
    print("Feature Engineering complete.")

if __name__ == "__main__":
    run()
