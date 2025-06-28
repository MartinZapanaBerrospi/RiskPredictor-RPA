import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, log_loss
from sklearn.utils import resample
import joblib
import os

# Definir ruta absoluta para guardar modelos en la carpeta 'models'
MODELS_DIR = os.path.join(os.path.dirname(__file__))

def model_path(filename):
    return os.path.join(MODELS_DIR, filename)

# Cargar datos
inputs = [
    'tipo_proyecto', 'metodologia', 'duracion_estimacion', 'presupuesto_estimado', 'numero_recursos',
    'tecnologias', 'complejidad', 'experiencia_equipo', 'hitos_clave'
]
df = pd.read_csv('synthetic_data_with_outputs.csv')
le_tipo = LabelEncoder()
df['tipo_proyecto_enc'] = le_tipo.fit_transform(df['tipo_proyecto'])
# Codificar metodologia
le_metodologia = LabelEncoder()
df['metodologia_enc'] = le_metodologia.fit_transform(df['metodologia'])
le_complejidad = LabelEncoder()
df['complejidad_enc'] = le_complejidad.fit_transform(df['complejidad'])
le_experiencia = LabelEncoder()
df['experiencia_equipo_enc'] = le_experiencia.fit_transform(df['experiencia_equipo'])

# Tecnologías: multi-hot encoding
mlb = MultiLabelBinarizer()
tec_matrix = mlb.fit_transform(df['tecnologias'].str.split(','))
tec_df = pd.DataFrame(tec_matrix, columns=[f'tec_{t}' for t in mlb.classes_])
df = pd.concat([df, tec_df], axis=1)

# Features finales
features = [
    'tipo_proyecto_enc', 'metodologia_enc', 'duracion_estimacion', 'presupuesto_estimado', 'numero_recursos',
    'complejidad_enc', 'experiencia_equipo_enc', 'hitos_clave'
] + list(tec_df.columns)

# Target
le_riesgo = LabelEncoder()
df['riesgo_general_enc'] = le_riesgo.fit_transform(df['riesgo_general'])

# Crear columnas sobrecosto y retraso antes del balanceo
df['sobrecosto'] = (df['costo_real'] > df['presupuesto_estimado']).astype(int)
df['retraso'] = (df['duracion_real'] > df['duracion_estimacion']).astype(int)

# Balanceo del dataset (upsampling de clases minoritarias)
df_majority = df[df['riesgo_general_enc'] == df['riesgo_general_enc'].value_counts().idxmax()]
classes = df['riesgo_general_enc'].unique()
df_list = [df[df['riesgo_general_enc'] == c] for c in classes]
max_count = max([len(d) for d in df_list])
df_balanced = pd.concat([
    resample(d, replace=True, n_samples=max_count, random_state=42) if len(d) < max_count else d
    for d in df_list
])

X = df_balanced[features]
y = df_balanced['riesgo_general_enc']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Ajuste de hiperparámetros con GridSearchCV
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [4, 6, 8],
    'learning_rate': [0.05, 0.1, 0.2],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

xgb_base = xgb.XGBClassifier(
    objective='multi:softprob',
    num_class=3,
    eval_metric='mlogloss',
    use_label_encoder=False,
    random_state=42
)
grid_search = GridSearchCV(xgb_base, param_grid, cv=3, scoring='f1_weighted', n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

print('Mejores hiperparámetros encontrados:')
print(grid_search.best_params_)

model = grid_search.best_estimator_

# Evaluación
y_pred = model.predict(X_test)
print('Reporte de clasificación:')
print(classification_report(y_test, y_pred, target_names=le_riesgo.classes_))
print('Matriz de confusión:')
print(confusion_matrix(y_test, y_pred))

# Mostrar distribución de clases en el dataset y en el test
print('Distribución de clases en todo el dataset:')
print(df['riesgo_general'].value_counts())
print('Distribución de clases en el conjunto de prueba:')
print(y_test.value_counts())

# Guardar modelo y encoders
joblib.dump(model, model_path('modelo_xgb_riesgo_general.pkl'))
joblib.dump(le_tipo, model_path('le_tipo_proyecto.pkl'))
joblib.dump(le_metodologia, model_path('le_metodologia.pkl'))
joblib.dump(le_complejidad, model_path('le_complejidad.pkl'))
joblib.dump(le_experiencia, model_path('le_experiencia.pkl'))
joblib.dump(mlb, model_path('mlb_tecnologias.pkl'))
joblib.dump(le_riesgo, model_path('le_riesgo_general.pkl'))

print('Modelo XGBoost entrenado y guardado.')

# --- Entrenamiento para sobrecosto (binario) ---
df['sobrecosto'] = (df['costo_real'] > df['presupuesto_estimado']).astype(int)
X_sobrecosto = df_balanced[features]
y_sobrecosto = df_balanced['sobrecosto']

X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(X_sobrecosto, y_sobrecosto, test_size=0.2, random_state=42)

sobrecosto_model = xgb.XGBClassifier(
    objective='binary:logistic',
    eval_metric='logloss',
    use_label_encoder=False,
    random_state=42
)
sobrecosto_model.fit(X_train_s, y_train_s)

# Probabilidad de sobrecosto
sobrecosto_probs = sobrecosto_model.predict_proba(X_test_s)[:,1]
print('\nProbabilidad de sobrecosto (primeros 10 casos):')
print(sobrecosto_probs[:10])

# Evaluación de probabilidades para sobrecosto
print('\nEvaluación modelo de sobrecosto:')
print('ROC AUC:', roc_auc_score(y_test_s, sobrecosto_probs))
print('Log-loss:', log_loss(y_test_s, sobrecosto_probs))
print(classification_report(y_test_s, (sobrecosto_probs > 0.5).astype(int)))

# --- Entrenamiento para retraso (binario) ---
df['retraso'] = (df['duracion_real'] > df['duracion_estimacion']).astype(int)
X_retraso = df_balanced[features]
y_retraso = df_balanced['retraso']

X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_retraso, y_retraso, test_size=0.2, random_state=42)

retraso_model = xgb.XGBClassifier(
    objective='binary:logistic',
    eval_metric='logloss',
    use_label_encoder=False,
    random_state=42
)
retraso_model.fit(X_train_r, y_train_r)

# Probabilidad de retraso
retraso_probs = retraso_model.predict_proba(X_test_r)[:,1]
print('\nProbabilidad de retraso (primeros 10 casos):')
print(retraso_probs[:10])

# Evaluación de probabilidades para retraso
print('\nEvaluación modelo de retraso:')
print('ROC AUC:', roc_auc_score(y_test_r, retraso_probs))
print('Log-loss:', log_loss(y_test_r, retraso_probs))
print(classification_report(y_test_r, (retraso_probs > 0.5).astype(int)))

# Guardar modelos
joblib.dump(sobrecosto_model, model_path('modelo_xgb_sobrecosto.pkl'))
joblib.dump(retraso_model, model_path('modelo_xgb_retraso.pkl'))

print('Modelos para sobrecosto y retraso entrenados y guardados.')
