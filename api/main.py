# API for risk prediction using FastAPI
from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import json

app = FastAPI()

# Load model (update path as needed)
# model = joblib.load('../models/model.pkl')

# Cargar modelos y encoders
model = joblib.load('models/modelo_xgb_riesgo_general.pkl')
sobrecosto_model = joblib.load('models/modelo_xgb_sobrecosto.pkl')
retraso_model = joblib.load('models/modelo_xgb_retraso.pkl')
le_tipo = joblib.load('models/le_tipo_proyecto.pkl')
le_complejidad = joblib.load('models/le_complejidad.pkl')
le_experiencia = joblib.load('models/le_experiencia.pkl')
mlb = joblib.load('models/mlb_tecnologias.pkl')
le_riesgo = joblib.load('models/le_riesgo_general.pkl')

class ProyectoInput(BaseModel):
    tipo_proyecto: str
    duracion_estimacion: int
    presupuesto_estimado: int
    numero_recursos: int
    tecnologias: str  # Coma separada
    complejidad: str
    experiencia_equipo: int
    hitos_clave: int

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir a ["http://localhost:5173"] si solo usas Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def read_root():
    return {"message": "Risk Predictor API"}

@app.post('/predict')
def predict_riesgo(proyecto: ProyectoInput):
    X_pred = pd.DataFrame([proyecto.dict()])
    X_pred['tipo_proyecto_enc'] = le_tipo.transform(X_pred['tipo_proyecto'])
    X_pred['complejidad_enc'] = le_complejidad.transform(X_pred['complejidad'])
    X_pred['experiencia_equipo_enc'] = X_pred['experiencia_equipo']
    tec_matrix = mlb.transform([X_pred.loc[0, 'tecnologias'].split(',')])
    tec_df = pd.DataFrame(tec_matrix, columns=[f'tec_{t}' for t in mlb.classes_])
    for col in tec_df.columns:
        X_pred[col] = tec_df[col].values
    features = [
        'tipo_proyecto_enc', 'duracion_estimacion', 'presupuesto_estimado', 'numero_recursos',
        'complejidad_enc', 'experiencia_equipo_enc', 'hitos_clave'
    ] + list(tec_df.columns)
    for col in features:
        if col not in X_pred:
            X_pred[col] = 0
    X_pred = X_pred[features]
    # Predicciones
    pred = model.predict(X_pred)[0]
    pred_label = le_riesgo.inverse_transform([pred])[0]
    pred_proba = model.predict_proba(X_pred)[0]
    sobrecosto_proba = sobrecosto_model.predict_proba(X_pred)[0][1]
    retraso_proba = retraso_model.predict_proba(X_pred)[0][1]
    return {
        "riesgo_general": pred_label,
        "probabilidades_riesgo": {clase: float(proba) for clase, proba in zip(le_riesgo.classes_, pred_proba)},
        "probabilidad_sobrecosto": float(sobrecosto_proba),
        "probabilidad_retraso": float(retraso_proba)
    }

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/opciones_formulario.json'))

@app.get('/opciones-formulario')
def get_opciones_formulario():
    with open(DATA_PATH, encoding='utf-8') as f:
        data = json.load(f)
    return JSONResponse(content=data)

@app.put('/opciones-formulario')
def update_opciones_formulario(new_data: dict):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    return {"status": "ok"}
