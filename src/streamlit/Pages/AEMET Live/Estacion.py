import streamlit as st
import pandas as pd
from src.api.services import http_request
from src.streamlit.config import aemet_url, db_url

comunidades_url = db_url + "/comunidades_autonomas"
comunidades = http_request.make_request(url=comunidades_url, method='get')[0]
com_names = [comunidad['nombre'] for comunidad in comunidades]
com_ids = [comunidad['id'] for comunidad in comunidades]
comunidad = st.selectbox("Selecciona la comunidad autónoma", com_names)
com_id = com_ids[com_names.index(comunidad)]

provincias_url = db_url + "/provincias"
provincias = http_request.make_request(url=provincias_url, method='get')[0]
prov_names = [provincia['nombre'] for provincia in provincias if provincia['com_auto_id'] == com_id]
prov_ids = [provincia['id'] for provincia in provincias if provincia['com_auto_id'] == com_id]
provincia = st.selectbox("Selecciona la provincia", prov_names)

estaciones_url = db_url + "/estaciones"
estaciones = http_request.make_request(url=estaciones_url, method='get')[0]
est_names = [estacion['nombre'] for estacion in estaciones if estacion['provincia_id'] == prov_ids[prov_names.index(provincia)]]
est_ids = [estacion['idema'] for estacion in estaciones if estacion['provincia_id'] == prov_ids[prov_names.index(provincia)]]
estacion = st.selectbox("Selecciona la estación meteorológica", est_names)
idema = est_ids[est_names.index(estacion)]

estacion_endpoint = "/tiempo-actual/estacion/{idema}"

if st.button("Obtener datos de la estación"):
    estacion_url = aemet_url + estacion_endpoint.format(idema=idema)
    response = http_request.make_request(url=estacion_url, method='get')
    data = response[0]
    status = response[1]
    if status != 200:
        st.error(f"Error al obtener los datos: {status}")
    else:
        st.success("Datos obtenidos correctamente")
        df = pd.DataFrame(data)
        st.write(df)

