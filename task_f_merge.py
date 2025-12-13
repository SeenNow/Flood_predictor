import pickle
import numpy as np
import pandas as pd
import config

def run():
    print("Starting Task F: Merging Models...")
    with open(config.TEST_FILE, 'rb') as f:
        X_test, y_test = pickle.load(f)
    with open(config.MODEL_RAIN_FILE, 'rb') as f:
        model_rain = pickle.load(f)
    with open(config.MODEL_WATER_FILE, 'rb') as f:
        model_water = pickle.load(f)
        
    rain_feats = ['Rainfall_mm', 'Humidity_pct', 'Temperature_c', 'Rainfall_Intensity']
    water_feats = ['Water_level_m', 'Water_Rise_Rate']
    
    # Ensemble Prediction
    pred_rain = model_rain.predict_proba(X_test[rain_feats])
    pred_water = model_water.predict_proba(X_test[water_feats])
    final_prob = (pred_rain + pred_water) / 2
    final_pred = np.argmax(final_prob, axis=1)
    
    # Save results with metadata
    results = X_test[['Date_Time', 'State']].copy()
    results['Actual'] = y_test
    results['Predicted'] = final_pred
    
    results.to_csv(config.PREDICTIONS_FILE, index=False)
    print("Predictions merged and saved.")

if __name__ == "__main__":
    run()
