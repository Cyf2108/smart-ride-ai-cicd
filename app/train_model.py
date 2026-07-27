import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

data = {
    "distance_km":   [2, 5, 10, 3, 8, 15, 20, 7, 12, 1, 5],
    "traffic_level": [1, 2, 3, 1, 2, 3, 3, 2, 1, 3, 5],
    "fare":          [6, 7, 20, 7, 18, 40, 45, 12, 22, 5, 10]
}

df = pd.DataFrame(data)

X = df[["distance_km", "traffic_level"]]
y = df["fare"]

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("AI model trained and saved as model.pkl")