# 🎯 RiskPredictor-RPA

## Sistema Inteligente de Predicción y Gestión de Riesgos en Proyectos de Tecnología

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React 19](https://img.shields.io/badge/React-19-61dafb?logo=react&logoColor=white)](https://react.dev)
[![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange?logo=python&logoColor=white)](https://xgboost.readthedocs.io)
[![Vite](https://img.shields.io/badge/Vite-6.x-646cff?logo=vite&logoColor=white)](https://vitejs.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 🌐 **[Ver Demo en Vivo →](https://martinzapanaberrospi.github.io/RiskPredictor-RPA/)**

---

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
3. La **API** procesa los datos con los encoders (LabelEncoder, MultiLabelBinarizer) y ejecuta la predicción
4. Los **modelos XGBoost** retornan probabilidades de riesgo general, sobrecosto y retraso
5. Los resultados se presentan al usuario y opcionalmente se generan reportes PDF

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

- Integración con MailHog para envío de reportes PDF como adjunto
- Funciona tanto desde el formulario principal como desde la tabla de proyectos

### 5. 🔄 Reentrenamiento de Modelos

- Botón en la interfaz para reentrenar modelos con datos actualizados
- Ejecuta `train_xgboost.py` vía subprocess
- Recarga automáticamente los modelos en memoria después del reentrenamiento

### 6. 🌗 Tema Claro/Oscuro

- Toggle persistente con localStorage
- Diseño adaptado para ambos modos

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
├── docs/                             # GitHub Pages - Página del proyecto
│   └── index.html
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

| Método | Endpoint                  | Descripción                              |
| :----- | :------------------------ | :--------------------------------------- |
| `POST` | `/generar-reporte`        | Genera y descarga PDF de riesgo          |
| `POST` | `/enviar-reporte-mailhog` | Genera PDF y lo envía por email          |
| `POST` | `/reentrenar-modelo`      | Reentrena modelos con datos actualizados |

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

### 4. Despliegue en Producción (Backend API)

Para que el Frontend estático en GitHub Pages pueda conectarse a una API real, puedes desplegar el backend de forma 100% gratuita y **sin tarjeta de crédito** en **[Render](https://render.com/)**, pero debes hacerlo manualmente desde su panel Web Service (no mediante Blueprints).

1. Crea una cuenta en Render conectada a tu GitHub.
2. En el panel, haz clic en el botón **"New +"** y selecciona **"Web Service"**.
   _(🚨 Es muy importante que elijas Web Service y NO "Blueprint", ya que la opción Blueprint ahora requiere ingresar una tarjeta de crédito incluso para cuentas gratuitas)._
3. Selecciona la opción **"Build and deploy from a Git repository"** y conecta este repositorio (`RiskPredictor-RPA`).
4. En la configuración del servicio, asegúrate de llenar estos campos:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker`
5. En la sección de Environment Variables, añade:
   - `PYTHON_VERSION`: `3.12.0`
   - `FRONTEND_URL`: `https://martinzapanaberrospi.github.io`
6. En **Instance Type**, asegúrate de elegir el plan **Free** ($0/month) y haz clic en "Create Web Service".

> **Nota:** La URL pública que te asigne Render (ej. `https://tu-api.onrender.com`) será el nuevo endpoint. El proyecto ya viene reconfigurado con los permisos de CORS necesarios.

### 5. (Opcional) MailHog para emails

Para la funcionalidad de envío de reportes por email, instalar y ejecutar [MailHog](https://github.com/mailhog/MailHog):

```bash
# Descargar e iniciar MailHog
# Interfaz web en http://localhost:8025
# Servidor SMTP en localhost:1025
```

---

## 📘 Guía de Uso

### Predicción de Riesgo

1. En el formulario principal, seleccionar el tipo de proyecto, metodología y demás parámetros
2. Hacer clic en **"Predecir Riesgo"**
3. Se mostrará un modal con el resultado: riesgo general, probabilidades, sobrecosto y retraso
4. Desde el modal se puede **descargar el reporte PDF** o **enviarlo por email**

### Gestión de Proyectos

1. Después de predecir, hacer clic en **"Guardar en Ejecución"** para registrar el proyecto
2. Acceder a **"Ver Proyectos en Ejecución"** para ver la tabla con todos los proyectos activos
3. Desde la tabla, se pueden **editar**, **eliminar**, **predecir nuevamente**, **enviar reportes** o **finalizar** proyectos
4. Al **finalizar** un proyecto, se registran los datos finales (costo real, duración real, riesgo) que alimentan el dataset de entrenamiento

### Reentrenamiento

1. Hacer clic en **"Reentrenar modelo"** en la vista principal
2. El sistema ejecutará el script de entrenamiento con los datos actualizados
3. Los modelos se recargarán en memoria automáticamente

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
