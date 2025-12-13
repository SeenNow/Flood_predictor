import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import config

def run():
    print("Starting Task H: Visualization...")
    df = pd.read_csv(config.PREDICTIONS_FILE)
    
    df['Date_Time'] = pd.to_datetime(df['Date_Time'])
    df['Year'] = df['Date_Time'].dt.year
    
    # Filter for alerts (1 or 2)
    flood_risks = df[df['Predicted'] > 0]
    
    summary = flood_risks.groupby(['Year', 'State']).size().reset_index(name='Predicted_Flood_Events')
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=summary, x='Year', y='Predicted_Flood_Events', hue='State', palette='viridis')
    plt.title('Predicted Flood Events by Area and Year')
    plt.savefig(config.FIGURE_FILE)
    print(f"Saved plot to {config.FIGURE_FILE}")

if __name__ == "__main__":
    run()
