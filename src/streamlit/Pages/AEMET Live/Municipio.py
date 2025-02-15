import streamlit as st
import pandas as pd
from src.api.services import http_request
from src.shared import helpers
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

municipios_url = db_url + "/municipios"
municipios = http_request.make_request(url=municipios_url, method='get')[0]
mun_names = [municipio['nombre'] for municipio in municipios if municipio['provincia_id'] == prov_ids[prov_names.index(provincia)]]
mun_ids = [municipio['id'] for municipio in municipios if municipio['provincia_id'] == prov_ids[prov_names.index(provincia)]]
municipio = st.selectbox("Selecciona el municipio", mun_names)
municipio_id = mun_ids[mun_names.index(municipio)]

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
