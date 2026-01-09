"""
train_model.py

Tränar ett neuralt nätverk för att förutsäga Melodifestival-placeringar
som tre klasser: 0 (sämst), 1 (näst bäst), 2 (bäst)
"""

import os
import numpy as np
import pandas as pd
import tensorflow as tf
from keras import layers, models, callbacks, optimizers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# --------------------------
# Inställningar för stabilitet
# --------------------------
SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)

FEATURE_COLUMNS = [
    'Key', 'BPM', 'Energy', 'Danceability', 'Happiness',
    'Acousticness', 'Instrumentalness', 'Liveness', 'Speechiness'
]
TARGET_COLUMN = 'Placering'

MODEL_DIR = 'saved_model'
SCALER_PATH = 'saved_scaler.gz'

# ---------------------------
# Ladda & städa data
# ---------------------------
def load_and_clean(csv_path):
    df = pd.read_csv(csv_path)
    df.columns = [c.strip() for c in df.columns]

    # Ta bort skräp
    df = df.replace('--------------------------------------', np.nan)
    df = df.dropna(subset=FEATURE_COLUMNS + [TARGET_COLUMN])

    # Omvandla till rätt typer
    df[FEATURE_COLUMNS] = df[FEATURE_COLUMNS].astype(float)
    df[TARGET_COLUMN] = df[TARGET_COLUMN].astype(int)

    return df

# ---------------------------
# Model (optimerad, mindre, stabil)
# ---------------------------
def build_model(input_dim, lr=5e-4):
    model = models.Sequential([
        layers.Input(shape=(input_dim,)),
        layers.Dense(32, activation='relu'),
        layers.Dense(16, activation='relu'),
        layers.Dense(3, activation='softmax')  # 3 klasser: 0,1,2
    ])

    model.compile(
        optimizer=optimizers.Adam(learning_rate=lr),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

# ---------------------------
# Train-funktion
# ---------------------------
def train(csv_path, epochs=300, batch_size=32):
    df = load_and_clean(csv_path)

    # --------- FIX: korrekt scaler här ----------
    X_raw = df[FEATURE_COLUMNS].values
    y = df[TARGET_COLUMN].values

    scaler = StandardScaler()
    X = scaler.fit_transform(X_raw)  # <--- SCALER fixad och korrekt

    # Dela i train/val
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=SEED
    )

    model = build_model(X.shape[1])

    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR, exist_ok=True)

    # Callbacks gör träningen stabil
    ckpt = callbacks.ModelCheckpoint(
        os.path.join(MODEL_DIR, 'best_model.keras'),
        monitor='val_accuracy',
        save_best_only=True,
        mode='max'
    )
    es = callbacks.EarlyStopping(
        monitor='val_accuracy',
        patience=15,
        restore_best_weights=True
    )
    rlrop = callbacks.ReduceLROnPlateau(
        monitor='val_accuracy',
        patience=5,
        factor=0.5,
        min_lr=1e-6,
        mode='max'
    )

    # --------- TRÄNA ----------
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[ckpt, es, rlrop],
        verbose=2
    )

    # Spara modell + scaler
    model.save(os.path.join(MODEL_DIR, 'final_model.keras'))
    joblib.dump(scaler, SCALER_PATH)

    # --------- RESULTAT ----------
    final_loss = history.history['loss'][-1]
    final_val_loss = history.history['val_loss'][-1]
    final_acc = history.history['accuracy'][-1]
    final_val_acc = history.history['val_accuracy'][-1]

    print("\n==============================")
    print("  SLUTRESULTAT PÅ VALIDERING")
    print("==============================")
    print(f"Final Loss (train): {final_loss:.4f}")
    print(f"Final Loss (val):   {final_val_loss:.4f}")
    print(f"Final Accuracy (train): {final_acc:.4f}")
    print(f"Final Accuracy (val):   {final_val_acc:.4f}")
    print("\nKlart! Modellen sparad och scaler sparad.")


# ---------------------------
# Main
# ---------------------------
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True)
    parser.add_argument('--epochs', type=int, default=300)
    parser.add_argument('--batch_size', type=int, default=16)
    args = parser.parse_args()

    train(args.data, args.epochs, args.batch_size)
