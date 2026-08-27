import geopandas as gpd
import pandas as pd
import re
import os

localidades_map = {
    '1': 'Usaquén', '01': 'Usaquén', 'Usaquen': 'Usaquén', 'Usaqun': 'Usaquén',
    '2': 'Chapinero', '02': 'Chapinero',
    '3': 'Santa Fe', '03': 'Santa Fe', 'Santa fe': 'Santa Fe',
    '4': 'San Cristóbal', '04': 'San Cristóbal', 'San Cristobal': 'San Cristóbal', 'San Cristbal': 'San Cristóbal',
    '5': 'Usme', '05': 'Usme',
    '6': 'Tunjuelito', '06': 'Tunjuelito',
    '7': 'Bosa', '07': 'Bosa',
    '8': 'Kennedy', '08': 'Kennedy',
    '9': 'Fontibón', '09': 'Fontibón', 'Fontibon': 'Fontibón', 'Fontibn': 'Fontibón',
    '10': 'Engativá', 'Engativa': 'Engativá', 'Engativ': 'Engativá',
    '11': 'Suba',
    '12': 'Barrios Unidos',
    '13': 'Teusaquillo',
    '14': 'Los Mártires', 'Los Martires': 'Los Mártires', 'Los Mrtires': 'Los Mártires',
    '15': 'Antonio Nariño', 'Antonio Narino': 'Antonio Nariño', 'Antonio Nario': 'Antonio Nariño',
    '16': 'Puente Aranda',
    '17': 'La Candelaria',
    '18': 'Rafael Uribe Uribe',
    '19': 'Ciudad Bolívar', 'Ciudad Bolivar': 'Ciudad Bolívar', 'Ciudad Bolvar': 'Ciudad Bolívar',
    '20': 'Sumapaz'
}

def clean_text_encoding(txt):
    if not txt or pd.isna(txt) or str(txt).strip() in ['', 'nan', 'None']:
        return ''
    s = str(txt).strip()
    s = s.replace('\ufffd', 'ó')
    return s

