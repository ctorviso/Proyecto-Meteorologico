import json

import pandas as pd

with open('data/locations/comunidades.json') as f:
    comunidades = json.load(f)

with open('data/locations/provincias.json') as f:
    provincias = json.load(f)

with open('data/locations/municipios.json') as f:
    municipios = json.load(f)

with open('data/locations/estaciones.json') as f:
    estaciones = json.load(f)

com_ids = comunidades.keys()
com_names = [comunidad['nombre'] for comunidad in comunidades.values()]
comunidad_lookup = {v["nombre"]: k for k, v in comunidades.items()}

prov_ids = provincias.keys()
prov_names = [provincia['nombre'] for provincia in provincias.values()]
provincia_lookup = {v["nombre"]: k for k, v in provincias.items()}

mun_ids = municipios.keys()
mun_names = [municipio['nombre'] for municipio in municipios.values()]
municipio_lookup = {v["nombre"]: k for k, v in municipios.items()}

est_ids = estaciones.keys()
est_names = [estacion['nombre'] for estacion in estaciones.values()]
estacion_lookup = {v["nombre"]: k for k, v in estaciones.items()}

estaciones_df = pd.DataFrame(estaciones).T.assign(idema=lambda x: x.index).reset_index(drop=True)
provincias_df = pd.DataFrame(provincias).T.assign(provincia_id=lambda x: x.index).reset_index(drop=True)
comunidades_df = pd.DataFrame(comunidades).T.assign(com_auto_id=lambda x: x.index).reset_index(drop=True)

provincias_df.rename(columns={'nombre': 'provincia'}, inplace=True)
comunidades_df.rename(columns={'nombre': 'comunidad'}, inplace=True)

estaciones_df['provincia_id'] = estaciones_df['provincia_id'].astype(str)
provincias_df['provincia_id'] = provincias_df['provincia_id'].astype(str)
provincias_df['com_auto_id'] = provincias_df['com_auto_id'].astype(str)
comunidades_df['com_auto_id'] = comunidades_df['com_auto_id'].astype(str)

locations_df = estaciones_df.merge(provincias_df, on='provincia_id', how='left')
locations_df = locations_df.merge(comunidades_df, on='com_auto_id', how='left')

element_cols_map = {
    'temperatura': ['tmed', 'tmax', 'tmin'],
    'lluvia': ['prec'],
    'viento': ['velmedia'],
    'humedad': ['hr_media', 'hr_min', 'hr_max']
}

label_maps = {
    'tmed': "Temperatura Media (°C)",
    'tmin': "Temperatura Mínima (°C)",
    'tmax': "Temperatura Máxima (°C)",
    'prec': "Precipitación",
    'velmedia': "Velocidad Viento",
    'racha': "Racha Viento",
    'hr_media': "Humedad Relativa",
    'hr_min': "Humedad Mínima",
    'hr_max': "Humedad Máxima"
}

color_maps = {
    'tmed': "RdYlBu_r",
    'tmin': "Blues",
    'tmax': "YlOrRd",
    'prec': "Blues",
    'velmedia': "Greens",
    'racha': "BuGn",
    'hr_media': "YlGn",
    'hr_min': "Greens",
    'hr_max': "Reds"
}
