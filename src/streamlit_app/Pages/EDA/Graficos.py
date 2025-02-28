from functools import reduce
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_folium import folium_static
from helpers.lookups import locations_df, element_cols_map_numeric, label_maps, color_maps
from helpers.maps.folium import spain_map, create_tooltip, get_column_choropleth
from helpers.maps.geojson import inject_col_values
from helpers.preprocessing import provincia_avg, convert_numeric
from helpers.visualization import histograma
from helpers import api
from src.streamlit_app.components.filters import date_range_filter, element_filter

st.title("Análisis Exploratorio de Datos")

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
        data = api.get_estaciones_historico_rango(elemento, fecha_inicial, fecha_final)
        if not data:
            st.error("No hay datos disponibles para el rango seleccionado.")
            return

        df = pd.DataFrame(data).merge(locations_df, on="idema", how="left").sort_values("fecha")
        df = convert_numeric(df, element_cols_map_numeric[elemento])
        for columna in element_cols_map_numeric[elemento]:
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
    scatter_elements = ['temperatura', 'lluvia', 'viento', 'humedad']

    data = api.get_estaciones_historico_rango(elemento=','.join(scatter_elements), fecha_ini=fecha_inicial, fecha_fin=fecha_final)

    if not data:
        st.error("No hay datos disponibles para el rango seleccionado.")
        return

    cols = [cols[0] for element, cols in element_cols_map_numeric.items() if element in scatter_elements]
    for col in cols:
        df_var = pd.DataFrame(data)[['idema', 'fecha', col]]
        dfs.append(df_var)
    
    df_merged_vars = reduce(
        lambda left, right: pd.merge(left, right, on=['idema', 'fecha'], how='outer'),
        dfs
    )
    df_merged = df_merged_vars.merge(locations_df, on="idema", how="left")

    if all(var in df_merged.columns for var in cols):
        fig_scatter = px.scatter_matrix(df_merged, dimensions=cols)
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
    st.header(f"Mapa Coroplético")

    st.write("Selecciona el elemento:")
    elemento = element_filter()

    if elemento:
        st.write(f"Mapa Coroplético de {elemento} por provincia")

        data = api.get_estaciones_historico_rango(elemento, fecha_inicial, fecha_final)
        df = pd.DataFrame(data)
        avg_df = provincia_avg(df, elemento)

        geojson = inject_col_values(avg_df, element_cols_map_numeric[elemento])

        maps = {}

        for col in element_cols_map_numeric[elemento]:
            maps[col] = spain_map()
            choro = get_column_choropleth(geojson, avg_df, col, label_maps[col], color_maps[col]).add_to(maps[col])
            create_tooltip(col, label_maps[col]).add_to(choro.geojson)

        selected_map = st.radio("Selecciona el variable:", list(maps.keys()))
        folium_static(maps[selected_map])

show_graficos()