def format_bogota_address(addr):
    if not addr or str(addr).strip() in ['', 'nan', 'None']:
        return ''
    
    s = str(addr).strip()
    s = clean_text_encoding(s)
    
    # Quitar prefijos repetidos de localidad
    s = re.sub(r'^(localidad\s*\d+\s*-\s*|\w+\s*-\s*)', '', s, flags=re.IGNORECASE)
    
    # 1. Normalizar tipos de vía principales
    s = re.sub(r'\b(cll|cl|calle|calles)\b\.?', 'Calle', s, flags=re.IGNORECASE)
    s = re.sub(r'\b(kra|kr|cra|cr|carrera|carreras)\b\.?', 'Carrera', s, flags=re.IGNORECASE)
    s = re.sub(r'\b(dg|diag|diagonal|diagonales)\b\.?', 'Diagonal', s, flags=re.IGNORECASE)
    s = re.sub(r'\b(tv|trans|transversal|transversales)\b\.?', 'Transversal', s, flags=re.IGNORECASE)
    s = re.sub(r'\b(av|avenida|ak|ac)\b\.?', 'Av.', s, flags=re.IGNORECASE)
    s = re.sub(r'\b(auto|autopista)\b\.?', 'Autopista', s, flags=re.IGNORECASE)
    
    # 2. Normalizar orientaciones y complementos
    s = re.sub(r'\b(sur|s)\b\.?', 'Sur', s, flags=re.IGNORECASE)
    s = re.sub(r'\b(este|e|esté)\b\.?', 'Este', s, flags=re.IGNORECASE)
    s = re.sub(r'\b(norte|n)\b\.?', 'Norte', s, flags=re.IGNORECASE)
    s = re.sub(r'\b(occidente|occ)\b\.?', 'Occidente', s, flags=re.IGNORECASE)
    s = re.sub(r'\b(oriente|or)\b\.?', 'Oriente', s, flags=re.IGNORECASE)
    s = re.sub(r'\b(bis)\b\.?', 'Bis', s, flags=re.IGNORECASE)
    
    # 3. Conectores entre vías
    s = re.sub(r'(Calle\s+[\w\d]+(?:\s+Sur)?(?:\s+Este)?)\s+(Carrera|Diagonal|Transversal|Av\.)', r'\1 con \2', s, flags=re.IGNORECASE)
    s = re.sub(r'(Carrera\s+[\w\d]+(?:\s+Sur)?(?:\s+Este)?)\s+(Calle|Diagonal|Transversal|Av\.)', r'\1 con \2', s, flags=re.IGNORECASE)
    s = re.sub(r'(Diagonal\s+[\w\d]+(?:\s+Sur)?(?:\s+Este)?)\s+(Transversal|Carrera|Calle|Av\.)', r'\1 con \2', s, flags=re.IGNORECASE)
    s = re.sub(r'(Transversal\s+[\w\d]+(?:\s+Sur)?(?:\s+Este)?)\s+(Carrera|Calle|Diagonal|Av\.)', r'\1 con \2', s, flags=re.IGNORECASE)
    
    s = re.sub(r'(Calle\s+[\w\d]+(?:\s+Sur)?(?:\s+Este)?)\s+(\d+[a-zA-Z]?)', r'\1 con Carrera \2', s)
    s = re.sub(r'(Carrera\s+[\w\d]+(?:\s+Sur)?(?:\s+Este)?)\s+(\d+[a-zA-Z]?)', r'\1 con Calle \2', s)
    s = re.sub(r'(Diagonal\s+[\w\d]+(?:\s+Sur)?(?:\s+Este)?)\s+(\d+[a-zA-Z]?)', r'\1 con Transversal \2', s)

    s = re.sub(r'\b(y|con)\b', 'con', s, flags=re.IGNORECASE)
    s = re.sub(r'\b(entre)\b', 'entre', s, flags=re.IGNORECASE)
    s = re.sub(r'\b(a la|a)\b', 'a', s, flags=re.IGNORECASE)
    s = re.sub(r'\b(no|num|numero)\b\.?', '# ', s, flags=re.IGNORECASE)

    # Limpiar espacios
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'#\s+', '# ', s)
    s = re.sub(r'-\s+', '- ', s)
    
    # Title casing de palabras
    words = s.split(' ')
    clean_words = []
    for w in words:
        wl = w.lower()
        if wl in ['con', 'y', 'de', 'la', 'el', 'los', 'las', 'entre', 'a', 'al', 'en']:
            clean_words.append(wl)
        elif wl in ['sur', 'este', 'bis', 'norte', 'occidente', 'oriente']:
            clean_words.append(w.capitalize())
        elif wl == 'av.':
            clean_words.append('Av.')
        else:
            clean_words.append(w.capitalize())
            
    res = ' '.join(clean_words)
    res = re.sub(r'(\d+)\s*([a-zA-Z])\b', lambda m: m.group(1) + m.group(2).upper(), res)
    return res

base_dir = os.path.dirname(os.path.abspath(__file__))
raw_dir = os.path.join(base_dir, "..", "01_DATOS", "01_RAW")
pred_path = os.path.join(base_dir, "05_predicciones", "riesgo_predicho.gpkg")
ranking_path = os.path.join(base_dir, "07_resultados", "ranking_zonas.csv")

puntos = gpd.read_file(os.path.join(raw_dir, "puntos_criticos_arrojo_clandestino_residuos.geojson"))
reportes = gpd.read_file(os.path.join(raw_dir, "Geopackage.gpkg"))
df_pred = gpd.read_file(pred_path)

puntos_3116 = puntos.to_crs(epsg=3116)
reportes_3116 = reportes.to_crs(epsg=3116)

dir_col = [c for c in puntos.columns if 'direc' in c.lower()][0]
puntos_3116['loc_clean'] = puntos_3116['Nombre_Localidad'].astype(str).map(lambda x: localidades_map.get(x, f"Localidad {x}"))
puntos_3116['dir_clean'] = puntos_3116[dir_col].apply(format_bogota_address)

