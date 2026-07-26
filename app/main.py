from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pickle
import os

from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime
import pytz

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

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

    prediction = model.predict(
        [[request.distance_km, request.traffic_level]]
    )

    fare = round(float(prediction[0]), 2)

    try:
        response = supabase.table("ride_predictions").insert({
            "distance_km": request.distance_km,
            "traffic_level": request.traffic_level,
            "predicted_fare": f"RM {fare}"
        }).execute()

        print("Supabase response:", response)

    except Exception as e:
        print("Supabase error:", e)

    return {
        "predicted_fare": f"RM {fare}"
    }

@app.get("/history")
def history():

    response = supabase \
        .table("ride_predictions") \
        .select("*") \
        .execute()

    malaysia = pytz.timezone("Asia/Kuala_Lumpur")

    for item in response.data:
        utc_time = datetime.fromisoformat(
            item["created_at"].replace("Z", "+00:00")
        )

        malaysia_time = utc_time.astimezone(malaysia)

        item["created_at"] = malaysia_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    return response.data