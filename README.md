# Bogotá Residuos Inteligente

## 1. Descripción del problema abordado

El proyecto aborda la identificación y priorización de zonas de Bogotá con mayor riesgo de arrojo clandestino de residuos y puntos críticos de gestión ineficiente. El problema se expresa como una brecha territorial entre la actividad de reportes ciudadanos, la presencia de infraestructura de recolección y la concentración de puntos críticos de residuos en zonas de alta vulnerabilidad operativa.

La propuesta busca apoyar la toma de decisiones de autoridades y operadores mediante un diagnóstico espacial y predictivo que permita identificar dónde se deben focalizar acciones de intervención, limpieza y fortalecimiento de la red de recolección.

## 2. Pregunta analítica

¿Cómo pueden integrarse distintas fuentes públicas y datos geoespaciales para identificar las zonas de Bogotá con mayor riesgo de residuos clandestinos y priorizar intervenciones de servicio y monitoreo territorial?

## 3. Hipótesis

La combinación de variables espaciales, de infraestructura y de reportes ciudadanos permite detectar con mayor precisión las zonas de mayor riesgo y construir un modelo predictivo útil para priorizar intervenciones de recolección, limpieza y vigilancia.

## 4. Fuentes de datos utilizadas

El análisis integra fuentes públicas y datos geográficos de la ciudad de Bogotá, principalmente:

- Cestas de recolección: `cestas.gpkg`
- Macrorutas de barrido: `macrorutas_de_barrido.gpkg`
- Puntos críticos de arrojo clandestino: `puntos_criticos_arrojo_clandestino_residuos.geojson`
- Reportes / base de gestión de residuos: `Geopackage.gpkg`

Estas fuentes se encuentran en la carpeta `01_DATOS/01_RAW` del proyecto y fueron procesadas para construir un dataset analítico unificado.

## 5. Metodología general

La metodología aplicada incluye las siguientes etapas:

1. Exploración de fuentes de datos geográficos y tabulares.
2. Identificación de variables relevantes para riesgo, infraestructura y cobertura.
3. Limpieza y normalización de geometrías, atributos y campos de texto.
4. Integración espacial y tabular entre datasets.
5. Construcción de una grilla territorial para Bogotá.
6. Ingeniería de variables e indicadores de riesgo.
7. Entrenamiento y comparación de modelos predictivos.
8. Evaluación del desempeño y priorización territorial.
9. Generación de mapas de riesgo y ranking de zonas prioritarias.
10. Visualización interactiva para apoyo institucional.

## 6. Estructura del repositorio

```text
RESIDUOS_BOGOTA/
├── README.md
├── data/
│   ├── raw/
│   ├── processed/
│   └── model/
├── notebooks/
│   ├── 01_exploracion.ipynb
│   ├── 02_limpieza.ipynb
│   ├── 03_analisis_espacial.ipynb
│   └── 05_modelos.ipynb
├── outputs/
│   ├── reports/
│   ├── visualizations/
│   └── results/
├── docs/
│   ├── formulario_caracterizacion.md
│   └── nota_integracion_datos_publicos.md
├── 01_DATOS/
│   ├── 01_RAW/
│   └── 02_PROCESADOS/
├── 02_NOTEBOOKS/
├── 03_MODELO/
├── 04_APP/
│   ├── app.py
│   ├── requirements.txt
│   └── assets/
└── 05_DOCUMENTACION/
```

## 7. Requisitos de ejecución

### Requisitos previos

- Python 3.10 o superior
- GeoPandas
- Pandas
- NumPy
- Scikit-learn
- Folium
- Streamlit
- Jupyter

### Instalación

```bash
pip install -r 04_APP/requirements.txt
```

### Ejecutar la aplicación interactiva

```bash
cd RESIDUOS_BOGOTA/04_APP
streamlit run app.py
```

### Ejecutar el análisis

Se recomienda seguir el orden de notebooks:

1. `02_NOTEBOOKS/01_exploracion.ipynb`
2. `02_NOTEBOOKS/02_limpieza.ipynb`
3. `02_NOTEBOOKS/03_analisis_espacial.ipynb`
4. `02_NOTEBOOKS/05_modelos.ipynb`

## 8. Resultados esperados

- Mapa territorial de riesgo predictivo
- Ranking de zonas prioritarias
- Recomendaciones de intervención operativa
- Visualización interactiva para apoyo institucional
- Diagnóstico reproducible basado en datos públicos y geoespaciales

## 9. Consideraciones

Este proyecto fue desarrollado como una solución de análisis y apoyo a la toma de decisiones territoriales para la gestión de residuos sólidos en Bogotá. Los resultados deben interpretarse como un insumo técnico orientado a priorizar acciones operativas y de supervisión.

## 10. Créditos

Proyecto desarrollado en el marco del concurso de análisis territorial y uso de datos públicos.
