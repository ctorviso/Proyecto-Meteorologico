from functools import reduce

import numpy as np
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
from helpers.lookups import locations_df, element_cols_map_numeric, label_maps, choropleth_color_maps, \
    histogram_color_maps, numeric_cols
from helpers.maps.folium import spain_map, create_tooltip, get_column_choropleth
from helpers.maps.geojson import inject_col_values
from helpers.preprocessing import convert_numeric
from helpers.visualization import histograms, scatter_matrix
from helpers import api
from src.streamlit_app.components.filters import date_range_filter, element_filter

st.title("Análisis Exploratorio de Datos")

fecha_inicial, fecha_final = date_range_filter()

def show_graphs():
    options = {
        "Histogramas": show_histograms,
        "Scatter Matrix": show_scatter_matrix,
        "Mapa Coroplético": choropleth_map
    }

    option = st.radio(
        options=options,
        label="Selecciona la visualización:"
    )

    options[option]()

def show_histograms():
    st.header("Histogramas")

    data = api.get_historico_average(
        fecha_ini=fecha_inicial,
        fecha_fin=fecha_final
    )

    if not data:
        st.error("No hay datos disponibles para el rango seleccionado.")
        return

    df = pd.DataFrame(data)
    df['provincia_id'] = df['provincia_id'].astype(str)
    df = df.merge(locations_df, on="provincia_id", how="left").sort_values("fecha")
    df = convert_numeric(df, numeric_cols)

    for elemento, cols in element_cols_map_numeric.items():

        if st.checkbox("Logaritmo", key=elemento):
            df[cols] = df[cols].apply(lambda x: x.apply(lambda y: y if y == 0 else np.log(y)))

        colors = [histogram_color_maps[col] for col in cols]

        hist = histograms(
            df,
            title=f"{elemento.upper()}",
            cols=element_cols_map_numeric[elemento],
            x_label=elemento,
            colors=colors
        )
        st.plotly_chart(hist, use_container_width=True)

def show_scatter_matrix():
    st.header("Scatter Matrix")
    
    dfs = []
    scatter_elements = ['temperatura', 'lluvia', 'viento', 'humedad']

    data = api.get_historico_average(
        elementos=scatter_elements,
        fecha_ini=fecha_inicial,
        fecha_fin=fecha_final
    )

    if not data:
        st.error("No hay datos disponibles para el rango seleccionado.")
        return

    cols = [cols[0] for element, cols in element_cols_map_numeric.items() if element in scatter_elements]

    for col in cols:
        df_var = pd.DataFrame(data)[['provincia_id', 'fecha', col]]
        dfs.append(df_var)
    
    df = reduce(
        lambda left, right: pd.merge(left, right, on=['provincia_id', 'fecha'], how='outer'),
        dfs
    )

    if all(var in df.columns for var in cols):
        fig = scatter_matrix(
            df,
            title="Scatter Matrix de Variables Meteorológicas",
            cols=cols,
            color='LightSkyBlue'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("No se pueden visualizar todas las variables en el Scatter Matrix.")

def choropleth_map():
    st.header(f"Mapa Coroplético")

    st.write("Selecciona el elemento:")
    elemento = element_filter()

    data = api.get_historico_average(
        fecha_ini=fecha_inicial,
        fecha_fin=fecha_final
    )

    if not data:
        st.error("No hay datos disponibles para el rango seleccionado.")
        return

    avg_df = pd.DataFrame(data)
    avg_df['provincia_id'] = avg_df['provincia_id'].astype(str)

    if elemento:
        st.write(f"Mapa Coroplético de {elemento} por provincia")

        geojson = inject_col_values(avg_df, element_cols_map_numeric[elemento])

        maps = {}

        for col in element_cols_map_numeric[elemento]:
            maps[col] = spain_map()
            choro = get_column_choropleth(geojson, avg_df, col, label_maps[col], choropleth_color_maps[col]).add_to(maps[col])
            create_tooltip(col, label_maps[col]).add_to(choro.geojson)

        selected_map = st.radio("Selecciona el variable:", list(maps.keys()))
        folium_static(maps[selected_map])

show_graphs()