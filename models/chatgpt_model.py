"""
Melodifestivalen - träningsscript för att förutsäga placering (0=ej topp2, 1=tvåa, 2=etta)

Detta script är designat för gymnasieelever och gör följande:
- Läser in en CSV med features för låtar och en kolumn "Placering" (0,1,2).
- Förbehandlar datan (enkla steg: ta bort NaN, skala features).
- Delar data i tränings- och testset.
- Bygger och tränar ett enkelt neuralt nätverk i TensorFlow/Keras.
- Utvärderar modellen och visar classification report + confusion matrix.
- Sparar modellen som HDF5-fil.

Instruktioner:
1. Placera er CSV i samma mapp och döp den till "melodifestivalen.csv", eller ange en annan sökväg i variabeln CSV_FIL.
   Förväntade kolumner: Key, BPM, Energy, Danceability, Happiness, Acousticness, Instrumentalness, Liveness, Speechiness, Placering
2. Installera beroenden:
   pip install pandas scikit-learn tensorflow
3. Kör: python Melodifestivalen_AI_modell.py
"""

import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.datasets import make_classification

CSV_FIL = "melodifestivalen.csv"
RANDOM_STATE = 42
TEST_SIZE = 0.2
EPOCHS = 60
BATCH_SIZE = 16

np.random.seed(RANDOM_STATE)
tf.random.set_seed(RANDOM_STATE)

EXPECTED_COLS = ["Key", "BPM", "Energy", "Danceability", "Happiness", "Acousticness", 
                 "Instrumentalness", "Liveness", "Speechiness", "Placering"]

def generate_synthetic_csv(path: str, n_samples: int = 200, random_state: int = RANDOM_STATE):
    X, y = make_classification(n_samples=n_samples,
                               n_features=9,
                               n_informative=6,
                               n_redundant=1,
                               n_classes=3,
                               weights=[0.6, 0.25, 0.15],
                               random_state=random_state)

    df = pd.DataFrame(X, columns=["_f" + str(i) for i in range(9)])
    df["Key"] = (np.abs(df["_f0"]) * 3).astype(int) % 12
    df["BPM"] = (60 + (np.abs(df["_f1"]) * 40)).astype(int)
    df["Energy"] = np.clip(np.abs(df["_f2"]) / 3.0, 0, 1)
    df["Danceability"] = np.clip(np.abs(df["_f3"]) / 3.0, 0, 1)
    df["Happiness"] = np.clip((df["_f4"] + 3) / 6.0, 0, 1)
    df["Acousticness"] = np.clip(np.abs(df["_f5"]) / 3.0, 0, 1)
    df["Instrumentalness"] = np.clip(np.abs(df["_f6"]) / 3.0, 0, 1)
    df["Liveness"] = np.clip(np.abs(df["_f7"]) / 3.0, 0, 1)
    df["Speechiness"] = np.clip(np.abs(df["_f8"]) / 3.0, 0, 1)

    df = df[["Key", "BPM", "Energy", "Danceability", "Happiness", "Acousticness",
             "Instrumentalness", "Liveness", "Speechiness"]]
    df["Placering"] = y

    df.to_csv(path, index=False)
    print(f"Genererade syntetisk CSV för test: {path} (rader={n_samples})")
    return df

if not os.path.exists(CSV_FIL):
    print(f"CSV-fil '{CSV_FIL}' hittades inte. Skapar syntetisk testfil.")
    df = generate_synthetic_csv(CSV_FIL, n_samples=300)
else:
    df = pd.read_csv(CSV_FIL)
    print(df.head())

missing = [c for c in EXPECTED_COLS if c not in df.columns]
if missing:
    raise ValueError("Följande förväntade kolumner saknas i CSV: " + ", ".join(missing))

df = df.dropna()
X = df[[c for c in EXPECTED_COLS if c != "Placering"]].copy()
y = df["Placering"].astype(int).copy()

try:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE)
except ValueError:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

num_features = X_train_scaled.shape[1]
num_classes = len(np.unique(y_train))

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(num_features,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()
history = model.fit(X_train_scaled, y_train, validation_split=0.1, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=2)

loss, acc = model.evaluate(X_test_scaled, y_test, verbose=0)
print(f"\nTest loss: {loss:.4f}  Test accuracy: {acc:.4f}")

y_prob = model.predict(X_test_scaled)
y_pred = np.argmax(y_prob, axis=1)

print("\nClassification report (på testsetet):")
print(classification_report(y_test, y_pred, digits=4))
print("Confusion matrix:")
print(confusion_matrix(y_test, y_pred))

n_show = min(10, len(X_test))
for i in range(n_show):
    row = X_test.iloc[i]
    true_label = int(y_test.iloc[i])
    probs = y_prob[i]
    pred_label = int(y_pred[i])
    prob_str = ", ".join([f"{p:.3f}" for p in probs])
    print(f"Ex {i+1}: True={true_label}  Pred={pred_label}  Probs=[{prob_str}]  Features={row.to_dict()}")

model.save("melodifestivalen_model.h5")
print("Modell sparad till melodifestivalen_model.h5")
