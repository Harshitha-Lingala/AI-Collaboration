import numpy as np
import pandas as pd

from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

import matplotlib.pyplot as plt
import seaborn as sns

# Load the Boston Housing dataset from scikit-learn
boston = load_boston()

# Create a pandas DataFrame with the feature names as columns
data = pd.DataFrame(data=boston.data, columns=boston.feature_names)

# Add the target column (house prices) to the DataFrame
data['PRICE'] = boston.target

# Display the first few rows of the dataset
print(data.head())

# Check for any missing data in the dataset
print(data.isnull().sum())

# Plot a heatmap of the correlation matrix to visualize the relationships between features and target
plt.figure(figsize=(12, 8))
correlation_matrix = data.corr().round(2)
sns.heatmap(data=correlation_matrix, annot=True, cmap='coolwarm')

# Let's select a few features (LSTAT, RM, PTRATIO) to use in our model
X = data[['LSTAT', 'RM', 'PTRATIO']]
y = data['PRICE']

# Split the dataset into training and test sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Linear Regression model on the training data
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Evaluate the model using Mean Squared Error (MSE) and R-squared score
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Mean Squared Error (MSE): {mse}')
print(f'R-squared score: {r2}')

# Save the trained model using pickle for future use
import pickle

with open('house_price_prediction_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Model saved successfully!")