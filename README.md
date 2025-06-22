# RPA para la Gestión de Riesgos en Proyectos de Tecnología

Este proyecto utiliza RPA e Inteligencia Artificial para evaluar riesgos en proyectos de tecnología, usando modelos de Machine Learning y datos históricos simulados. Incluye una API predictiva y generación automática de reportes.

## Estructura del proyecto

```
RiskPredictor-RPA/
│
├── data/                # Datasets sintéticos y archivos de datos
│   └── synthetic_data.csv
│
├── models/              # Modelos entrenados y scripts de entrenamiento
│   ├── train_model.py
│   └── model.pkl
│
├── api/                 # Código de la API predictiva (FastAPI)
│   └── main.py
│
├── reports/             # Reportes generados automáticamente
│   └── example_report.pdf
│
├── utils/               # Utilidades y funciones auxiliares
│   └── data_preprocessing.py
│
├── requirements.txt     # Dependencias del proyecto
├── README.md            # Descripción y guía del proyecto
└── .gitignore           # Archivos y carpetas a ignorar por git
```

## Requisitos
- Python 3.8+
- scikit-learn
- xgboost
- fastapi
- uvicorn
- pandas
- joblib

## Instrucciones básicas

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Genera o coloca el dataset sintético en `data/synthetic_data.csv`.
3. Entrena el modelo ejecutando:
   ```bash
   python models/train_model.py
   ```
4. Inicia la API:
   ```bash
   uvicorn api.main:app --reload
   ```
5. Accede a la API en [http://localhost:8000](http://localhost:8000)

## Créditos
Grupo 7 - RPA para la Gestión de Riesgos en Proyectos de Tecnología

