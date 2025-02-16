import streamlit as st
import pandas as pd
from src.api.services import http_request
from src.shared import helpers
from src.streamlit.config import aemet_url, com_names, provincias, municipios, \
    comunidad_lookup, provincia_lookup, municipio_lookup

comunidad = st.selectbox("Selecciona la comunidad autónoma", com_names)
com_id = comunidad_lookup[comunidad]

prov_names = [provincias[index]["nombre"] for index in provincias if str(provincias[index]["com_auto_id"]) == com_id]
provincia = st.selectbox("Selecciona la provincia", prov_names)
prov_id = provincia_lookup[provincia]

mun_names = [municipios[index]["nombre"] for index in municipios if str(municipios[index]["provincia_id"]) == prov_id]
municipio = st.selectbox("Selecciona el municipio", mun_names)
municipio_id = municipio_lookup[municipio]

municipio_endpoint = "/tiempo-actual/municipio/{municipio}"

def municipio_json_to_dataframe(_data):
    _df = pd.DataFrame()

    for key, values in _data.items():
        if isinstance(values, list):  # Only process list-based attributes
            temp_df = pd.DataFrame(values)
            temp_df.rename(columns={"value": key}, inplace=True)
            if "periodo" in _df.columns:
                _df = _df.merge(temp_df, on="periodo", how="outer")
            else:
                _df = temp_df

    _df["periodo"] = _df["periodo"].astype(int)
    _df.sort_values("periodo", inplace=True)
    _df.set_index("periodo", inplace=True)

    return _df[_df.index < 24]

if st.button("Obtener datos del municipio"):
    municipio_url = aemet_url + municipio_endpoint.format(municipio=municipio_id)
    response = http_request.make_request(url=municipio_url, method='get')
    data = response[0]
    status = response[1]
    if status != 200:
        st.error(f"Error al obtener los datos: {status}")
    else:
        st.success("Datos obtenidos correctamente")

        for i, day in enumerate(data):
            day_df = municipio_json_to_dataframe(day)

            date = day['fecha']
            orto = day['orto']
            ocaso = day['ocaso']

            if i == 0:
                st.title("Hoy")
            elif i == 1:
                st.title("Mañana")
            else:
                st.title("Pasado mañana")

            st.write(f"{helpers.format_fecha(date)}")
            st.write(day_df)
