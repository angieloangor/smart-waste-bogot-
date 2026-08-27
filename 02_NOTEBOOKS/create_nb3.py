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

nb3_cells = [
    md_cell("# Análisis Espacial y Feature Engineering\nEn este notebook construiremos la grilla de 250m x 250m y realizaremos los cruces espaciales de nuestras capas limpias."),
    code_cell("import geopandas as gpd\nimport pandas as pd\nimport numpy as np\nfrom shapely.geometry import box\nimport os\n\nPROC_DIR = '../01_DATOS/02_PROCESADOS'\nMODEL_DIR = '../03_MODELO/01_dataset_modelo'"),
    code_cell("# 1. Cargar capas limpias\npuntos = gpd.read_file(f\"{PROC_DIR}/puntos_limpios.gpkg\")\ncestas = gpd.read_file(f\"{PROC_DIR}/cestas_limpias.gpkg\")\nmacrorutas = gpd.read_file(f\"{PROC_DIR}/macrorutas_limpias.gpkg\")\nreportes = gpd.read_file(f\"{PROC_DIR}/reportes_limpios.gpkg\")\n\nprint(\"Datos cargados exitosamente.\")"),
    code_cell("# 2. Construir la Grilla Espacial de 250m x 250m\n# Obtenemos el bounding box máximo que cubra los reportes y puntos críticos\nminx, miny, maxx, maxy = reportes.total_bounds\n\n# Ajustar bounds por los puntos críticos si están más lejos\nminx2, miny2, maxx2, maxy2 = puntos.total_bounds\nminx = min(minx, minx2)\nminy = min(miny, miny2)\nmaxx = max(maxx, maxx2)\nmaxy = max(maxy, maxy2)\n\n# Tamaño de celda en metros\ncell_size = 250\n\ngrid_cells = []\nfor x0 in np.arange(minx, maxx, cell_size):\n    for y0 in np.arange(miny, maxy, cell_size):\n        x1 = x0 + cell_size\n        y1 = y0 + cell_size\n        grid_cells.append(box(x0, y0, x1, y1))\n\ngrilla = gpd.GeoDataFrame(grid_cells, columns=['geometry'], crs='EPSG:3116')\ngrilla['id_celda'] = [f\"C{str(i).zfill(5)}\" for i in range(len(grilla))]\nprint(f\"Se generó una grilla de {len(grilla)} celdas de {cell_size}m x {cell_size}m.\")"),
    code_cell("# 3. Cruce Espacial (Spatial Join)\n# 3.1 Reportes por celda\nreportes_grilla = gpd.sjoin(reportes, grilla, how='inner', predicate='intersects')\nreportes_count = reportes_grilla.groupby('id_celda').size().reset_index(name='num_reportes')\n\n# 3.2 Puntos Críticos (cercanos)\npuntos_grilla = gpd.sjoin(puntos, grilla, how='inner', predicate='intersects')\npuntos_count = puntos_grilla.groupby('id_celda').size().reset_index(name='num_puntos_criticos')\n\n# 3.3 Cestas\ncestas_grilla = gpd.sjoin(cestas, grilla, how='inner', predicate='intersects')\ncestas_count = cestas_grilla.groupby('id_celda').size().reset_index(name='num_cestas')\n\n# 3.4 Cobertura de barrido (Macrorutas)\nmacrorutas_grilla = gpd.sjoin(macrorutas, grilla, how='inner', predicate='intersects')\nmacrorutas_celdas = macrorutas_grilla['id_celda'].unique()\n"),
    code_cell("# 4. Consolidar variables en la grilla\ngrilla_modelo = grilla.merge(reportes_count, on='id_celda', how='left')\ngrilla_modelo = grilla_modelo.merge(puntos_count, on='id_celda', how='left')\ngrilla_modelo = grilla_modelo.merge(cestas_count, on='id_celda', how='left')\n\n# Rellenar nulos con 0\ngrilla_modelo['num_reportes'] = grilla_modelo['num_reportes'].fillna(0)\ngrilla_modelo['num_puntos_criticos'] = grilla_modelo['num_puntos_criticos'].fillna(0)\ngrilla_modelo['num_cestas'] = grilla_modelo['num_cestas'].fillna(0)\n\n# Variable de cobertura (1 = Sí, 0 = No)\ngrilla_modelo['tiene_macroruta'] = grilla_modelo['id_celda'].apply(lambda x: 1 if x in macrorutas_celdas else 0)\n\n# Filtrar grilla para conservar solo zonas relevantes (ej. que tengan al menos 1 reporte, cesta, macroruta o punto)\ngrilla_activa = grilla_modelo[(grilla_modelo['num_reportes'] > 0) | \n                              (grilla_modelo['num_puntos_criticos'] > 0) | \n                              (grilla_modelo['tiene_macroruta'] == 1) | \n                              (grilla_modelo['num_cestas'] > 0)].copy()\nprint(f\"Celdas activas en Bogotá (con algún dato de interés): {len(grilla_activa)}\")"),
    code_cell("# 5. Distancias a infraestructuras (Distancia al elemento más cercano)\n# Nota: Calcular distancias puede ser intensivo. \n# Usamos sjoin_nearest para encontrar la cesta y punto crítico más cercano al centroide de la celda.\n\ncentroides = grilla_activa.copy()\ncentroides.geometry = centroides.geometry.centroid\n\n# Distancia a la cesta más cercana\nif len(cestas) > 0:\n    # El sjoin_nearest añade la distancia si especificamos distance_col\n    dist_cestas = gpd.sjoin_nearest(centroides, cestas, how='left', distance_col='dist_cesta_mas_cercana')\n    # Como puede devolver duplicados (empates de distancia), agrupamos y tomamos el mínimo real:\n    min_dist_cestas = dist_cestas.groupby('id_celda')['dist_cesta_mas_cercana'].min().reset_index()\n    grilla_activa = grilla_activa.merge(min_dist_cestas, on='id_celda', how='left')\nelse:\n    grilla_activa['dist_cesta_mas_cercana'] = 9999\n\n# Distancia a punto crítico más cercano\nif len(puntos) > 0:\n    dist_puntos = gpd.sjoin_nearest(centroides, puntos, how='left', distance_col='dist_punto_critico')\n    min_dist_puntos = dist_puntos.groupby('id_celda')['dist_punto_critico'].min().reset_index()\n    grilla_activa = grilla_activa.merge(min_dist_puntos, on='id_celda', how='left')\nelse:\n    grilla_activa['dist_punto_critico'] = 9999\n\n# Rellenar con un valor alto si no hay infra cercana en absoluto\ngrilla_activa['dist_cesta_mas_cercana'] = grilla_activa['dist_cesta_mas_cercana'].fillna(9999)\ngrilla_activa['dist_punto_critico'] = grilla_activa['dist_punto_critico'].fillna(9999)\n"),
    code_cell("# 6. Definición del Target y guardado del Dataset Analítico\n# Definiremos un riesgo histórico simple por ahora para entrenar (ej. target = 1 si hay puntos críticos > 0 o reportes > umbral)\numbral_reportes = grilla_activa['num_reportes'].quantile(0.85) if grilla_activa['num_reportes'].max() > 0 else 0\n\ngrilla_activa['target_riesgo'] = np.where(\n    (grilla_activa['num_puntos_criticos'] > 0) | (grilla_activa['num_reportes'] >= umbral_reportes),\n    1, 0\n)\n\nprint(f\"Distribución del Target:\\n{grilla_activa['target_riesgo'].value_counts()}\")\n\n# Guardar el dataset completo espacial\ngrilla_activa.to_file(f\"{MODEL_DIR}/dataset_modelo.gpkg\", driver='GPKG')\n\n# Guardar versión CSV para Pandas directo (sin geometría)\ngrilla_df = grilla_activa.drop(columns='geometry')\ngrilla_df.to_csv(f\"{MODEL_DIR}/dataset_modelo.csv\", index=False)\n\nprint(\"Dataset Analítico (Grilla) creado y guardado en 03_MODELO/01_dataset_modelo/\")")
]

create_notebook('03_analisis_espacial.ipynb', nb3_cells)
print("Notebook 03_analisis_espacial.ipynb creado.")
