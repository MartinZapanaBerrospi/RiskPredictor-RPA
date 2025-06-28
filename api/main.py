# API for risk prediction using FastAPI
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
import joblib
import pandas as pd
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import os
import json
import uuid
import csv
import subprocess
import sys
from utils.reporte_profesional import generar_reporte_pdf
from utils.email_mailhog import enviar_reporte_mailhog

app = FastAPI()

# Load model (update path as needed)
# model = joblib.load('../models/model.pkl')

# Cargar modelos y encoders
model = joblib.load('models/modelo_xgb_riesgo_general.pkl')
sobrecosto_model = joblib.load('models/modelo_xgb_sobrecosto.pkl')
retraso_model = joblib.load('models/modelo_xgb_retraso.pkl')
le_tipo = joblib.load('models/le_tipo_proyecto.pkl')
le_metodologia = joblib.load('models/le_metodologia.pkl')
le_complejidad = joblib.load('models/le_complejidad.pkl')
le_experiencia = joblib.load('models/le_experiencia.pkl')
mlb = joblib.load('models/mlb_tecnologias.pkl')
le_riesgo = joblib.load('models/le_riesgo_general.pkl')

class ProyectoInput(BaseModel):
    tipo_proyecto: str
    metodologia: str
    duracion_estimacion: int
    presupuesto_estimado: int
    numero_recursos: int
    tecnologias: str  # Coma separada
    complejidad: str
    experiencia_equipo: int
    hitos_clave: int

