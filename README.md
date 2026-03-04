# RiskPredictor-RPA: Predicción y Gestión de Riesgos en Proyectos TI

[![GitHub Pages](https://img.shields.io/badge/📖_Documentación-GitHub_Pages-blue?style=for-the-badge)](https://martinzapanaberrospi.github.io/RiskPredictor-RPA/)

> 📖 **[Ver documentación completa →](https://martinzapanaberrospi.github.io/RiskPredictor-RPA/)**

Este proyecto implementa un sistema completo para la predicción y gestión de riesgos en proyectos de tecnología, combinando Machine Learning, una API REST (FastAPI) y un frontend moderno en React.

## Arquitectura del Proyecto

El sistema está compuesto por los siguientes módulos principales:

- **Frontend (React):**
  - Interfaz de usuario para ingresar proyectos, visualizar predicciones, gestionar proyectos en ejecución y lanzar reentrenamientos.
  - Se comunica con la API mediante peticiones HTTP (fetch/AJAX).

- **Backend/API (FastAPI):**
  - Expone endpoints REST para predicción de riesgos, gestión de proyectos en ejecución, edición de opciones de formulario y reentrenamiento de modelos.
  - Carga y utiliza modelos de Machine Learning entrenados previamente.
  - Permite reentrenar los modelos bajo demanda ejecutando scripts de Python y recargando los modelos en memoria.

- **Modelos y scripts de ML (Python):**
  - Scripts para generación de datos sintéticos, entrenamiento y reentrenamiento de modelos (XGBoost, scikit-learn).
  - Los modelos y encoders se guardan en archivos `.pkl` y son cargados por la API.

- **Archivos de datos:**
  - `synthetic_data_with_outputs.csv`: Dataset principal para entrenamiento y reentrenamiento.
  - `proyectos_ejecucion.csv`: Proyectos en curso gestionados desde el frontend.
  - `opciones_formulario.json`: Opciones dinámicas para los formularios del frontend.

### Diagrama de alto nivel

```
[Usuario]
   │
   ▼
[Frontend React]
   │  (HTTP/JSON)
   ▼
[API FastAPI  ──── Modelos ML (joblib .pkl)]
   │  │
   │  └── Ejecuta scripts de entrenamiento/reentrenamiento
   │
   └── Lee/Escribe archivos CSV/JSON en /data
```

## Estructura del proyecto

```
RiskPredictor-RPA/
│
├── api/                 # API REST con FastAPI
│   └── main.py          # Endpoints, predicción, reportes
│
├── data/                # Datos y scripts de generación
│   ├── generate_synthetic_data.py
│   ├── preparacion.py
│   └── opciones_formulario.json
│
├── models/              # Entrenamiento de modelos ML
│   ├── train_xgboost.py
│   └── prueba_comparacion_modelos.py
│
├── frontend/            # Aplicación React + TypeScript
│   └── src/
│       ├── App.tsx
│       ├── ProyectosEjecucion.tsx
│       ├── Modal*.tsx
│       └── App.css
│
├── utils/               # Utilidades del backend
│   ├── reporte_profesional.py
│   └── email_mailhog.py
│
├── docs/                # Documentación (GitHub Pages)
│   └── index.html
│
├── requirements.txt     # Dependencias del backend (Python)
├── README.md            # Descripción y guía del proyecto
└── .gitignore           # Archivos y carpetas a ignorar por git
```

## Requisitos

- Python 3.8+
- Node.js 18+
- pip

## Instalación y ejecución

### 1. Backend (API FastAPI)

1. Instala las dependencias de Python:
   ```bash
   pip install -r requirements.txt
   ```
2. (Opcional) Genera datos sintéticos:
   ```bash
   python data/generate_synthetic_data.py
   ```
3. Entrena los modelos:
   ```bash
   python models/train_xgboost.py
   ```
4. Inicia la API:
   ```bash
   uvicorn api.main:app --reload
   ```
   Accede a la documentación interactiva en [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Frontend (React)

1. Entra a la carpeta `frontend`:
   ```bash
   cd frontend
   ```
2. Instala las dependencias:
   ```bash
   npm install
   ```
3. Inicia la app:
   ```bash
   npm run dev
   ```
   Accede a la interfaz en [http://localhost:5173](http://localhost:5173)

## Funcionalidades principales

- Predicción de riesgo general, sobrecosto y retraso para proyectos TI.
- Gestión de proyectos en ejecución y finalización desde el frontend.
- Reentrenamiento de modelos desde la interfaz.
- Generación de reportes PDF profesionales.
- Envío de reportes por email.
- API REST documentada y lista para integración.

## Créditos

Desarrollado por Grupo 7 - RPA para la Gestión de Riesgos en Proyectos de Tecnología.
