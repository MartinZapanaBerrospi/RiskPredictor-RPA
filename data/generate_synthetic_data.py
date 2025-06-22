import pandas as pd
import numpy as np
import random

# Parámetros para la generación de datos
N = 200  # Número de proyectos sintéticos

complejidades = ['baja', 'media', 'alta']
tecnologias_posibles = ['cloud', 'big data', 'IA', 'IoT', 'blockchain', 'mobile', 'web']

# Función para generar una fila de datos sintéticos
def generar_proyecto():
    duracion = np.random.randint(6, 37)  # 6 a 36 meses
    presupuesto = np.random.randint(100000, 2000001)  # 100k a 2M
    recursos = np.random.randint(3, 31)  # 3 a 30 personas
    tecnologias = random.sample(tecnologias_posibles, k=np.random.randint(1, 4))
    complejidad = random.choice(complejidades)
    experiencia = np.random.randint(1, 16)  # 1 a 15 años
    hitos = np.random.randint(2, 11)  # 2 a 10 hitos
    # Etiqueta de riesgo simulada (0: bajo, 1: medio, 2: alto)
    riesgo = np.random.choice([0, 1, 2], p=[0.5, 0.3, 0.2])
    return {
        'duracion_estimacion': duracion,
        'presupuesto_estimado': presupuesto,
        'numero_recursos': recursos,
        'tecnologias': ','.join(tecnologias),
        'complejidad': complejidad,
        'experiencia_equipo': experiencia,
        'hitos_clave': hitos,
        'riesgo': riesgo
    }

# Generar el dataset
proyectos = [generar_proyecto() for _ in range(N)]
df = pd.DataFrame(proyectos)
df.to_csv('synthetic_data.csv', index=False)

print('¡Dataset sintético generado en synthetic_data.csv!')
