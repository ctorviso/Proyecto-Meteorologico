import streamlit as st
import pandas as pd

from src.streamlit import requester
from src.streamlit.config import api_url, \
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

ini, fin = st.columns(2)

with ini:
    fecha_ini = str(st.date_input(label="Fecha inicio"))

with fin:
    fecha_fin = str(st.date_input(label="Fecha fin"))

endpoint = "/db/historico/estacion/{idema}/{elemento}/rango/{fecha_ini}/{fecha_fin}"

elements = ["lluvia", "temperatura", "viento", "humedad"]

selection = st.pills(
    "Elemento",
    options=elements,
    selection_mode="multi",
)

for element in selection:
    data = requester.get_request(endpoint.format(elemento=element, idema=idema, fecha_ini=fecha_ini, fecha_fin=fecha_fin))
    st.title(element)

    if len(data) == 0:
        st.error("No hay datos disponibles para el rango de fechas seleccionado")
        continue

    df = pd.DataFrame(data)
    st.write(df)
