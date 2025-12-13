import pickle
from sklearn.linear_model import LogisticRegression
import config

def run():
    print("Starting Task E2: Water Model...")
    with open(config.TRAIN_FILE, 'rb') as f:
        X_train, y_train = pickle.load(f)
    
    features = ['Water_level_m', 'Water_Rise_Rate']
    model = LogisticRegression()
    model.fit(X_train[features], y_train)
    
    with open(config.MODEL_WATER_FILE, 'wb') as f:
        pickle.dump(model, f)
    print("Water Level model trained.")

if __name__ == "__main__":
    run()
