import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Cargar datos
inputs = [
    'tipo_proyecto', 'duracion_estimacion', 'presupuesto_estimado', 'numero_recursos',
    'tecnologias', 'complejidad', 'experiencia_equipo', 'hitos_clave'
]
df = pd.read_csv('synthetic_data_with_outputs.csv')

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

X = df[features]
y = df['riesgo_general_enc']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenamiento XGBoost
model = xgb.XGBClassifier(objective='multi:softprob', num_class=3, eval_metric='mlogloss', use_label_encoder=False)
model.fit(X_train, y_train)

# Evaluación
y_pred = model.predict(X_test)
print('Reporte de clasificación:')
print(classification_report(y_test, y_pred, target_names=le_riesgo.classes_))
print('Matriz de confusión:')
print(confusion_matrix(y_test, y_pred))

# Guardar modelo y encoders
joblib.dump(model, 'modelo_xgb_riesgo_general.pkl')
joblib.dump(le_tipo, 'le_tipo_proyecto.pkl')
joblib.dump(le_complejidad, 'le_complejidad.pkl')
joblib.dump(le_experiencia, 'le_experiencia.pkl')
joblib.dump(mlb, 'mlb_tecnologias.pkl')
joblib.dump(le_riesgo, 'le_riesgo_general.pkl')

print('Modelo XGBoost entrenado y guardado.')
