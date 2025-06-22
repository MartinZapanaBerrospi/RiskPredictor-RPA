import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils import resample
import joblib

# Cargar datos
inputs = [
    'tipo_proyecto', 'duracion_estimacion', 'presupuesto_estimado', 'numero_recursos',
    'tecnologias', 'complejidad', 'experiencia_equipo', 'hitos_clave'
]
df = pd.read_csv('../data/synthetic_data_with_outputs.csv')
# Preprocesamiento de variables categóricas
le_tipo = LabelEncoder()
df['tipo_proyecto_enc'] = le_tipo.fit_transform(df['tipo_proyecto'])
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
    'tipo_proyecto_enc', 'duracion_estimacion', 'presupuesto_estimado', 'numero_recursos',
    'complejidad_enc', 'experiencia_equipo_enc', 'hitos_clave'
] + list(tec_df.columns)

# Target
le_riesgo = LabelEncoder()
df['riesgo_general_enc'] = le_riesgo.fit_transform(df['riesgo_general'])

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
joblib.dump(model, 'modelo_xgb_riesgo_general.pkl')
joblib.dump(le_tipo, 'le_tipo_proyecto.pkl')
joblib.dump(le_complejidad, 'le_complejidad.pkl')
joblib.dump(le_experiencia, 'le_experiencia.pkl')
joblib.dump(mlb, 'mlb_tecnologias.pkl')
joblib.dump(le_riesgo, 'le_riesgo_general.pkl')

print('Modelo XGBoost entrenado y guardado.')
