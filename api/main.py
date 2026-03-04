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
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

from utils.reporte_profesional import generar_reporte_pdf
from utils.email_mailhog import enviar_reporte_mailhog

load_dotenv()

app = FastAPI()

# Inicialización de Base de Datos PostgreSQL Persistente
DB_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    if not DB_URL:
        raise Exception("DATABASE_URL no está configurada")
    
    # Supabase requiere conexiones seguras por defecto
    url = DB_URL
    if 'sslmode=' not in url:
        url += '?sslmode=require' if '?' not in url else '&sslmode=require'
        
    return psycopg2.connect(url)

def init_db():
    if not DB_URL:
        print("Advertencia: DATABASE_URL no está configurada. Saltando init_db().")
        return
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Tabla auditoria (Log automático oculto)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS auditoria_predicciones (
                        id SERIAL PRIMARY KEY,
                        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        tipo_proyecto TEXT,
                        metodologia TEXT,
                        duracion_estimacion REAL,
                        presupuesto_estimado REAL,
                        numero_recursos REAL,
                        tecnologias TEXT,
                        complejidad TEXT,
                        experiencia_equipo REAL,
                        hitos_clave REAL,
                        riesgo_general TEXT,
                        probabilidad_sobrecosto REAL,
                        probabilidad_retraso REAL
                    )
                ''')
                
                # Tabla proyectos_ejecucion (para Guardar Proyectos desde el Frontend)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS proyectos_ejecucion (
                        id TEXT PRIMARY KEY,
                        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        tipo_proyecto TEXT,
                        metodologia TEXT,
                        duracion_estimacion REAL,
                        presupuesto_estimado REAL,
                        numero_recursos REAL,
                        tecnologias TEXT,
                        complejidad TEXT,
                        experiencia_equipo REAL,
                        hitos_clave REAL,
                        costo_real REAL,
                        duracion_real REAL,
                        riesgo_general TEXT,
                        estado TEXT DEFAULT 'ejecucion'
                    )
                ''')
                conn.commit()
    except Exception as e:
        print(f"Error inicializando base de datos Postgres: {e}")

init_db()

def _save_audit_log(proyecto_dict: dict, prediction_result: dict):
    if not DB_URL: return
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO auditoria_predicciones (
                        tipo_proyecto, metodologia, duracion_estimacion, presupuesto_estimado, 
                        numero_recursos, tecnologias, complejidad, experiencia_equipo, hitos_clave,
                        riesgo_general, probabilidad_sobrecosto, probabilidad_retraso
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (
                    proyecto_dict.get('tipo_proyecto'), proyecto_dict.get('metodologia'),
                    proyecto_dict.get('duracion_estimacion'), proyecto_dict.get('presupuesto_estimado'),
                    proyecto_dict.get('numero_recursos'), proyecto_dict.get('tecnologias'),
                    proyecto_dict.get('complejidad'), proyecto_dict.get('experiencia_equipo'),
                    proyecto_dict.get('hitos_clave'), prediction_result.get('riesgo_general'),
                    prediction_result.get('probabilidad_sobrecosto', 0), prediction_result.get('probabilidad_retraso', 0)
                ))
                conn.commit()
    except Exception as e:
        print(f"Error saving audit log: {e}")

# Configuración CORS mejorada para permitir peticiones desde GitHub Pages (frontend) en producción
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
origins = [
    "http://localhost:5173",  # React Vite Frontend (Desarrollo local)
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "https://martinzapanaberrospi.github.io" # Frontend de Producción
]

if frontend_url not in origins:
    origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    duracion_estimacion: float
    presupuesto_estimado: float
    numero_recursos: float
    tecnologias: str  # Coma separada
    complejidad: str
    experiencia_equipo: float
    hitos_clave: float

class EnvioReporteRequest(BaseModel):
    destinatario: str
    proyecto: dict
    prediccion: Optional[dict] = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Helper: ejecuta la lógica de predicción sobre un dict de proyecto
# ---------------------------------------------------------------------------
def _predict_risk(proyecto_dict: dict) -> dict:
    """Recibe un dict con los campos del proyecto y devuelve la predicción."""
    X_pred = pd.DataFrame([proyecto_dict])
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


