import pandas as pd
import numpy as np
import random

# Semilla para reproducibilidad
definir_semilla = 42
np.random.seed(definir_semilla)
random.seed(definir_semilla)

# Parámetros para la generación de datos
N = 200  # Número de proyectos sintéticos

complejidades = ['baja', 'media', 'alta']
tecnologias_posibles = ['cloud', 'big data', 'IA', 'IoT', 'blockchain', 'mobile', 'web']
tipos_proyecto = [
    'desarrollo software', 'migración', 'implementación ERP', 'integración sistemas', 'automatización RPA', 'modernización', 'soporte TI'
]

# Reglas para correlaciones y generación realista
def generar_proyecto():
    tipo = random.choice(tipos_proyecto)
    if tipo == 'implementación ERP':
        duracion = np.random.randint(18, 37)
        presupuesto = np.random.randint(800000, 2000001)
        recursos = np.random.randint(10, 31)
        complejidad = 'alta'
        tecnologias = random.sample(tecnologias_posibles, k=np.random.randint(2, 5))
    elif tipo == 'migración':
        duracion = np.random.randint(6, 18)
        presupuesto = np.random.randint(100000, 600000)
        recursos = np.random.randint(3, 12)
        complejidad = random.choice(['baja', 'media'])
        tecnologias = random.sample(tecnologias_posibles, k=1)
    elif tipo == 'automatización RPA':
        duracion = np.random.randint(6, 18)
        presupuesto = np.random.randint(150000, 500000)
        recursos = np.random.randint(3, 10)
        complejidad = random.choice(['media', 'alta'])
        tecnologias = random.sample(tecnologias_posibles, k=2)
    elif tipo == 'desarrollo software':
        duracion = np.random.randint(8, 25)
        presupuesto = np.random.randint(200000, 1000000)
        recursos = np.random.randint(5, 20)
        complejidad = random.choice(['media', 'alta'])
        tecnologias = random.sample(tecnologias_posibles, k=np.random.randint(1, 4))
    elif tipo == 'integración sistemas':
        duracion = np.random.randint(10, 24)
        presupuesto = np.random.randint(250000, 900000)
        recursos = np.random.randint(5, 15)
        complejidad = random.choice(['media', 'alta'])
        tecnologias = random.sample(tecnologias_posibles, k=2)
    elif tipo == 'modernización':
        duracion = np.random.randint(8, 20)
        presupuesto = np.random.randint(200000, 700000)
        recursos = np.random.randint(4, 12)
        complejidad = random.choice(['media', 'alta'])
        tecnologias = random.sample(tecnologias_posibles, k=2)
    else:  # soporte TI
        duracion = np.random.randint(6, 13)
        presupuesto = np.random.randint(100000, 400000)
        recursos = np.random.randint(3, 8)
        complejidad = 'baja'
        tecnologias = random.sample(tecnologias_posibles, k=1)

    experiencia = np.random.randint(1, 16)  # 1 a 15 años
    hitos = np.random.randint(2, 11)  # 2 a 10 hitos

    # Etiquetado de riesgo basado en reglas
    riesgo = 0  # bajo
    if complejidad == 'alta' or duracion > 24 or presupuesto > 1000000:
        riesgo = 2  # alto
    elif complejidad == 'media' or duracion > 15 or presupuesto > 500000:
        riesgo = 1  # medio
    # Ajuste por experiencia del equipo
    if experiencia < 4 and riesgo < 2:
        riesgo += 1
    if experiencia > 10 and riesgo > 0:
        riesgo -= 1
    riesgo = min(max(riesgo, 0), 2)

    return {
        'tipo_proyecto': tipo,
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

print('¡Dataset sintético realista generado en synthetic_data.csv!')
