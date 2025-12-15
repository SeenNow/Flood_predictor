import os

# Base path for NFS
BASE_DIR = "/mnt/data/Flood_predictor"

# Define shared filenames with absolute paths
DATA_FILE = os.path.join(BASE_DIR, "weather_data.csv")
CLEAN_FILE = os.path.join(BASE_DIR, "clean_data.csv")
FEATURE_FILE = os.path.join(BASE_DIR, "features.csv")
TRAIN_FILE = os.path.join(BASE_DIR, "train_data.pkl")
TEST_FILE = os.path.join(BASE_DIR, "test_data.pkl")
MODEL_RAIN_FILE = os.path.join(BASE_DIR, "model_rain.pkl")
MODEL_WATER_FILE = os.path.join(BASE_DIR, "model_water.pkl")
PREDICTIONS_FILE = os.path.join(BASE_DIR, "predictions.csv")
RESULTS_FILE = os.path.join(BASE_DIR, "validation_report.txt")
FIGURE_FILE = os.path.join(BASE_DIR, "flood_prediction_trends.png")