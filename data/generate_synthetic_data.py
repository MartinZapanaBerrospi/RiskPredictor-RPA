import pandas as pd
import numpy as np
import random

# Semilla para reproducibilidad
definir_semilla = 42
np.random.seed(definir_semilla)
random.seed(definir_semilla)

N = 200  # Número de proyectos sintéticos

complejidades = ['baja', 'media', 'alta']
tecnologias_posibles = ['cloud', 'big data', 'IA', 'IoT', 'blockchain', 'mobile', 'web']
tipos_proyecto = [
    'desarrollo software', 'migración', 'implementación ERP', 'integración sistemas', 'automatización RPA', 'modernización', 'soporte TI'
]

# Función para simular valores faltantes
def simular_faltante(valor, prob=0.05):
    return valor if np.random.rand() > prob else np.nan

# Generación realista de proyectos TI sintéticos
def generar_proyecto():
    tipo = random.choice(tipos_proyecto)
    if tipo == 'implementación ERP':
        duracion = int(np.random.normal(28, 4))
        presupuesto = int(np.random.normal(1200000, 250000))
        recursos = int(np.random.normal(20, 5))
        complejidad = 'alta'
        tecnologias = random.sample(tecnologias_posibles, k=np.random.randint(2, 5))
    elif tipo == 'migración':
        duracion = int(np.random.normal(12, 3))
        presupuesto = int(np.random.normal(350000, 100000))
        recursos = int(np.random.normal(7, 2))
        complejidad = random.choice(['baja', 'media'])
        tecnologias = random.sample(tecnologias_posibles, k=1)
    elif tipo == 'automatización RPA':
        duracion = int(np.random.normal(10, 3))
        presupuesto = int(np.random.normal(300000, 80000))
        recursos = int(np.random.normal(6, 2))
        complejidad = random.choice(['media', 'alta'])
        tecnologias = random.sample(tecnologias_posibles, k=2)
    elif tipo == 'desarrollo software':
        duracion = int(np.random.normal(15, 5))
        presupuesto = int(np.random.normal(600000, 200000))
        recursos = int(np.random.normal(12, 4))
        complejidad = random.choice(['media', 'alta'])
        tecnologias = random.sample(tecnologias_posibles, k=np.random.randint(1, 4))
    elif tipo == 'integración sistemas':
        duracion = int(np.random.normal(16, 4))
        presupuesto = int(np.random.normal(500000, 150000))
        recursos = int(np.random.normal(10, 3))
        complejidad = random.choice(['media', 'alta'])
        tecnologias = random.sample(tecnologias_posibles, k=2)
    elif tipo == 'modernización':
        duracion = int(np.random.normal(12, 3))
        presupuesto = int(np.random.normal(400000, 100000))
        recursos = int(np.random.normal(8, 2))
        complejidad = random.choice(['media', 'alta'])
        tecnologias = random.sample(tecnologias_posibles, k=2)
    else:  # soporte TI
        duracion = int(np.random.normal(9, 2))
        presupuesto = int(np.random.normal(200000, 50000))
        recursos = int(np.random.normal(5, 1))
        complejidad = 'baja'
        tecnologias = random.sample(tecnologias_posibles, k=1)

    # Limitar valores a rangos razonables
    duracion = max(6, min(duracion, 36))
    presupuesto = max(100000, min(presupuesto, 2000000))
    recursos = max(3, min(recursos, 30))

    experiencia = int(np.random.normal(8, 3))  # años de experiencia promedio
    experiencia = max(1, min(experiencia, 15))
    hitos = np.random.randint(2, 11)

    # Variables adicionales
    satisfaccion_cliente = simular_faltante(round(np.random.normal(7.5, 1.5), 1), prob=0.08)  # escala 1-10
    cambios_alcance = simular_faltante(np.random.poisson(2), prob=0.05)
    incidencias_criticas = simular_faltante(np.random.binomial(3, 0.2), prob=0.05)
    rotacion_equipo = simular_faltante(np.random.binomial(recursos, 0.1), prob=0.05)

    # Etiquetado de riesgo avanzado
    score = 0
    score += 1.5 if complejidad == 'alta' else (0.5 if complejidad == 'media' else 0)
    score += 1 if duracion > 20 else 0
    score += 1 if presupuesto > 1000000 else 0
    score += 1 if experiencia < 4 else 0
    score += 0.5 if cambios_alcance and cambios_alcance > 3 else 0
    score += 0.5 if incidencias_criticas and incidencias_criticas > 1 else 0
    score += 0.5 if rotacion_equipo and rotacion_equipo > 2 else 0
    score -= 1 if satisfaccion_cliente and satisfaccion_cliente > 8 else 0
    score -= 0.5 if experiencia > 12 else 0
    # Asignar riesgo
    if score >= 3: riesgo = 2  # alto
    elif score >= 1.5: riesgo = 1  # medio
    else: riesgo = 0  # bajo

    return {
        'tipo_proyecto': tipo,
        'duracion_estimacion': duracion,
        'presupuesto_estimado': presupuesto,
        'numero_recursos': recursos,
        'tecnologias': ','.join(tecnologias),
        'complejidad': complejidad,
        'experiencia_equipo': experiencia,
        'hitos_clave': hitos,
        'satisfaccion_cliente': satisfaccion_cliente,
        'cambios_alcance': cambios_alcance,
        'incidencias_criticas': incidencias_criticas,
        'rotacion_equipo': rotacion_equipo,
        'riesgo': riesgo
    }

proyectos = [generar_proyecto() for _ in range(N)]
df = pd.DataFrame(proyectos)
df.to_csv('synthetic_data.csv', index=False)

print('¡Dataset sintético robusto generado en synthetic_data.csv!')
