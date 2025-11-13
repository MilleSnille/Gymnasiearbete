import pandas as pd
import numpy as np

def load_yearly_data(csv_path):
    """
    Läser in CSV-filen och delar upp datan år för år.
    Returnerar en lista där varje element är en DataFrame för ett år.
    """
    df = pd.read_csv(csv_path)
    
    years = []
    current_year = []

    for _, row in df.iterrows():
        if str(row['Key']).startswith('---'):
            # Nytt år
            if current_year:
                years.append(pd.DataFrame(current_year))
                current_year = []
        else:
            current_year.append(row)
    
    # Lägg till sista året
    if current_year:
        years.append(pd.DataFrame(current_year))

    # Konvertera alla värden till numeriska (float)
    for i in range(len(years)):
        years[i] = years[i].apply(pd.to_numeric, errors='coerce').dropna()

    print(f"Antal år hittade: {len(years)}")
    return years

def split_features_targets(df):
    """Delar upp features (X) och target (y) från ett DataFrame."""
    X = df.drop(columns=['Placering']).values
    y = df['Placering'].values
    return X, y
