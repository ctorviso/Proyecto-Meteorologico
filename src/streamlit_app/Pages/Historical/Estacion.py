import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from helpers.lookups import element_cols_map
from src.api.routes.db_routes import elements
from src.streamlit_app.components import filters
from src.streamlit_app.components.maps import estacion_map
from helpers import api

fig = go.Figure()

with st.columns([1, 3, 1])[1]:
    com_id, prov_id, idema = filters.estacion_filter()

    estacion_map(fig, idema)
    fecha_ini, fecha_fin = filters.date_range_filter()

with st.columns([1, 3, 1])[1]:
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

with st.spinner("Cargando datos..."):
    data = api.get_historico(
        idemas=[idema],
        fecha_ini=fecha_ini,
        fecha_fin=fecha_fin
    )

    if data:
        st.success("Datos obtenidos correctamente.")
        df = pd.DataFrame(data)
        cols = ['fecha']
        for element in elements:
            cols.extend(element_cols_map[element])
        st.write(df[cols].sort_values("fecha"))
