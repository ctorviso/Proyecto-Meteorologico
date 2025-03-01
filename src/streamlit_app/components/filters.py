import pandas as pd
import streamlit as st
from helpers.lookups import com_names, comunidad_lookup, provincias, provincia_lookup, estacion_lookup, \
    estaciones, elements


def estacion_filter():
    comunidad = st.selectbox("Selecciona la comunidad autónoma", com_names)
    com_id = comunidad_lookup[comunidad]
    st.session_state.com_id = com_id

    prov_names = [provincias[index]["nombre"] for index in provincias if
                  str(provincias[index]["com_auto_id"]) == com_id]
    provincia = st.selectbox("Selecciona la provincia", prov_names)
    prov_id = provincia_lookup[provincia]
    st.session_state.prov_id = prov_id

    est_names = [estaciones[index]["nombre"] for index in estaciones if
                 str(estaciones[index]["provincia_id"]) == prov_id]
    estacion = st.selectbox("Selecciona la estación meteorológica", est_names)
    idema = estacion_lookup[estacion]
    st.session_state.idema = idema

    return com_id, prov_id, idema


def date_range_filter():
    last_week = pd.Timestamp.now() - pd.DateOffset(weeks=2)

    ini, _, fin, _ = st.columns([2,1,2,1])

    with ini:
        fecha_ini = str(
            st.date_input(label="Fecha inicio", value=last_week,
                          max_value=pd.Timestamp.now()))  # default to last week

    with fin:
        fecha_fin = str(st.date_input(label="Fecha fin", value=pd.Timestamp.now(), max_value=pd.Timestamp.now(),
                                      min_value=fecha_ini))

    return fecha_ini, fecha_fin


def element_filter(selection_mode: str = "single"):

    container = st.container()
    with container:
        selection = st.pills(
            "Elementos",
            options=elements,
            selection_mode=selection_mode,
            label_visibility="collapsed"
        )

    return selection