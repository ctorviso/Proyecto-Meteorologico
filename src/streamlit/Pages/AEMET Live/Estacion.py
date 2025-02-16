import streamlit as st
import pandas as pd
from src.api.services import http_request
from src.streamlit.config import aemet_url, \
    com_names, provincias, estaciones, \
    comunidad_lookup, provincia_lookup, estacion_lookup

comunidad = st.selectbox("Selecciona la comunidad autónoma", com_names)
com_id = comunidad_lookup[comunidad]

prov_names = [provincias[index]["nombre"] for index in provincias if str(provincias[index]["com_auto_id"]) == com_id]
provincia = st.selectbox("Selecciona la provincia", prov_names)
prov_id = provincia_lookup[provincia]

est_names = [estaciones[index]["nombre"] for index in estaciones if str(estaciones[index]["provincia_id"]) == prov_id]
estacion = st.selectbox("Selecciona la estación meteorológica", est_names)
idema = estacion_lookup[estacion]

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

