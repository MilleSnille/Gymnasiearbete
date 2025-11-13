import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense
from keras.models import Sequential, load_model

# 1. Läs in CSV
data = pd.read_csv("melodifestivalen.csv")

# 2. Separera features och labels
X = data[['Key', 'BPM', 'Danceability', 'Happiness', 
          'Acousticness', 'Instrumentalness', 'Liveness', 'Speechiness']]
y = data['Placering']

# 3. Dela upp i träning och test (80-20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4. Skala features
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Spara scaler för senare användning
import joblib
joblib.dump(scaler, "scaler.save")

# 6. One-hot encode labels
y_train_categorical = to_categorical(y_train, num_classes=3)

# 7. Skapa modellen
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    Dense(32, activation='relu'),
    Dense(3, activation='softmax')
])

# 8. Kompilera modellen
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 9. Träna modellen
history = model.fit(
    X_train_scaled, y_train_categorical,
    epochs=50, batch_size=8, validation_split=0.2
)

# 10. Spara modellen
model.save("melodifestivalen_model.h5")
print("Modellen sparad som melodifestivalen_model.h5")

# 11. Spara testdata för test_model.py
test_data = X_test.copy()
test_data['Placering'] = y_test
test_data.to_csv("test_data.csv", index=False)
print("Testdata sparad som test_data.csv")
