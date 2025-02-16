import json
from src.shared.helpers import get_env_var

host = get_env_var("HOST")

if host == "localhost":
    aemet_url = f"http://{host}:8000/api/aemet"
    db_url = f"http://{host}:8000/api/db"
else:
    aemet_url = f"https://{host}/api/aemet"
    db_url = f"https://{host}/api/db"

with open('src/streamlit/data/comunidades.json') as f:
    comunidades = json.load(f)

with open('src/streamlit/data/provincias.json') as f:
    provincias = json.load(f)

with open('src/streamlit/data/municipios.json') as f:
    municipios = json.load(f)

with open('src/streamlit/data/estaciones.json') as f:
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
