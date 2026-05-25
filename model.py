import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

# Load dataset
data = pd.read_csv("heat_data.csv")

# Features and labels
X = data[["temperature", "humidity"]]
y = data["risk"]

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model
pickle.dump(model, open("heat_model.pkl", "wb"))

print("AI Model Trained Successfully!")