import joblib
import pandas as pd
import numpy as np

# Cargar modelo y encoders
model = joblib.load('modelo_xgb_riesgo_general.pkl')
le_tipo = joblib.load('le_tipo_proyecto.pkl')
le_complejidad = joblib.load('le_complejidad.pkl')
le_experiencia = joblib.load('le_experiencia.pkl')
mlb = joblib.load('mlb_tecnologias.pkl')
le_riesgo = joblib.load('le_riesgo_general.pkl')

# Cargar modelos adicionales
sobrecosto_model = joblib.load('models/modelo_xgb_sobrecosto.pkl')
retraso_model = joblib.load('models/modelo_xgb_retraso.pkl')

# Ejemplo de input del usuario
input_dict = {
    'tipo_proyecto': 'desarrollo software',
    'duracion_estimacion': 14,
    'presupuesto_estimado': 350000,
    'numero_recursos': 8,
    'tecnologias': 'web,mobile',
    'complejidad': 'media',
    'experiencia_equipo': 7,
    'hitos_clave': 5
}

# Preprocesamiento
X_pred = pd.DataFrame([input_dict])
X_pred['tipo_proyecto_enc'] = le_tipo.transform(X_pred['tipo_proyecto'])
X_pred['complejidad_enc'] = le_complejidad.transform(X_pred['complejidad'])
# Si experiencia_equipo fue codificada como numérica, no transformar
if hasattr(le_experiencia, 'classes_') and X_pred['experiencia_equipo'].dtype == object:
    X_pred['experiencia_equipo_enc'] = le_experiencia.transform(X_pred['experiencia_equipo'])
else:
    X_pred['experiencia_equipo_enc'] = X_pred['experiencia_equipo']
# Tecnologías multi-hot
tec_matrix = mlb.transform([X_pred.loc[0, 'tecnologias'].split(',')])
tec_df = pd.DataFrame(tec_matrix, columns=[f'tec_{t}' for t in mlb.classes_])
for col in tec_df.columns:
    X_pred[col] = tec_df[col].values

features = [
    'tipo_proyecto_enc', 'duracion_estimacion', 'presupuesto_estimado', 'numero_recursos',
    'complejidad_enc', 'experiencia_equipo_enc', 'hitos_clave'
] + list(tec_df.columns)

# Completar columnas faltantes con 0 (por si acaso)
for col in features:
    if col not in X_pred:
        X_pred[col] = 0
X_pred = X_pred[features]

# Predicción riesgo general
pred = model.predict(X_pred)[0]
pred_label = le_riesgo.inverse_transform([pred])[0]
pred_proba = model.predict_proba(X_pred)[0]

# Predicción sobrecosto y retraso (probabilidad)
sobrecosto_proba = sobrecosto_model.predict_proba(X_pred)[0][1]
retraso_proba = retraso_model.predict_proba(X_pred)[0][1]

print(f"Predicción de riesgo general: {pred_label}")
print("Probabilidades por clase:")
for clase, proba in zip(le_riesgo.classes_, pred_proba):
    print(f"  {clase}: {proba:.2f}")
print(f"\nProbabilidad de sobrecosto: {sobrecosto_proba:.2f}")
print(f"Probabilidad de retraso: {retraso_proba:.2f}")
