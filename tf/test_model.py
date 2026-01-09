import pandas as pd
import joblib
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
from keras.utils import to_categorical

# 1. Läs testdata
test_data = pd.read_csv("test_data.csv")
X_test = test_data[['Key', 'BPM', 'Danceability', 'Happiness', 
                    'Acousticness', 'Instrumentalness', 'Liveness', 'Speechiness']]
y_test = test_data['Placering']

# 2. Ladda scaler och skala testdata
scaler = joblib.load("scaler.save")
X_test_scaled = scaler.transform(X_test)

# 3. One-hot encode labels
y_test_categorical = to_categorical(y_test, num_classes=3)

# 4. Ladda modellen
model = load_model("melodifestivalen_model.h5")

# 5. Utvärdera modellen
test_loss, test_acc = model.evaluate(X_test_scaled, y_test_categorical)
print(f"Test Accuracy: {test_acc:.2f}")

# 6. Prediktioner
predictions = model.predict(X_test_scaled)
predicted_classes = predictions.argmax(axis=1)

# 7. Lägg till prediktioner i testdata och spara
test_data['Prediktion'] = predicted_classes
test_data.to_csv("test_predictions.csv", index=False)
print("Prediktioner sparade i test_predictions.csv")
