# RiskPredictor-RPA: Predicción y Gestión de Riesgos en Proyectos TI

Este proyecto implementa un sistema completo para la predicción y gestión de riesgos en proyectos de tecnología, combinando Machine Learning, una API REST (FastAPI) y un frontend moderno en React.

## Estructura del proyecto

```
RiskPredictor-RPA/
│
├── data/                # Datasets sintéticos, opciones de formulario y proyectos en ejecución
│   ├── synthetic_data_with_outputs.csv
│   ├── opciones_formulario.json
│   └── proyectos_ejecucion.csv
│
├── models/              # Modelos entrenados y scripts de entrenamiento
│   ├── train_xgboost.py
│   ├── modelo_xgb_riesgo_general.pkl
│   ├── modelo_xgb_sobrecosto.pkl
│   ├── modelo_xgb_retraso.pkl
│   └── encoders (archivos .pkl de LabelEncoder y MultiLabelBinarizer)
│
├── api/                 # Código de la API predictiva (FastAPI)
│   └── main.py
│
├── frontend/            # Aplicación React para la interacción de usuario
│   ├── src/
│   │   ├── App.tsx
│   │   ├── ProyectosEjecucion.tsx
│   │   └── App.css
│   └── ...
│
├── reports/             # (Opcional) Reportes generados automáticamente
│
├── utils/               # Utilidades y funciones auxiliares
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

## ¿Qué incluye cada carpeta?
- **data/**: Datasets sintéticos, opciones de formulario y proyectos en ejecución (archivos CSV y JSON).
- **models/**: Scripts de entrenamiento y modelos/encoders entrenados (archivos .pkl).
- **api/**: Código de la API REST (FastAPI) que expone endpoints para predicción, gestión de proyectos y reentrenamiento.
- **frontend/**: Aplicación React con formularios dinámicos, listado de proyectos en ejecución y visualización de resultados.
- **reports/**: (Opcional) Reportes generados automáticamente.
- **utils/**: Funciones auxiliares para preprocesamiento y utilidades.

## Funcionalidades principales
- Predicción de riesgo general, sobrecosto y retraso para proyectos TI.
- Gestión de proyectos en ejecución y finalización desde el frontend.
- Reentrenamiento de modelos desde la interfaz.
- API REST documentada y lista para integración.

## Créditos
Desarrollado por Grupo 7 - RPA para la Gestión de Riesgos en Proyectos de Tecnología.

