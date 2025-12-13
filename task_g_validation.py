import pandas as pd
from sklearn.metrics import classification_report, accuracy_score
import config

def run():
    print("Starting Task G: Validation...")
    results = pd.read_csv(config.PREDICTIONS_FILE)
    acc = accuracy_score(results['Actual'], results['Predicted'])
    report = classification_report(results['Actual'], results['Predicted'])
    
    output = f"Accuracy: {acc}\n\n{report}"
    with open(config.RESULTS_FILE, "w") as f:
        f.write(output)
    print(output)

if __name__ == "__main__":
    run()
