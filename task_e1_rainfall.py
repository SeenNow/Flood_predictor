import pickle
from sklearn.ensemble import RandomForestClassifier
import config

def run():
    print("Starting Task E1: Rainfall Model...")
    with open(config.TRAIN_FILE, 'rb') as f:
        X_train, y_train = pickle.load(f)
    
    features = ['Rainfall_mm', 'Humidity_pct', 'Temperature_c', 'Rainfall_Intensity']
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train[features], y_train)
    
    with open(config.MODEL_RAIN_FILE, 'wb') as f:
        pickle.dump(model, f)
    print("Rainfall model trained.")

if __name__ == "__main__":
    run()
