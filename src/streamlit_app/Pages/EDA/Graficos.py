from functools import reduce

import folium
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
from helpers.lookups import locations_df, element_cols_map_numeric, label_maps, choropleth_color_maps, \
    histogram_color_maps, numeric_cols, scatter_cols, scatter_color_maps
from helpers.maps.folium import spain_map, create_tooltip, get_column_choropleth
from helpers.maps.geojson import inject_col_values
from helpers.preprocessing import convert_numeric
from helpers.visualization import histograms, scatter_matrix
from helpers import api
from src.streamlit_app.components.filters import date_range_filter, element_filter

st.title("Análisis Exploratorio de Datos")

with st.sidebar:
    fecha_inicial, fecha_final = date_range_filter()

    with st.spinner("Cargando datos..."):
        data = api.get_historico_average(
            fecha_ini=fecha_inicial,
            fecha_fin=fecha_final
        )

selected_element = element_filter()

def show_graphs():

    show_choropleth_map()
    show_histograms()
    show_scatter_matrix()

def show_histograms():
    st.header("Histogramas")

    if not data:
        st.error("No hay datos disponibles para el rango seleccionado.")
        return

    df = pd.DataFrame(data)
    df['provincia_id'] = df['provincia_id'].astype(str)
    df = df.merge(locations_df, on="provincia_id", how="left").sort_values("fecha")
    df = convert_numeric(df, numeric_cols)

    cols = element_cols_map_numeric[selected_element]
    if st.checkbox("Logaritmo", key=selected_element):
        df[cols] = df[cols].apply(lambda x: x.apply(lambda y: y if y == 0 else np.log(y)))

    colors = [histogram_color_maps[col] for col in cols]

    hist = histograms(
        df,
        title=f"{selected_element.upper()}",
        cols=element_cols_map_numeric[selected_element],
        x_label=selected_element,
        colors=colors
    )
    st.plotly_chart(hist, use_container_width=True)

def show_scatter_matrix():
    st.header("Scatter Matrix")

    x_cols = element_cols_map_numeric[selected_element]
    y_cols = [col for col in scatter_cols if col not in x_cols]

    x_col_labels = [label_maps[col] for col in x_cols]
    y_col_labels = [label_maps[col] for col in y_cols]
    
    dfs = []
    for col in numeric_cols:
        df_var = pd.DataFrame(data)[['provincia_id', 'fecha', col]]
        dfs.append(df_var)
    
    df = reduce(
        lambda left, right: pd.merge(left, right, on=['provincia_id', 'fecha'], how='outer'),
        dfs
    )

    fig = scatter_matrix(
        df,
        title="Scatter Matrix de Variables Meteorológicas",
        x_cols=x_cols,
        y_cols= y_cols,
        x_labels=x_col_labels,
        y_labels=y_col_labels,
        color=scatter_color_maps[selected_element]
    )
    st.plotly_chart(fig, use_container_width=True)

def show_choropleth_map():

    if selected_element:

        geojson = inject_col_values(avg_df, element_cols_map_numeric[selected_element])

        maps = {}

        for col in element_cols_map_numeric[selected_element]:
            maps[col] = spain_map()

            folium.TileLayer(
                tiles='https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png',
                attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                name='Land Only',
                overlay=True
            ).add_to(maps[col])

            choro = get_column_choropleth(geojson, avg_df, col, label_maps[col], choropleth_color_maps[col]).add_to(maps[col])
            create_tooltip(col, label_maps[col]).add_to(choro.geojson)

        cols = list(maps.keys())
        col_labels = [label_maps[col] for col in cols]

        selected_label = st.radio(
            label="Selecciona el variable:",
            options=col_labels,
            label_visibility="hidden",
            horizontal=True
        )
        selected_map = cols[col_labels.index(selected_label)]

        folium_static(maps[selected_map], width=1000, height=600)

if not data:
    st.error("No hay datos disponibles para el rango seleccionado.")

else:
    avg_df = pd.DataFrame(data)
    avg_df['provincia_id'] = avg_df['provincia_id'].astype(str)

    show_graphs()