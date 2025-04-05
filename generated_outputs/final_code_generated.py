# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Load the dataset
data = pd.read_csv('iris.csv')

# Check for missing values and impute if necessary
if data.isnull().values.any():
    imputer = SimpleImputer(strategy='mean')
    data = imputer.fit_transform(data)

# Split the dataset into features and target variable
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Encode categorical data if applicable

# Normalize or scale the data
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the models
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)

knn = KNeighborsClassifier()
knn.fit(X_train, y_train)

dtree = DecisionTreeClassifier()
dtree.fit(X_train, y_train)

# Make predictions
y_pred_log_reg = log_reg.predict(X_test)
y_pred_knn = knn.predict(X_test)
y_pred_dtree = dtree.predict(X_test)

# Evaluate the models
acc_log_reg = accuracy_score(y_test, y_pred_log_reg)
acc_knn = accuracy_score(y_test, y_pred_knn)
acc_dtree = accuracy_score(y_test, y_pred_dtree)

print(f"Logistic Regression Accuracy: {acc_log_reg}")
print(f"K-Nearest Neighbors Accuracy: {acc_knn}")
print(f"Decision Tree Accuracy: {acc_dtree}")