class EnvioReporteRequest(BaseModel):
    destinatario: str
    proyecto: dict
    prediccion: Optional[dict] = None

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
    X_pred['metodologia_enc'] = le_metodologia.transform(X_pred['metodologia'])
    X_pred['complejidad_enc'] = le_complejidad.transform(X_pred['complejidad'])
    X_pred['experiencia_equipo_enc'] = X_pred['experiencia_equipo']
    tec_matrix = mlb.transform([X_pred.loc[0, 'tecnologias'].split(',')])
    tec_df = pd.DataFrame(tec_matrix, columns=[f'tec_{t}' for t in mlb.classes_])
    for col in tec_df.columns:
        X_pred[col] = tec_df[col].values
    features = [
        'tipo_proyecto_enc', 'metodologia_enc', 'duracion_estimacion', 'presupuesto_estimado', 'numero_recursos',
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

PROY_EJEC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/proyectos_ejecucion.csv'))

# Helper: get fieldnames for proyectos en ejecución
PROY_EJEC_FIELDS = [
    'id', 'tipo_proyecto', 'metodologia', 'duracion_estimacion', 'presupuesto_estimado', 'numero_recursos',
    'tecnologias', 'complejidad', 'experiencia_equipo', 'hitos_clave'
]

@app.post('/proyectos-ejecucion')
def add_proyecto_ejecucion(proyecto: dict):
    # Generar un id único
    proyecto_id = str(uuid.uuid4())
    row = {'id': proyecto_id, **proyecto}
    # Escribir en el CSV (append)
    file_exists = os.path.exists(PROY_EJEC_PATH)
    with open(PROY_EJEC_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=PROY_EJEC_FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
    return {"status": "ok", "id": proyecto_id}

@app.get('/proyectos-ejecucion')
def list_proyectos_ejecucion():
    if not os.path.exists(PROY_EJEC_PATH):
        return []
    with open(PROY_EJEC_PATH, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

@app.get('/proyectos-ejecucion/{proy_id}')
def get_proyecto_ejecucion(proy_id: str):
    if not os.path.exists(PROY_EJEC_PATH):
        raise HTTPException(status_code=404, detail='No hay proyectos en ejecución')
    with open(PROY_EJEC_PATH, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['id'] == proy_id:
                return row
    raise HTTPException(status_code=404, detail='Proyecto no encontrado')

@app.put('/proyectos-ejecucion/{proy_id}')
def update_proyecto_ejecucion(proy_id: str, datos: dict):
    if not os.path.exists(PROY_EJEC_PATH):
        raise HTTPException(status_code=404, detail='No hay proyectos en ejecución')
    proyectos = []
    updated = False
    with open(PROY_EJEC_PATH, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['id'] == proy_id:
                row.update(datos)
                updated = True
            proyectos.append(row)
    if not updated:
        raise HTTPException(status_code=404, detail='Proyecto no encontrado')
    with open(PROY_EJEC_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=PROY_EJEC_FIELDS)
        writer.writeheader()
        writer.writerows(proyectos)
    return {"status": "ok"}

@app.post('/proyectos-ejecucion/{proy_id}/finalizar')
def finalizar_proyecto(proy_id: str, datos_finales: dict):
    # Mover a synthetic_data_with_outputs.csv
    SYNTH_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/synthetic_data_with_outputs.csv'))
    # Leer proyectos en ejecución
    if not os.path.exists(PROY_EJEC_PATH):
        raise HTTPException(status_code=404, detail='No hay proyectos en ejecución')
    proyectos = []
    finalizado = None
    with open(PROY_EJEC_PATH, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['id'] == proy_id:
                finalizado = {**row, **datos_finales}
            else:
                proyectos.append(row)
    if not finalizado:
        raise HTTPException(status_code=404, detail='Proyecto no encontrado')
    # Guardar el resto de proyectos en ejecución
    with open(PROY_EJEC_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=PROY_EJEC_FIELDS)
        writer.writeheader()
        writer.writerows(proyectos)
    # Agregar a synthetic_data_with_outputs.csv
    synth_fields = [
        'tipo_proyecto', 'metodologia', 'duracion_estimacion', 'presupuesto_estimado', 'numero_recursos',
        'tecnologias', 'complejidad', 'experiencia_equipo', 'hitos_clave',
        'costo_real', 'duracion_real', 'riesgo_general'
    ]
    file_exists = os.path.exists(SYNTH_PATH)
    with open(SYNTH_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=synth_fields)
        if not file_exists:
            writer.writeheader()
        writer.writerow({k: finalizado.get(k, '') for k in synth_fields})
    return {"status": "ok"}

@app.post('/reentrenar-modelo')
def reentrenar_modelo(background_tasks: BackgroundTasks):
    """
    Ejecuta el script de entrenamiento de modelos y devuelve el estado y la salida.
    """
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/train_xgboost.py'))
    python_exe = sys.executable  # Usar el mismo Python del backend
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    try:
        result = subprocess.run([python_exe, script_path], capture_output=True, text=True, check=True, cwd=project_root)
        # Recargar modelos y encoders
        global model, sobrecosto_model, retraso_model, le_tipo, le_metodologia, le_complejidad, le_experiencia, mlb, le_riesgo
        model = joblib.load('models/modelo_xgb_riesgo_general.pkl')
        sobrecosto_model = joblib.load('models/modelo_xgb_sobrecosto.pkl')
        retraso_model = joblib.load('models/modelo_xgb_retraso.pkl')
        le_tipo = joblib.load('models/le_tipo_proyecto.pkl')
        le_metodologia = joblib.load('models/le_metodologia.pkl')
        le_complejidad = joblib.load('models/le_complejidad.pkl')
        le_experiencia = joblib.load('models/le_experiencia.pkl')
        mlb = joblib.load('models/mlb_tecnologias.pkl')
        le_riesgo = joblib.load('models/le_riesgo_general.pkl')
        return {"status": "ok", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "output": e.stdout + '\n' + e.stderr}

@app.post('/generar-reporte')
def generar_reporte(proyecto: ProyectoInput):
    # Predecir riesgo igual que en /predict
    X_pred = pd.DataFrame([proyecto.dict()])
    X_pred['tipo_proyecto_enc'] = le_tipo.transform(X_pred['tipo_proyecto'])
    X_pred['metodologia_enc'] = le_metodologia.transform(X_pred['metodologia'])
    X_pred['complejidad_enc'] = le_complejidad.transform(X_pred['complejidad'])
    X_pred['experiencia_equipo_enc'] = X_pred['experiencia_equipo']
    tec_matrix = mlb.transform([X_pred.loc[0, 'tecnologias'].split(',')])
    tec_df = pd.DataFrame(tec_matrix, columns=[f'tec_{t}' for t in mlb.classes_])
    for col in tec_df.columns:
        X_pred[col] = tec_df[col].values
    features = [
        'tipo_proyecto_enc', 'metodologia_enc', 'duracion_estimacion', 'presupuesto_estimado', 'numero_recursos',
        'complejidad_enc', 'experiencia_equipo_enc', 'hitos_clave'
    ] + list(tec_df.columns)
    for col in features:
        if col not in X_pred:
            X_pred[col] = 0
    X_pred = X_pred[features]
    pred = model.predict(X_pred)[0]
    pred_label = le_riesgo.inverse_transform([pred])[0]
    pred_proba = model.predict_proba(X_pred)[0]
    # Preparar datos para el reporte
    proyecto_dict = {
        "Tipo de proyecto": proyecto.tipo_proyecto,
        "Metodología": proyecto.metodologia,
        "Duración estimada (meses)": proyecto.duracion_estimacion,
        "Presupuesto estimado (USD)": proyecto.presupuesto_estimado,
        "Número de recursos": proyecto.numero_recursos,
        "Tecnologías": proyecto.tecnologias,
        "Complejidad": proyecto.complejidad,
        "Experiencia del equipo": proyecto.experiencia_equipo,
        "Hitos clave": proyecto.hitos_clave
    }
    prediccion_dict = {
        "riesgo_general": pred_label,
        "probabilidades": {clase: float(proba) for clase, proba in zip(le_riesgo.classes_, pred_proba)}
    }
    # Generar PDF temporal
    pdf_path = f"reporte_riesgo_{uuid.uuid4().hex}.pdf"
    generar_reporte_pdf(proyecto_dict, prediccion_dict, filename=pdf_path)
    # Devolver el PDF como descarga
    return FileResponse(pdf_path, media_type='application/pdf', filename='reporte_riesgo.pdf')

@app.post('/enviar-reporte-mailhog')
def enviar_reporte_mailhog_endpoint(request: EnvioReporteRequest):
    """
    Genera el PDF y lo envía por email usando MailHog (localhost:1025).
    El PDF será idéntico al de descarga, con predicción si es posible.
    """
    ruta_pdf = 'reporte_riesgo.pdf'
    from utils.reporte_profesional import generar_reporte_pdf
    # Si no hay predicción, la calculamos igual que en /generar-reporte
    prediccion = request.prediccion
    if not prediccion and request.proyecto:
        # Simula ProyectoInput
        class Dummy:
            def __init__(self, d):
                self.__dict__ = d
            def dict(self):
                return self.__dict__
        proyecto_obj = Dummy(request.proyecto)
        X_pred = pd.DataFrame([proyecto_obj.dict()])
        X_pred['tipo_proyecto_enc'] = le_tipo.transform(X_pred['tipo_proyecto'])
        X_pred['metodologia_enc'] = le_metodologia.transform(X_pred['metodologia'])
        X_pred['complejidad_enc'] = le_complejidad.transform(X_pred['complejidad'])
        X_pred['experiencia_equipo_enc'] = X_pred['experiencia_equipo']
        tec_matrix = mlb.transform([X_pred.loc[0, 'tecnologias'].split(',')])
        tec_df = pd.DataFrame(tec_matrix, columns=[f'tec_{t}' for t in mlb.classes_])
        for col in tec_df.columns:
            X_pred[col] = tec_df[col].values
        features = [
            'tipo_proyecto_enc', 'metodologia_enc', 'duracion_estimacion', 'presupuesto_estimado', 'numero_recursos',
            'complejidad_enc', 'experiencia_equipo_enc', 'hitos_clave'
        ] + list(tec_df.columns)
        for col in features:
            if col not in X_pred:
                X_pred[col] = 0
        X_pred = X_pred[features]
        pred = model.predict(X_pred)[0]
        pred_label = le_riesgo.inverse_transform([pred])[0]
        pred_proba = model.predict_proba(X_pred)[0]
        sobrecosto_proba = sobrecosto_model.predict_proba(X_pred)[0][1]
        retraso_proba = retraso_model.predict_proba(X_pred)[0][1]
        prediccion = {
            "riesgo_general": pred_label,
            "probabilidades": {clase: float(proba) for clase, proba in zip(le_riesgo.classes_, pred_proba)},
            "probabilidad_sobrecosto": float(sobrecosto_proba),
            "probabilidad_retraso": float(retraso_proba)
        }
    generar_reporte_pdf(request.proyecto, prediccion or {}, filename=ruta_pdf)
    asunto = "Reporte de Evaluación de Riesgo"
    cuerpo = "Adjunto encontrará el reporte PDF generado automáticamente."
    enviar_reporte_mailhog(request.destinatario, asunto, cuerpo, ruta_pdf)
    return {"mensaje": "Reporte enviado correctamente a MailHog"}

@app.delete('/proyectos-ejecucion/{proy_id}')
def delete_proyecto_ejecucion(proy_id: str):
    if not os.path.exists(PROY_EJEC_PATH):
        raise HTTPException(status_code=404, detail='No hay proyectos en ejecución')
    proyectos = []
    deleted = False
    with open(PROY_EJEC_PATH, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['id'] == proy_id:
                deleted = True
                continue
            proyectos.append(row)
    if not deleted:
        raise HTTPException(status_code=404, detail='Proyecto no encontrado')
    with open(PROY_EJEC_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=PROY_EJEC_FIELDS)
        writer.writeheader()
        writer.writerows(proyectos)
    return {"status": "ok"}
