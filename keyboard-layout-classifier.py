import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


# Load datasets
qwerty_data = pd.read_csv('qwerty_dataset.csv')
dvorak_data = pd.read_csv('dvorak_dataset.csv')

# Add labels to each dataset (0 for QWERTY, 1 for Dvorak)
qwerty_data['label'] = 0
dvorak_data['label'] = 1

# Combine datasets
data = pd.concat([qwerty_data, dvorak_data])

# Split data into features and labels
X = data[['home_row_score', 'bigram_bonus', 'frequency_score', 'movement_cost']]
y = data['label']

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

joblib.dump(scaler, 'scaler.pkl')

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Define the neural network model
def create_model(input_shape):
    model = Sequential([
        Dense(64, activation='relu', input_shape=(input_shape,)),
        Dropout(0.5),
        Dense(32, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

input_shape = X_train.shape[1]
model = create_model(input_shape)

# Train the model
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)

# Evaluate the model on the test set
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Accuracy: {accuracy:.2f}')

# Save the trained model
model.save('keyboard_layout_classifier.h5')
