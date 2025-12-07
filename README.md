# Sistema Inteligente de Predicción de Demanda Energética

Este proyecto implementa un sistema híbrido para predecir el consumo de energía diario, integrando datos históricos locales con datos meteorológicos reales obtenidos de una API.

## ¿Cómo funciona el sistema?

El flujo de ejecución se orquesta desde `main.py` y sigue estos 5 pasos secuenciales:

### 1. Ingesta y Limpieza (Paradigma Funcional)
- **Código**: `src/data_loader.py`
- El sistema carga el archivo `data/enunciado1_energia.csv`.
- Utiliza funciones puras de `pandas` para limpiar valores nulos y normalizar formatos de fecha.
- **Paradigma**: Transformación de datos inmutables (input -> función -> output).

### 2. Enriquecimiento de Datos (API Externa)
- **Código**: `src/weather_service.py`
- Se conecta a la API pública de **Open-Meteo**.
- Busca el clima histórico real (temperatura, lluvias) para las fechas encontradas en tu CSV.
- Combina (hace "merge") los datos de tu CSV con los datos reales del clima.

### 3. Modelado de Usuarios (Paradigma OOP)
- **Código**: `src/models.py`
- Convierte la columna de texto "Tipo de Usuario" (Residencial, Industrial, etc.) en **Objetos Python**.
- Aplica **Polimorfismo**: Cada objeto calcula su tarifa o impacto de forma diferente según su clase (`UsuarioIndustrial`, `UsuarioResidencial`, etc.).

### 4. Predicción (Machine Learning)
- **Código**: `src/predictor.py`
- Entrena un modelo de **Regresión Lineal**.
- Aprende la relación entre: *Temperatura, Humedad, Tipo de Usuario* -> *Consumo (kWh)*.
- Genera una predicción matemática basada en esos patrones.

### 5. Visualización
- **Código**: `src/visualizer.py`
- Genera gráficos en la carpeta `output/`:
    - Tendencias de consumo.
    - Comparación de lo Real vs lo que el Modelo Predijo.

## Cómo Ejecutarlo

1. Asegúrate de tener las librerías instaladas:
   ```bash
   pip install -r requirements.txt
   ```
2. Corre el script principal:
   ```bash
   python main.py
   ```
3. Revisa la carpeta `output/` para ver los resultados.

## 🌐 Dashboard Interactivo (UI Profesional)

Para una experiencia visual e interactiva, el proyecto incluye un dashboard web construido con **Streamlit**.

### Características:
- **Carga de Archivos**: Sube tus propios datasets CSV.
- **Geolocalización**: Selecciona entre +30 ciudades globales para ajustar la predicción al clima local.
- **Gráficos Interactivos**: Explora los datos con zoom y tooltips usando **Plotly**.

#### Ejecución del Dashboard:
```bash
streamlit run app_dashboard.py
```

<img width="1896" height="910" alt="image" src="https://github.com/user-attachments/assets/94ff692e-41d4-4080-babc-4e1f22fddd30" />



