import pandas as pd
from tensorflow import keras
import joblib 

import tensorflow as tf
import numpy as np
from data_preprocessing import load_yearly_data, split_features_targets
from sklearn.preprocessing import MinMaxScaler

# Ladda in data
years = load_yearly_data("melodifestival.csv")

# Välj vilket år du vill testa
year_to_test = 5  # ändra detta värde!

# Ladda modellen
model = tf.keras.models.load_model(f"model_year_{year_to_test}.h5")

# Förbered testdata
test_year = years[year_to_test - 1]
X_test, y_test = split_features_targets(test_year)

# Normalisera på nytt
scaler = MinMaxScaler()
X_test = scaler.fit_transform(X_test)

# Gör förutsägelser
predictions = model.predict(X_test)

# Skriv ut några exempel
print("\nExempel på förutsägelser:")
for i in range(min(10, len(predictions))):
    print(f"Riktig placering: {y_test[i]:.0f} | Förutsagd: {predictions[i][0]:.2f}")
