from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
from helpers import api
from helpers.lookups import element_cols_map_numeric, label_maps, choropleth_color_maps, provincias, \
    histogram_color_maps, offset_map, elements, provincias_df
from helpers.lookups import numeric_cols
from helpers.geojson import inject_col_values, get_geodata_provincias
from helpers.preprocessing import convert_numeric
from helpers.visualization import bar_plots, choropleth_map
from src.streamlit_app.Pages.EDA.Graficos import selected_element

if "mapa_first_run" not in st.session_state:
    st.session_state.mapa_first_run = True

st.title(":world_map: Mapa Coroplético")

with st.sidebar:
    selected_element = st.selectbox(options=[element.capitalize() for element in elements], label='Elemento')
    selected_element = selected_element.lower()
    variables = element_cols_map_numeric[selected_element]
    if len(variables) > 1:
        selected_column = st.radio(options=variables, label='Variable')
    else:
        selected_column = variables[0]

    st.session_state.selected_element = selected_element

if st.session_state.mapa_first_run or 'df' not in st.session_state:
    st.session_state.mapa_first_run = False

    with st.spinner("Cargando datos..."):
        st.session_state.mapa_data = api.get_historico_average(
            fecha_ini=(datetime.now() - timedelta(days=offset_map[list(offset_map.keys())[-3]])).strftime('%Y-%m-%d'),
            fecha_fin=datetime.now().strftime('%Y-%m-%d')
        )

    _df = pd.DataFrame(st.session_state.mapa_data).drop(columns=["extracted"])
    _df = convert_numeric(_df, numeric_cols)
    _df = _df[_df['provincia_id'] != '0']
    _df = _df.apply(lambda x: pd.to_numeric(x, errors='coerce') if x.name != 'fecha' else x)

    st.session_state.df = _df
    st.rerun()


rango_historico = st.pills(options=dict(list(offset_map.items())[:-2]), label='Rango histórico:', key="rango", default=list(offset_map.keys())[0])
if rango_historico is None:
    st.stop()

avg_df = st.session_state.df if 'df' in st.session_state else None

if avg_df is None:
    st.stop()

fecha_inicial = (datetime.now() - timedelta(days=offset_map[rango_historico]))
avg_df['fecha'] = pd.to_datetime(avg_df['fecha'], errors='coerce')
avg_df = avg_df[avg_df['fecha'] >= fecha_inicial]

avg_df = avg_df.groupby('provincia_id').mean().reset_index().drop(columns=['fecha'])
avg_df['provincia_id'] = avg_df['provincia_id'].astype(str)
avg_df['provincia'] = pd.merge(avg_df, provincias_df[['provincia', 'provincia_id']], on='provincia_id', how='left')['provincia']



geojson = get_geodata_provincias()
geojson['features'] = [f for f in geojson['features'] if f['properties']['provincia_id'] not in ['35', '38']]

if geojson is None or avg_df is None or len(st.session_state.mapa_data) == 0:
    st.error("No hay datos disponibles para el rango seleccionado.")
    st.stop()

for element in element_cols_map_numeric.keys():
    inject_col_values(geojson, avg_df, element_cols_map_numeric[element])

def show_choropleth_map():

    fig = choropleth_map(
        avg_df,
        selected_column,
        geojson,
        label_maps,
        choropleth_color_maps
    )

    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': False,
        'scrollZoom': False,

    })

if st.session_state.selected_element:
    show_choropleth_map()
