from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pickle

app = FastAPI()
model = pickle.load(open("model.pkl", "rb"))

class RideRequest(BaseModel):
    distance_km: float
    traffic_level: int

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r") as f:
        return f.read()

@app.post("/predict")
def predict(request: RideRequest):
    prediction = model.predict([[request.distance_km, request.traffic_level]])
    fare = round(float(prediction[0]), 2)
    return {"predicted_fare": f"RM {fare}"}
