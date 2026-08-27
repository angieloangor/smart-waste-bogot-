import json
import os

def create_notebook(filename, cells):
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.5"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)

def md_cell(text):
    return {"cell_type": "markdown", "metadata": {}, "source": [text]}

def code_cell(code):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [code]}

exploracion_cells = [
    md_cell("# Exploración de Datos: Bogotá Residuos Inteligente\nEn este notebook realizaremos una exploración inicial de los datasets base para entender su estructura, valores nulos y distribuciones."),
    code_cell("import geopandas as gpd\nimport pandas as pd\nimport matplotlib.pyplot as plt\nimport os\n\n# Definir rutas\nRAW_DIR = '../01_DATOS/01_RAW'"),
    code_cell("# Cargar datos\npuntos_criticos = gpd.read_file(f\"{RAW_DIR}/puntos_criticos_arrojo_clandestino_residuos.geojson\")\ncestas = gpd.read_file(f\"{RAW_DIR}/cestas.gpkg\")\nmacrorutas = gpd.read_file(f\"{RAW_DIR}/macrorutas_de_barrido.gpkg\")\nreportes = gpd.read_file(f\"{RAW_DIR}/Geopackage.gpkg\")\n\nprint(\"Puntos críticos:\", puntos_criticos.shape)\nprint(\"Cestas:\", cestas.shape)\nprint(\"Macrorutas:\", macrorutas.shape)\nprint(\"Reportes:\", reportes.shape)"),
    code_cell("# Información de Reportes\nreportes.info()\nprint(\"\\nNulos en reportes:\\n\", reportes.isna().sum())\nprint(\"\\nDuplicados en reportes:\", reportes.duplicated().sum())")
]

limpieza_cells = [
    md_cell("# Limpieza y Normalización Espacial\nConvertimos los CRS a EPSG:3116 y limpiamos valores nulos/incorrectos."),
    code_cell("import geopandas as gpd\nimport pandas as pd\nimport os\n\nRAW_DIR = '../01_DATOS/01_RAW'\nPROC_DIR = '../01_DATOS/02_PROCESADOS'\n\n# Cargar\npuntos = gpd.read_file(f\"{RAW_DIR}/puntos_criticos_arrojo_clandestino_residuos.geojson\")\ncestas = gpd.read_file(f\"{RAW_DIR}/cestas.gpkg\")\nmacrorutas = gpd.read_file(f\"{RAW_DIR}/macrorutas_de_barrido.gpkg\")\nreportes = gpd.read_file(f\"{RAW_DIR}/Geopackage.gpkg\")"),
    code_cell("# Normalizar CRS a EPSG:3116\nTARGET_CRS = 'EPSG:3116'\npuntos_3116 = puntos.to_crs(TARGET_CRS)\ncestas_3116 = cestas.to_crs(TARGET_CRS)\nmacrorutas_3116 = macrorutas.to_crs(TARGET_CRS)\nreportes_3116 = reportes.to_crs(TARGET_CRS)"),
    code_cell("# Limpieza básica\n# Eliminar nulos en geometría\nreportes_3116 = reportes_3116.dropna(subset=['geometry'])\nreportes_3116 = reportes_3116[reportes_3116.is_valid]\n\npuntos_3116 = puntos_3116.dropna(subset=['geometry'])\npuntos_3116 = puntos_3116[puntos_3116.is_valid]\n\ncestas_3116 = cestas_3116.dropna(subset=['geometry'])\ncestas_3116 = cestas_3116[cestas_3116.is_valid]"),
    code_cell("# Guardar limpios\npuntos_3116.to_file(f\"{PROC_DIR}/puntos_limpios.gpkg\", driver='GPKG')\ncestas_3116.to_file(f\"{PROC_DIR}/cestas_limpias.gpkg\", driver='GPKG')\nreportes_3116.to_file(f\"{PROC_DIR}/reportes_limpios.gpkg\", driver='GPKG')\nmacrorutas_3116.to_file(f\"{PROC_DIR}/macrorutas_limpias.gpkg\", driver='GPKG')\n\nprint(\"Datos limpios y normalizados exportados a 02_PROCESADOS.\")")
]

create_notebook('01_exploracion.ipynb', exploracion_cells)
create_notebook('02_limpieza.ipynb', limpieza_cells)
print("Notebooks creados.")
