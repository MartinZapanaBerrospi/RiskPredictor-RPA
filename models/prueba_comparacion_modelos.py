import pandas as pd
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, log_loss
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer

# Cargar datos
DATA_PATH = '../data/dataset.csv'
df = pd.read_csv(DATA_PATH)

# Codificación de variables categóricas
le_tipo = LabelEncoder()
df['tipo_proyecto_enc'] = le_tipo.fit_transform(df['tipo_proyecto'])
le_metodologia = LabelEncoder()
df['metodologia_enc'] = le_metodologia.fit_transform(df['metodologia'])
le_complejidad = LabelEncoder()
df['complejidad_enc'] = le_complejidad.fit_transform(df['complejidad'])
le_experiencia = LabelEncoder()
df['experiencia_equipo_enc'] = le_experiencia.fit_transform(df['experiencia_equipo'])

mlb = MultiLabelBinarizer()
tec_matrix = mlb.fit_transform(df['tecnologias'].astype(str).str.split(','))
tec_df = pd.DataFrame(tec_matrix, columns=[f'tec_{t}' for t in mlb.classes_])
df = pd.concat([df, tec_df], axis=1)

features = [
    'tipo_proyecto_enc', 'metodologia_enc', 'duracion_estimacion', 'presupuesto_estimado', 'numero_recursos',
    'complejidad_enc', 'experiencia_equipo_enc', 'hitos_clave'
] + list(tec_df.columns)

le_riesgo = LabelEncoder()
df['riesgo_general_enc'] = le_riesgo.fit_transform(df['riesgo_general'])

X = df[features]
y = df['riesgo_general_enc']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelo XGBoost
xgb_model = xgb.XGBClassifier(objective='multi:softprob', num_class=3, eval_metric='mlogloss', use_label_encoder=False, random_state=42)
xgb_model.fit(X_train, y_train)
y_pred_xgb = xgb_model.predict(X_test)
y_proba_xgb = xgb_model.predict_proba(X_test)

print('--- XGBoost ---')
print(classification_report(y_test, y_pred_xgb, target_names=le_riesgo.classes_))
print('Matriz de confusión:')
print(confusion_matrix(y_test, y_pred_xgb))
print('ROC AUC:', roc_auc_score(y_test, y_proba_xgb, multi_class='ovr'))
print('Log-loss:', log_loss(y_test, y_proba_xgb))

# Modelo RandomForest (scikit-learn)
sk_model = RandomForestClassifier(n_estimators=200, random_state=42)
sk_model.fit(X_train, y_train)
y_pred_rf = sk_model.predict(X_test)
y_proba_rf = sk_model.predict_proba(X_test)

print('\n--- RandomForest (scikit-learn) ---')
print(classification_report(y_test, y_pred_rf, target_names=le_riesgo.classes_))
print('Matriz de confusión:')
print(confusion_matrix(y_test, y_pred_rf))
print('ROC AUC:', roc_auc_score(y_test, y_proba_rf, multi_class='ovr'))
print('Log-loss:', log_loss(y_test, y_proba_rf))

print('\nComparación completada.')
