import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
import config

def run():
    print("Starting Task D: Train/Test Split...")
    df = pd.read_csv(config.FEATURE_FILE)
    
    # X includes State/Date_Time for tracking metadata
    X = df.drop(columns=['Flood_alert'])
    y = df['Flood_alert']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    with open(config.TRAIN_FILE, 'wb') as f:
        pickle.dump((X_train, y_train), f)
    with open(config.TEST_FILE, 'wb') as f:
        pickle.dump((X_test, y_test), f)
    print("Data split complete.")

if __name__ == "__main__":
    run()