def _proyecto_to_display_dict(proyecto_dict: dict) -> dict:
    """Convierte un dict de proyecto a un dict con claves legibles para el reporte PDF."""
    return {
        "Tipo de proyecto": proyecto_dict.get("tipo_proyecto", ""),
        "Metodología": proyecto_dict.get("metodologia", ""),
        "Duración estimada (meses)": proyecto_dict.get("duracion_estimacion", ""),
        "Presupuesto estimado (USD)": proyecto_dict.get("presupuesto_estimado", ""),
        "Número de recursos": proyecto_dict.get("numero_recursos", ""),
        "Tecnologías": proyecto_dict.get("tecnologias", ""),
        "Complejidad": proyecto_dict.get("complejidad", ""),
        "Experiencia del equipo": proyecto_dict.get("experiencia_equipo", ""),
        "Hitos clave": proyecto_dict.get("hitos_clave", "")
    }


def _prediccion_to_report_dict(prediccion: dict) -> dict:
    """Normaliza un dict de predicción al formato esperado por el reporte PDF."""
    return {
        "riesgo_general": prediccion.get("riesgo_general", ""),
        "probabilidades": prediccion.get("probabilidades_riesgo") or prediccion.get("probabilidades", {}),
        "probabilidad_sobrecosto": prediccion.get("probabilidad_sobrecosto", 0),
        "probabilidad_retraso": prediccion.get("probabilidad_retraso", 0)
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get('/')
def read_root():
    return {"message": "Risk Predictor API"}

@app.post('/predict')
def predict_riesgo(proyecto: ProyectoInput):
    resultado = _predict_risk(proyecto.dict())
    _save_audit_log(proyecto.dict(), resultado)
    return resultado

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

@app.post('/proyectos-ejecucion')
def add_proyecto_ejecucion(proyecto: dict):
    proyecto_id = str(uuid.uuid4())
    if not DB_URL: return {"status": "ok", "id": proyecto_id}
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO proyectos_ejecucion (
                        id, tipo_proyecto, metodologia, duracion_estimacion, presupuesto_estimado,
                        numero_recursos, tecnologias, complejidad, experiencia_equipo, hitos_clave
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (
                    proyecto_id, proyecto.get('tipo_proyecto'), proyecto.get('metodologia'),
                    proyecto.get('duracion_estimacion'), proyecto.get('presupuesto_estimado'),
                    proyecto.get('numero_recursos'), proyecto.get('tecnologias'),
                    proyecto.get('complejidad'), proyecto.get('experiencia_equipo'),
                    proyecto.get('hitos_clave')
                ))
                conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "ok", "id": proyecto_id}

@app.get('/proyectos-ejecucion')
def list_proyectos_ejecucion():
    if not DB_URL: return []
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM proyectos_ejecucion")
                rows = cursor.fetchall()
                # Remove datetime elements to prevent JSON serialization issues if needed
                for r in rows:
                    if 'fecha_creacion' in r and r['fecha_creacion']:
                        r['fecha_creacion'] = r['fecha_creacion'].isoformat()
                return [dict(row) for row in rows]
    except Exception as e:
        return []

@app.get('/proyectos-ejecucion/{proy_id}')
def get_proyecto_ejecucion(proy_id: str):
    if not DB_URL: raise HTTPException(status_code=404, detail='Proyecto no encontrado')
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM proyectos_ejecucion WHERE id = %s", (proy_id,))
                row = cursor.fetchone()
                if row:
                    if 'fecha_creacion' in row and row['fecha_creacion']:
                        row['fecha_creacion'] = row['fecha_creacion'].isoformat()
                    return dict(row)
    except Exception:
        pass
    raise HTTPException(status_code=404, detail='Proyecto no encontrado')

