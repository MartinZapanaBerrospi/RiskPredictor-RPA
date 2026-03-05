# 🎯 RiskPredictor-RPA

## Sistema Inteligente de Predicción y Gestión de Riesgos en Proyectos de Tecnología

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React 19](https://img.shields.io/badge/React-19-61dafb?logo=react&logoColor=white)](https://react.dev)
[![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange?logo=python&logoColor=white)](https://xgboost.readthedocs.io)
[![Vite](https://img.shields.io/badge/Vite-6.x-646cff?logo=vite&logoColor=white)](https://vitejs.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> ⚡ **Despliegue Full-Stack:** Backend (FastAPI + Supabase) y Frontend (React SPA). Ver guía de despliegue en Vercel y Render en la sección de Instalación.

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Stack Tecnológico](#-stack-tecnológico)
- [Funcionalidades Principales](#-funcionalidades-principales)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Modelos de Machine Learning](#-modelos-de-machine-learning)
- [API REST — Referencia de Endpoints](#-api-rest--referencia-de-endpoints)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Guía de Uso](#-guía-de-uso)
- [Generación de Datos Sintéticos](#-generación-de-datos-sintéticos)
- [Generación de Reportes PDF](#-generación-de-reportes-pdf)
- [Créditos](#-créditos)

---

## 📖 Descripción General

**RiskPredictor-RPA** es un sistema completo para la predicción y gestión de riesgos en proyectos de tecnología de la información. Combina **Machine Learning** (modelos XGBoost), una **API REST de alto rendimiento** (FastAPI) y un **frontend moderno** (React + TypeScript) para ofrecer:

- Predicciones inteligentes de riesgo basadas en las características del proyecto
- Gestión integral del ciclo de vida de proyectos en ejecución
- Generación automática de reportes PDF profesionales
- Capacidad de reentrenamiento continuo con datos de proyectos finalizados

El sistema está diseñado para equipos de gestión de proyectos TI que necesitan evaluar y mitigar riesgos de forma proactiva, utilizando datos históricos y modelos predictivos para tomar decisiones informadas.

---

## 🏗️ Arquitectura del Sistema

El sistema sigue una arquitectura **cliente-servidor** con tres capas principales:

```
┌──────────────────────────────────────────────────────────────┐
│                        USUARIO                                │
│                    (Navegador Web)                             │
└──────────────────────┬───────────────────────────────────────┘
                       │ HTTP/JSON
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                   FRONTEND (React 19)                         │
│  ┌─────────────┐ ┌──────────────────┐ ┌──────────────────┐   │
│  │ Formulario  │ │ Proyectos en     │ │ Modales de       │   │
│  │ Predicción  │ │ Ejecución (CRUD) │ │ Resultado/Email  │   │
│  └─────────────┘ └──────────────────┘ └──────────────────┘   │
└──────────────────────┬───────────────────────────────────────┘
                       │ fetch (REST API)
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI)                            │
│  ┌─────────┐ ┌───────────┐ ┌──────────┐ ┌────────────────┐   │
│  │/predict │ │/proyectos │ │/reportes │ │/reentrenar     │   │
│  │         │ │-ejecucion │ │  PDF     │ │  modelo        │   │
│  └────┬────┘ └─────┬─────┘ └────┬─────┘ └───────┬────────┘   │
│       │            │            │                │             │
│       ▼            ▼            ▼                ▼             │
│  ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌────────────────┐    │
│  │ Modelos │ │ CSV/JSON │ │  FPDF2   │ │ Subprocess     │    │
│  │  .pkl   │ │  Data    │ │  Engine  │ │ train_xgboost  │    │
│  └─────────┘ └──────────┘ └──────────┘ └────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

### Flujo de datos

1. El **usuario** interactúa con el formulario del frontend ingresando las características del proyecto
2. El **frontend** envía los datos al backend mediante HTTP POST
3. El sistema permite a los usuarios exportar evaluaciones de riesgo en formato PDF. Estos reportes incluyen:

- Resumen ejecutivo del proyecto.
- Evaluación general de riesgo (Alto, Medio, Bajo).
- Probabilidades detalladas para sobrecosto y retraso.
- Gráficos de distribución de probabilidades generados con `matplotlib`.

### Ciclo de Vida de los Datos: Supabase y Reentrenamiento

Para garantizar la integridad corporativa y la escalabilidad, el sistema divide su almacenamiento en dos estrategias:

1. **Almacenamiento en la Nube (Supabase PostgreSQL):** Es el repositorio central de producción.
   - **Log de Auditoría Automatizado (`auditoria_predicciones`):** El backend captura de forma invisible el 100% de los parámetros ingresados en una predicción exitosa. Es una bitácora de uso inmanejable por el usuario final.
   - **Registro de Proyectos (`proyectos_ejecucion`):** Almacena únicamente las evaluaciones en las que el usuario hace clic en el botón **"Guardar Evaluación"**. Permite a los gestores dar seguimiento (CRUD) al proyecto a lo largo del tiempo hasta que éste finaliza y se revelan sus métricas reales.
   - _Nota:_ Requiere configurar la variable `DATABASE_URL` (ver `.env.example`).

2. **CSVs Estáticos (Módulo de Machine Learning):**
   - Los archivos `.csv` en la carpeta `data/` (como `dataset.csv`) conforman la base de conocimiento histórico que la Inteligencia Artificial utilizó para entrenarse originalmente (datos balanceados sintéticamente).
   - **Flujo de Mejora Continua:** En el estado de producción, el sistema web **ya no inyecta datos directamente a estos CSVs**. En su lugar, cuando exista un volumen considerable de proyectos "Finalizados" en Supabase, el administrador de datos debe extraer dicha información, agregarla al `dataset.csv` local y ejecutar manualmente el pipeline de reentrenamiento (`python models/train_xgboost.py`). Este proceso permite que el algoritmo evolucione y adapta sus predicciones a la realidad operativa de la organización.

---

## 🛠️ Stack Tecnológico

### Backend

| Tecnología       | Versión | Uso                                                  |
| :--------------- | :------ | :--------------------------------------------------- |
| **Python**       | 3.8+    | Lenguaje principal del backend y ML                  |
| **FastAPI**      | Latest  | Framework REST de alto rendimiento                   |
| **Uvicorn**      | Latest  | Servidor ASGI para FastAPI                           |
| **XGBoost**      | Latest  | Algoritmo de Gradient Boosting (modelos predictivos) |
| **Scikit-learn** | Latest  | Preprocessing, encoding, métricas de evaluación      |
| **Pandas**       | Latest  | Manipulación de datos tabulares                      |
| **NumPy**        | Latest  | Computación numérica                                 |
| **Joblib**       | Latest  | Serialización de modelos (.pkl)                      |
| **FPDF2**        | Latest  | Generación de reportes PDF profesionales             |

### Frontend

| Tecnología     | Versión | Uso                                  |
| :------------- | :------ | :----------------------------------- |
| **React**      | 19.1    | Biblioteca de interfaz de usuario    |
| **TypeScript** | 5.8     | Tipado estático para JavaScript      |
| **Vite**       | 6.3     | Build tool y dev server ultrarrápido |
| **ESLint**     | 9.25    | Linting y calidad de código          |

---

## ✨ Funcionalidades Principales

### 1. 🎯 Predicción de Riesgo

- **Riesgo general**: Clasificación multiclase (Alto, Medio, Bajo) con probabilidades por clase
- **Probabilidad de sobrecosto**: Estimación binaria de si el proyecto excederá el presupuesto
- **Probabilidad de retraso**: Estimación binaria de si el proyecto se retrasará

### 2. 📋 Gestión de Proyectos en Ejecución

- **Crear**: Registrar nuevos proyectos después de la predicción
- **Leer**: Listar todos los proyectos activos en tabla interactiva
- **Actualizar**: Editar datos de proyectos mediante modal
- **Eliminar**: Dar de baja proyectos con confirmación
- **Finalizar**: Cerrar proyectos con datos finales (costo real, duración real) que alimentan el dataset de entrenamiento

### 3. 📄 Reportes PDF Profesionales

- Generación automática de PDFs con:
  - Datos del proyecto evaluado
  - Resultados de la predicción con probabilidades
  - Interpretación detallada según nivel de riesgo
  - Recomendaciones específicas para sobrecosto y retraso
- Descarga directa o envío por email

### 4. 📧 Envío de Reportes por Email

- Integración nativa con **Brevo HTTP API** para envío de reportes PDF de forma instantánea.
- No utiliza puertos SMTP tradicionales, evitando bloqueos en entornos cloud (como Render).
- Envía un correo con diseño profesional en HTML y el PDF adjunto.

### 5. 🔄 Reentrenamiento de Modelos

- Botón en la interfaz para reentrenar modelos con datos actualizados
- Ejecuta `train_xgboost.py` vía subprocess
- Recarga automáticamente los modelos en memoria después del reentrenamiento

### 6. 🌗 Diseño UI/UX Premium (Glassmorphism)

- Interfaz completamente rediseñada bajo la tendencia **Glassmorphism** (fondos translúcidos, desenfoque, bordes sutiles).
- Componentes modales avanzados con animaciones elásticas y retroalimentación interactiva (Toasts centrados y superiores).
- **Tema Claro/Oscuro** persistente con `localStorage`, adaptando paletas de colores corporativos (Azul/Índigo en modo oscuro, Blanco/Gris en modo claro) de forma fluida.

---

## 📁 Estructura del Proyecto

```
RiskPredictor-RPA/
│
├── api/                              # Backend - API REST
│   └── main.py                       # Endpoints FastAPI, helpers de predicción
│
├── data/                             # Datos y generación
│   ├── generate_synthetic_data.py    # Generador de 20,000 proyectos sintéticos
│   ├── preparacion.py                # Preparación de dataset para entrenamiento
│   └── opciones_formulario.json      # Opciones dinámicas del formulario
│
├── models/                           # Machine Learning
│   ├── train_xgboost.py              # Entrenamiento con GridSearchCV + balanceo
│   └── prueba_comparacion_modelos.py # Comparación XGBoost vs RandomForest
│
├── frontend/                         # Aplicación React + TypeScript + Vite
│   ├── src/
│   │   ├── App.tsx                   # Formulario principal de predicción
│   │   ├── App.css                   # Estilos completos (tema claro/oscuro)
│   │   ├── ProyectosEjecucion.tsx    # Vista CRUD de proyectos
│   │   ├── ModalEditarProyecto.tsx   # Modal para edición de proyectos
│   │   ├── ModalFinalizarProyecto.tsx # Modal para cierre de proyectos
│   │   ├── ModalResultadoRiesgo.tsx  # Modal de resultado (vista proyectos)
│   │   ├── ModalResultadoRiesgoPrincipal.tsx # Modal de resultado (vista principal)
│   │   ├── ModalEnviarEmail.tsx      # Modal para envío de reportes por email
│   │   ├── ReportePDFButton.tsx      # Botón de descarga de PDF
│   │   ├── Toast.tsx                 # Notificaciones toast
│   │   ├── main.tsx                  # Entry point
│   │   └── index.css                 # Estilos base
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── utils/                            # Utilidades del backend
│   ├── __init__.py                   # Inicializador de paquete
│   ├── reporte_profesional.py        # Generación de PDFs (clase PDFReport)
│   └── email_mailhog.py             # Envío de emails con adjunto PDF
│
├── requirements.txt                  # Dependencias Python
├── .gitignore                        # Archivos excluidos de git
└── README.md                         # Esta documentación
```

---

## 🧠 Modelos de Machine Learning

### Proceso de Entrenamiento

El sistema utiliza **3 modelos XGBoost** especializados, entrenados con un dataset sintético de **20,000 registros**:

#### 1. Modelo de Riesgo General (Multiclase)

- **Algoritmo**: `XGBClassifier` con `multi:softprob`
- **Clases**: Alto, Medio, Bajo
- **Optimización**: `GridSearchCV` con 3-fold cross-validation
  - `n_estimators`: [100, 200]
  - `max_depth`: [4, 6, 8]
  - `learning_rate`: [0.05, 0.1, 0.2]
  - `subsample`: [0.8, 1.0]
  - `colsample_bytree`: [0.8, 1.0]
- **Balanceo**: Upsampling de clases minoritarias
- **Métrica**: `f1_weighted`

#### 2. Modelo de Sobrecosto (Binario)

- **Algoritmo**: `XGBClassifier` con `binary:logistic`
- **Target**: `costo_real > presupuesto_estimado`
- **Métricas**: ROC AUC, Log-loss

#### 3. Modelo de Retraso (Binario)

- **Algoritmo**: `XGBClassifier` con `binary:logistic`
- **Target**: `duracion_real > duracion_estimacion`
- **Métricas**: ROC AUC, Log-loss

### Features de Entrada (9 variables)

| Feature                | Tipo       | Encoding            | Descripción                        |
| :--------------------- | :--------- | :------------------ | :--------------------------------- |
| `tipo_proyecto`        | Categórica | LabelEncoder        | Tipo de proyecto TI                |
| `metodologia`          | Categórica | LabelEncoder        | Metodología de desarrollo          |
| `duracion_estimacion`  | Numérica   | —                   | Duración estimada en meses         |
| `presupuesto_estimado` | Numérica   | —                   | Presupuesto en USD                 |
| `numero_recursos`      | Numérica   | —                   | Personas asignadas al equipo       |
| `tecnologias`          | Multi-cat  | MultiLabelBinarizer | Tecnologías utilizadas (multi-hot) |
| `complejidad`          | Categórica | LabelEncoder        | Baja, Media, Alta                  |
| `experiencia_equipo`   | Numérica   | —                   | Años promedio de experiencia       |
| `hitos_clave`          | Numérica   | —                   | Número de milestones               |

### Artefactos Generados (`.pkl`)

| Archivo                         | Contenido                            |
| :------------------------------ | :----------------------------------- |
| `modelo_xgb_riesgo_general.pkl` | Modelo multiclase XGBoost            |
| `modelo_xgb_sobrecosto.pkl`     | Modelo binario de sobrecosto         |
| `modelo_xgb_retraso.pkl`        | Modelo binario de retraso            |
| `le_tipo_proyecto.pkl`          | LabelEncoder para tipo_proyecto      |
| `le_metodologia.pkl`            | LabelEncoder para metodología        |
| `le_complejidad.pkl`            | LabelEncoder para complejidad        |
| `le_experiencia.pkl`            | LabelEncoder para experiencia_equipo |
| `mlb_tecnologias.pkl`           | MultiLabelBinarizer para tecnologías |
| `le_riesgo_general.pkl`         | LabelEncoder para clases de riesgo   |

---

## 🔌 API REST — Referencia de Endpoints

Base URL: `http://localhost:8000`

### Predicción

| Método | Endpoint   | Descripción                                  |
| :----- | :--------- | :------------------------------------------- |
| `GET`  | `/`        | Health check                                 |
| `POST` | `/predict` | Predice riesgo general, sobrecosto y retraso |

**Ejemplo `POST /predict`:**

```json
{
  "tipo_proyecto": "desarrollo software",
  "metodologia": "scrum",
  "duracion_estimacion": 14,
  "presupuesto_estimado": 350000,
  "numero_recursos": 8,
  "tecnologias": "web,mobile",
  "complejidad": "media",
  "experiencia_equipo": 7,
  "hitos_clave": 5
}
```

**Respuesta:**

```json
{
  "riesgo_general": "Medio",
  "probabilidades_riesgo": {
    "Alto": 0.15,
    "Bajo": 0.35,
    "Medio": 0.5
  },
  "probabilidad_sobrecosto": 0.42,
  "probabilidad_retraso": 0.38
}
```

### Formulario

| Método | Endpoint               | Descripción                |
| :----- | :--------------------- | :------------------------- |
| `GET`  | `/opciones-formulario` | Obtiene opciones dinámicas |
| `PUT`  | `/opciones-formulario` | Actualiza opciones         |

### Proyectos en Ejecución

| Método   | Endpoint                              | Descripción                 |
| :------- | :------------------------------------ | :-------------------------- |
| `POST`   | `/proyectos-ejecucion`                | Crea un proyecto            |
| `GET`    | `/proyectos-ejecucion`                | Lista todos los proyectos   |
| `GET`    | `/proyectos-ejecucion/{id}`           | Obtiene un proyecto por ID  |
| `PUT`    | `/proyectos-ejecucion/{id}`           | Actualiza un proyecto       |
| `DELETE` | `/proyectos-ejecucion/{id}`           | Elimina un proyecto         |
| `POST`   | `/proyectos-ejecucion/{id}/finalizar` | Finaliza y mueve al dataset |

### Reportes y Utilidades

| Método | Endpoint                  | Descripción                                |
| :----- | :------------------------ | :----------------------------------------- |
| `POST` | `/generar-reporte`        | Genera y descarga PDF de riesgo            |
| `POST` | `/enviar-reporte-mailhog` | Genera PDF y lo envía vía Brevo HTTP API   |
| `POST` | `/reentrenar-modelo`      | Reentrena modelos (requiere entorno local) |

> 📖 Documentación interactiva automática disponible en: `http://localhost:8000/docs`

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- **Python** 3.8 o superior
- **Node.js** 18 o superior
- **pip** y **npm**

### 1. Clonar el repositorio

```bash
git clone https://github.com/MartinZapanaBerrospi/RiskPredictor-RPA.git
cd RiskPredictor-RPA
```

### 2. Backend (API FastAPI)

```bash
# 1. Crear entorno virtual (Recomendado)
python -m venv venv

# 2. Activar el entorno virtual
# En Windows (Git Bash) o Linux/Mac:
source venv/Scripts/activate  # Alternativa CMD: venv\Scripts\activate

# 3. Instalar dependencias de Python
pip install -r requirements.txt

# 4. (Opcional) Generar datos sintéticos
python data/generate_synthetic_data.py

# 5. Preparar dataset para entrenamiento
python data/preparacion.py

# 6. Entrenar los modelos
python models/train_xgboost.py

# 7. Iniciar la API
uvicorn api.main:app --reload
```

> La API estará disponible en `http://localhost:8000`
> Documentación interactiva en `http://localhost:8000/docs`

### 3. Frontend (React + Vite)

```bash
# Entrar a la carpeta frontend
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

> El frontend estará disponible en `http://localhost:5173`

### 4. Despliegue en Producción (Backend API) en Render

Para que tu Frontend en React pueda conectarse a la API pública, puedes desplegar el backend (FastAPI) de forma gratuita en **[Render](https://render.com/)**:

1. Crea una cuenta en Render conectada a tu GitHub.
2. Crea un **"New Web Service"** (elige la opción manual gratuita, no Blueprint).
3. Conecta este repositorio (`RiskPredictor-RPA`).
4. Configuración:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker`
5. Variables de Entorno (Environment Variables):
   - `PYTHON_VERSION`: `3.12.0`
   - `DATABASE_URL`: Tu conexión a Supabase PostgreSQL.
   - `FRONTEND_URL`: URL de tu frontend en Vercel (ej: `https://mi-app-react.vercel.app`) para habilitar CORS de forma segura.

### 5. Despliegue en Producción (Frontend React) en Vercel

Dado que la aplicación es una Single Page Application (SPA) construida con Vite, **[Vercel](https://vercel.com/)** es el hosting ideal y gratuito:

1. Crea una cuenta en Vercel con tu cuenta de GitHub.
2. Haz clic en **"Add New Project"** e importa el repositorio `RiskPredictor-RPA`.
3. Configuración del Framework: Vercel autodetectará que es un proyecto de Vite.
4. **Root Directory:** Haz clic en Editar y selecciona `frontend`.
5. Variables de Entorno (Environment Variables):
   - Agrega `VITE_API_URL` y pon como valor la URL pública que te dio Render (ej. `https://riskpredictor-api.onrender.com`).
6. Haz clic en **Deploy**. ¡Tu aplicación completa y funcional con base de datos estará en vivo!

### 5. Configuración de Email (Brevo HTTP API)

El sistema utiliza **Brevo** (anteriormente Sendinblue) para el envío de reportes PDF por email, sin depender de puertos SMTP (que suelen ser bloqueados en servidores cloud como Render).

1. Crea una cuenta gratuita en [brevo.com](https://www.brevo.com/) (permite 300 emails/día gratis).
2. Verifica tu correo remitente en **Settings → Senders**.
3. Genera una API Key en **Settings → SMTP & API → API Keys**.
4. En tu servidor (Render o `.env` local), configura las siguientes variables:
   - `BREVO_API_KEY`: Tu API Key generada.
   - `SMTP_EMAIL`: El correo remitente verificado en el paso 2.

---

## 📘 Guía de Uso

### Predicción de Riesgo

1. En el formulario principal, selecciona el tipo de proyecto, metodología y demás características (incluyendo tecnologías base).
2. Haz clic en **"Generar Predicción"**. El sistema validará los datos y consultará el motor analítico.
3. Se mostrará un modal interactivo con el resultado: riesgo general (etiqueta dinámica), probabilidades (barras de progreso), probabilidad de sobrecosto y retraso.
4. Acciones disponibles en el modal:
   - **💾 Guardar Proyecto**: Registra los datos del proyecto y la predicción en la base de datos (Supabase) para seguimiento.
   - **📄 Descargar reporte PDF**: Genera y descarga un reporte formal al instante.
   - **📧 Enviar por Email**: Solicita un correo destinatario, genera el archivo PDF en el servidor, y lo envía adjunto con un diseño corporativo vía Brevo.

### Gestión de Proyectos en Ejecución

1. Ve a la vista **"Ver Proyectos en Ejecución"** para administrar los proyectos previamente guardados desde el dashboard de predicción.
2. La vista presenta una tabla horizontal escalable (con scroll responsivo) que lista todos los proyectos activos.
3. Desde la tabla, se pueden **editar**, **eliminar**, **enviar reportes por email** o **finalizar** proyectos.
4. Al **finalizar (🎯)** un proyecto, se solicitan los valores reales finales (costo real, duración real). Esta información histórica es la que se usará para retroalimentar y mejorar los modelos predictivos en el futuro.

### Reentrenamiento del Motor (Modo Administrador)

Debido a que el entrenamiento de modelos de Machine Learning requiere alta capacidad de cómputo (memoria RAM/CPU), esta acción debe realizarse en un **entorno local o servidor dedicado**, y no desde la UI pública desplegada en cuentas de capa gratuita (Render Free Tier):

1. Descarga la data histórica de proyectos `finalizados` desde tu base de datos Supabase.
2. Inyéctala en `data/dataset.csv`.
3. Ejecuta en terminal: `python models/train_xgboost.py` para generar los nuevos algoritmos (`.pkl`).
4. Haz _commit & push_ de los nuevos `.pkl` al repositorio para actualizar el sistema en la nube.

---

## 📊 Generación de Datos Sintéticos

El script `data/generate_synthetic_data.py` genera **20,000 proyectos TI sintéticos** con distribuciones realistas basadas en:

- **Tipos de proyecto**: desarrollo software, migración, implementación ERP, integración sistemas, automatización RPA, modernización, soporte TI
- **Metodologías**: scrum, kanban, agile, cascada (asignadas según tipo)
- **Tecnologías**: cloud, big data, IA, IoT, blockchain, mobile, web
- **Complejidad**: baja, media, alta (correlacionada con tipo)
- **Riesgo**: calculado con reglas que consideran experiencia, complejidad, tecnologías, presupuesto y duración

### Reglas de riesgo

- Experiencia baja + complejidad alta → mayor riesgo
- 3+ tecnologías → mayor riesgo
- Proyectos tipo ERP/integración → mayor riesgo
- Presupuesto por recurso bajo → mayor riesgo
- Duración corta + complejidad alta → mayor riesgo

---

## 📄 Generación de Reportes PDF

Los reportes PDF incluyen:

1. **Encabezado**: Título profesional con fecha de generación
2. **Datos del Proyecto**: Tabla con todos los parámetros ingresados
3. **Resultado de Predicción**: Riesgo general, probabilidades por clase, sobrecosto y retraso
4. **Interpretación de Resultados**: Análisis textual personalizado según nivel de riesgo con recomendaciones específicas

Generados por `utils/reporte_profesional.py` usando la librería FPDF2 con diseño corporativo.

---

## 👥 Créditos

Desarrollado por **Grupo 7** — RPA para la Gestión de Riesgos en Proyectos de Tecnología.
