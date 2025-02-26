from functools import reduce
import folium
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_folium import folium_static
from helpers.lookups import locations_df, element_cols_map, label_maps, color_maps
from helpers.maps.folium import spain_map, add_to_map
from helpers.preprocessing import provincia_avg
from helpers.visualization import histograma
from src.db.db_handler import DBHandler
from src.streamlit_app.components.filters import date_range_filter, element_filter

st.title("Análisis Exploratorio de Datos")

db = DBHandler()

fecha_inicial, fecha_final = date_range_filter()

def show_graficos():
    options = ["Histogramas", "Scatter Matrix", "Mapa Coroplético"]

    opcion = st.radio(
        options=options,
        label="Selecciona la visualización:"
    )

    if opcion == options[0]:
        graficar_histogramas()
    elif opcion == options[1]:
        graficar_scatter_matrix()
    elif opcion == options[2]:
        mapa_coropletico()

def graficar_histogramas():
    st.header("Histogramas")

    st.write("Selecciona el elemento:")
    elemento = element_filter()

    if elemento:
        columna = element_cols_map[elemento][0]
        data = db.get_estaciones_historico_rango(elemento, fecha_inicial, fecha_final)
        df = pd.DataFrame(data).merge(locations_df, on="idema", how="left").sort_values("fecha")

        if columna in df.columns:
            fig = histograma(
                df,
                title=f"Histograma de {label_maps[columna]}",
                col=columna,
                x_label=columna
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(f"La columna {columna} no está disponible en los datos.")

def graficar_scatter_matrix():
    st.header("Scatter Matrix")
    
    dfs = []
    element_vars = [v[0] for v in element_cols_map.values()]

    for element, var in element_cols_map.items():

        data = db.get_estaciones_historico_rango(element, fecha_inicial, fecha_final)
        df_var = pd.DataFrame(data)[['idema', 'fecha', var[0]]]
        dfs.append(df_var)
    
    df_merged_vars = reduce(
        lambda left, right: pd.merge(left, right, on=['idema', 'fecha'], how='outer'),
        dfs
    )
    df_merged = df_merged_vars.merge(locations_df, on="idema", how="left")

    if all(var in df_merged.columns for var in element_vars):
        fig_scatter = px.scatter_matrix(df_merged, dimensions=element_vars)
        fig_scatter.update_traces(marker=dict(color="purple", size=6, opacity=0.7))
        fig_scatter.update_layout(
            title="Scatter Matrix de Variables Meteorológicas",
            width=1300,
            height=1300
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.error("No se pueden visualizar todas las variables en el Scatter Matrix.")

def mapa_coropletico():
    st.header("Mapa Coroplético de la temperatura media por provincia")

    st.write("Selecciona el elemento:")
    elemento = element_filter()

    if elemento:
        data = db.get_estaciones_historico_rango(elemento, fecha_inicial, fecha_final)
        df = pd.DataFrame(data)
        avg_df = provincia_avg(df, elemento)

        cols = element_cols_map[elemento]
        mapa = spain_map()

        for col in cols:
            add_to_map(mapa, avg_df, col, label_maps[col], color_maps[col])

        folium.LayerControl().add_to(mapa)
        folium_static(mapa)

show_graficos()