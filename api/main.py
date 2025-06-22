# API for risk prediction using FastAPI
from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

# Load model (update path as needed)
# model = joblib.load('../models/model.pkl')

@app.get('/')
def read_root():
    return {"message": "Risk Predictor API"}

# Add prediction endpoint here