@app.put('/proyectos-ejecucion/{proy_id}')
def update_proyecto_ejecucion(proy_id: str, datos: dict):
    if not DB_URL: return {"status": "ok"}
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                set_clause = ", ".join([f"{k} = %s" for k in datos.keys()])
                values = list(datos.values())
                values.append(proy_id)
                
                cursor.execute(f"UPDATE proyectos_ejecucion SET {set_clause} WHERE id = %s", values)
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail='Proyecto no encontrado')
                conn.commit()
                return {"status": "ok"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/proyectos-ejecucion/{proy_id}/finalizar')
def finalizar_proyecto(proy_id: str, datos_finales: dict):
    if not DB_URL: return {"status": "ok"}
    # Retrieve the project first
    proyecto = None
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM proyectos_ejecucion WHERE id = %s", (proy_id,))
                row = cursor.fetchone()
                if row:
                    proyecto = dict(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en base de datos")

    if not proyecto:
        raise HTTPException(status_code=404, detail='Proyecto no encontrado')
    
    # Update state
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE proyectos_ejecucion 
                    SET costo_real = %s, duracion_real = %s, riesgo_general = %s, estado = 'finalizado'
                    WHERE id = %s
                """, (
                    datos_finales.get('costo_real'), datos_finales.get('duracion_real'),
                    datos_finales.get('riesgo_general', proyecto.get('riesgo_general')), proy_id
                ))
                conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error actualizando proyecto")
    
    # Retrocompatibilidad: Añadir a los CSVs para que el entrenamiento sintético original siga funcionando
    finalizado = {**proyecto, **datos_finales}
    SYNTH_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/synthetic_data_with_outputs.csv'))
    synth_fields = [
        'tipo_proyecto', 'metodologia', 'duracion_estimacion', 'presupuesto_estimado', 'numero_recursos',
        'tecnologias', 'complejidad', 'experiencia_equipo', 'hitos_clave',
        'costo_real', 'duracion_real', 'riesgo_general'
    ]
    file_exists = os.path.exists(SYNTH_PATH)
    try:
        import csv
        with open(SYNTH_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=synth_fields)
            if not file_exists:
                writer.writeheader()
            writer.writerow({k: finalizado.get(k, '') for k in synth_fields})
    except Exception:
        pass # Fallback silent

    DATASET_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/dataset.csv'))
    file_exists_dataset = os.path.exists(DATASET_PATH)
    try:
        import csv
        with open(DATASET_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=synth_fields)
            if not file_exists_dataset:
                writer.writeheader()
            writer.writerow({k: finalizado.get(k, '') for k in synth_fields})
    except Exception:
        pass

    return {"status": "ok"}

@app.post('/reentrenar-modelo')
def reentrenar_modelo(background_tasks: BackgroundTasks):
    """Ejecuta el script de entrenamiento y recarga los modelos en memoria."""
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/train_xgboost.py'))
    python_exe = sys.executable
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    try:
        result = subprocess.run([python_exe, script_path], capture_output=True, text=True, check=True, cwd=project_root)
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
    prediccion = _predict_risk(proyecto.dict())
    proyecto_dict = _proyecto_to_display_dict(proyecto.dict())
    prediccion_dict = _prediccion_to_report_dict(prediccion)
    pdf_path = f"reporte_riesgo_{uuid.uuid4().hex}.pdf"
    generar_reporte_pdf(proyecto_dict, prediccion_dict, filename=pdf_path)
    return FileResponse(pdf_path, media_type='application/pdf', filename='reporte_riesgo.pdf')

@app.post('/enviar-reporte-mailhog')
def enviar_reporte_mailhog_endpoint(request: EnvioReporteRequest):
    """Genera el PDF y lo envía por email usando MailHog (localhost:1025)."""
    prediccion = request.prediccion
    # Si no hay predicción o le faltan probabilidades, calcularla
    if not prediccion or not prediccion.get('probabilidades') or not isinstance(prediccion.get('probabilidades'), dict) or len(prediccion.get('probabilidades')) == 0:
        if request.proyecto:
            prediccion = _predict_risk(request.proyecto)

    proyecto_dict = _proyecto_to_display_dict(request.proyecto)
    prediccion_dict = _prediccion_to_report_dict(prediccion or {})
    pdf_path = f"reporte_riesgo_{uuid.uuid4().hex}.pdf"
    generar_reporte_pdf(proyecto_dict, prediccion_dict, filename=pdf_path)
    asunto = "Reporte de Evaluación de Riesgo"
    cuerpo = "Adjunto encontrará el reporte PDF generado automáticamente."
    enviar_reporte_mailhog(request.destinatario, asunto, cuerpo, pdf_path)
    try:
        os.remove(pdf_path)
    except Exception:
        pass
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