reportes_3116['barrio_clean'] = reportes_3116['Barrio'].apply(clean_text_encoding)
reportes_3116['dir_clean'] = reportes_3116['Direccion'].apply(format_bogota_address)

centroides = df_pred.copy()
centroides.geometry = centroides.geometry.centroid

near_puntos = gpd.sjoin_nearest(centroides, puntos_3116[['geometry', 'loc_clean', 'dir_clean']], how='left', distance_col='dist_p')
near_puntos = near_puntos.drop_duplicates(subset=['id_celda'])

near_rep = gpd.sjoin_nearest(centroides, reportes_3116[['geometry', 'barrio_clean', 'dir_clean']], how='left', distance_col='dist_r')
near_rep = near_rep.drop_duplicates(subset=['id_celda'])

cols_to_drop = ['loc_clean', 'dir_p', 'dir_r', 'barrio_clean', 'dist_p', 'dist_r', 'dist_rep', 'nombre_lugar', 'loc_name', 'punto_str', 'Barrio', 'Direccion']
for c in cols_to_drop:
    if c in df_pred.columns:
        df_pred = df_pred.drop(columns=[c])

df_pred = df_pred.merge(near_puntos[['id_celda', 'loc_clean', 'dir_clean', 'dist_p']].rename(columns={'dir_clean': 'dir_p'}), on='id_celda', how='left')
df_pred = df_pred.merge(near_rep[['id_celda', 'barrio_clean', 'dir_clean', 'dist_r']].rename(columns={'dir_clean': 'dir_r', 'dist_r': 'dist_rep'}), on='id_celda', how='left')

df_pred['loc_name'] = df_pred['loc_clean'].map(lambda x: localidades_map.get(str(x), str(x)))

def construir_etiqueta_clara(row):
    loc = str(row['loc_name']).strip()
    barrio = str(row['barrio_clean']).strip() if pd.notna(row['barrio_clean']) and str(row['barrio_clean']).strip() not in ['', 'nan', 'None'] else ''
    dir_r = str(row['dir_r']).strip() if pd.notna(row['dir_r']) and str(row['dir_r']).strip() not in ['', 'nan', 'None'] else ''
    dir_p = str(row['dir_p']).strip() if pd.notna(row['dir_p']) and str(row['dir_p']).strip() not in ['', 'nan', 'None'] else ''
    dist_rep = row['dist_rep'] if pd.notna(row['dist_rep']) else 99999
    
    # 1. Si la celda está muy cerca de un reporte ciudadano (<= 250m) y es en Santa Fe
    if dist_rep <= 250 and barrio and loc in ['Santa Fe', 'La Candelaria', 'San Cristóbal']:
        if dir_r:
            return f"{loc} • Barrio {barrio} ({dir_r})"
        return f"{loc} • Barrio {barrio}"
    
    # 2. Si hay dirección limpia de punto crítico en su localidad
    if dir_p and dir_p.lower() not in ['', 'nan', 'none']:
        return f"{loc} • {dir_p}"
    elif dir_r and dist_rep <= 500:
        return f"{loc} • {dir_r}"
    else:
        return f"{loc} • Sector Cuadrante {row['id_celda']}"

df_pred['nombre_lugar'] = df_pred.apply(construir_etiqueta_clara, axis=1)

# Limpiar columnas auxiliares
df_pred = df_pred.drop(columns=['dir_p', 'dir_r', 'dist_p', 'dist_rep', 'barrio_clean', 'loc_clean'])

# Guardar de nuevo
df_pred.to_file(pred_path, driver='GPKG')

# Actualizar ranking
ranking = df_pred[['id_celda', 'loc_name', 'nombre_lugar', 'nivel_riesgo', 'probabilidad_riesgo', 'indice_prioridad', 'accion_recomendada', 'num_reportes', 'num_cestas', 'tiene_macroruta']].sort_values(by='indice_prioridad', ascending=False).head(100)
ranking.to_csv(ranking_path, index=False)

print("Enriquecimiento y estandarización completada con éxito!")


