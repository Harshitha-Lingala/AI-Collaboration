# Import necessary libraries
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
import joblib

# Load the dataset
try:
    data = pd.read_csv('house_prices_dataset.csv')
except FileNotFoundError:
    print("Error: File not found.")
    exit()

# Check if 'price' column exists in the dataset
if 'price' not in data.columns:
    print("Error: 'price' column not found in the dataset.")
    exit()

# Separate features and target variable
X = data.drop('price', axis=1)
y = data['price']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train the model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
print("R^2 Score:", r2)

# Save the model to a file
joblib.dump(model, 'house_price_prediction_model.pkl')
print("Model saved successfully.")

# Example of loading the model for prediction
# loaded_model = joblib.load('house_price_prediction_model.pkl')
# prediction = loaded_model.predict(some_new_data)
# print("Prediction:", prediction)
