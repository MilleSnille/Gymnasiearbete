import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers   

import tensorflow as tf
from tensorflow import keras
import numpy as np
from data_preprocessing import load_yearly_data, split_features_targets

# Ladda in datan
years = load_yearly_data("melodifestival.csv")

# Loopa över alla år
for i in range(len(years)):
    print(f"\n=== Tränar modell (testar på år {i+1}) ===")
    
    # Dela upp tränings- och testdata
    train_years = [years[j] for j in range(len(years)) if j != i]
    test_year = years[i]

    # Slå ihop träningsåren till en DataFrame
    train_df = train_years[0]
    for ydf in train_years[1:]:
        train_df = train_df._append(ydf, ignore_index=True)

    # Dela upp X/y
    X_train, y_train = split_features_targets(train_df)
    X_test, y_test = split_features_targets(test_year)

    # Normalisera
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Bygg modell
    model = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1)  # För regression
    ])

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    # Träna
    history = model.fit(
        X_train, y_train,
        epochs=100,
        batch_size=8,
        verbose=0,  # sätt till 1 om ni vill se träningen
        validation_split=0.2
    )

    # Spara modellen
    model.save(f"model_year_{i+1}.h5")

    # Testa på det året
    test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)
    print(f"Testår {i+1} — MAE: {test_mae:.2f}")


