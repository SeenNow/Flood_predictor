import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import config

def run():
    print("Starting Task B: Preprocessing...")
    df = pd.read_csv(config.DATA_FILE)
    
    # Filter and clean
    df = df[df['Rainfall_mm'] >= 0].fillna(method='ffill')
    
    # Normalize
    scaler = MinMaxScaler()
    cols_to_norm = ['Rainfall_mm', 'Water_level_m', 'Humidity_pct']
    df[cols_to_norm] = scaler.fit_transform(df[cols_to_norm])
    
    df.to_csv(config.CLEAN_FILE, index=False)
    print("Preprocessing complete.")

if __name__ == "__main__":
    run()
