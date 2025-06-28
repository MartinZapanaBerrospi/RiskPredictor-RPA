import pandas as pd
import os

# Ruta absoluta al archivo de datos completos
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'synthetic_data_with_outputs.csv'))

# Leer el dataset completo
df = pd.read_csv(DATA_PATH)

# Seleccionar todos los campos originales de generate_synthetic_data + sobrecosto, retraso, puntos_riesgo y riesgo_general
campos_base = [
    'tipo_proyecto', 'metodologia', 'duracion_estimacion', 'presupuesto_estimado', 'numero_recursos',
    'tecnologias', 'complejidad', 'experiencia_equipo', 'hitos_clave',
    'costo_real', 'duracion_real'
]
campos_extra = ['sobrecosto', 'retraso', 'puntos_riesgo', 'riesgo_general']

# Solo agregar los campos extra si existen en el archivo
campos_final = campos_base + [c for c in campos_extra if c in df.columns]

df[campos_final].to_csv('dataset.csv', index=False)

print('Archivo dataset.csv generado con todos los campos originales y los calculados.')
