from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
from sklearn.preprocessing import MinMaxScaler

from helpers import api
from helpers.lookups import element_cols_map_numeric, label_maps, histogram_color_maps, numeric_cols, scatter_cols, \
    scatter_color_maps, provincia_lookup, prov_names, offset_map, provincias, estaciones, estacion_lookup, \
    estaciones_df
from helpers.preprocessing import convert_numeric, log_transform_df
from helpers.visualization import histograms, scatter_matrix, time_series, bar_plots
from src.streamlit_app.components.tabs import element_tabs

if "graficos_first_run" not in st.session_state:
    st.session_state.graficos_first_run = True

st.title(":chart_with_upwards_trend: Análisis Exploratorio de Datos")

element_tabs()
selected_element = st.session_state.selected_element


def show_graphs():
    col1, col2 = st.columns(2)
    height = 560

    with col1:
        with st.container(border=True, height=height):
            show_daily_average()

    with col2:
        with st.container(border=True, height=height):
            show_histogram_locations()

    st.markdown("<div style='margin: 10px'></div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        with st.container(border=True, height=height):
            show_histograms()

    with col4:
        with st.container(border=True, height=height):
            show_scatter_matrix()

def show_histograms():

    columns = element_cols_map_numeric[selected_element]

    if st.checkbox("Logaritmo", key=f"{selected_element}_log_histogram"):
        selected_df = avg_df_log
    else:
        selected_df = avg_df

    colors = [histogram_color_maps[col] for col in columns]

    hist = histograms(
        selected_df,
        title=f"Histograma",
        cols=element_cols_map_numeric[selected_element],
        x_label=selected_element,
        colors=colors
    )
    st.plotly_chart(hist, use_container_width=True)


def show_scatter_matrix():
    x_cols = element_cols_map_numeric[selected_element]

    compare_var_label = st.selectbox(
        "Seleccionar elemento para comparar con " + selected_element,
        options=[label_maps[col] for col in scatter_cols if col != selected_element],
        key=f"{selected_element}_compare_var"
    )

    compare_var = [col for col in scatter_cols if label_maps[col] == compare_var_label][0]

    y_cols = [compare_var]

    x_col_labels = [label_maps[col] for col in x_cols]
    y_col_labels = [label_maps[col] for col in y_cols]

    fig = scatter_matrix(
        avg_df,
        title=f"Correlación entre {selected_element} y {label_maps[compare_var]}",
        x_cols=x_cols,
        y_cols=y_cols,
        x_labels=x_col_labels,
        y_labels=y_col_labels,
        color=scatter_color_maps[selected_element],
        trendline=True
    )

    st.plotly_chart(fig, use_container_width=True)

def show_daily_average():

    if st.checkbox("MinMax", key=f"{selected_element}_minmax"):
        scaler = MinMaxScaler()
        daily_avg[numeric_cols] = scaler.fit_transform(daily_avg[numeric_cols])

    columns = element_cols_map_numeric[selected_element]
    df_element = daily_avg[columns]

    fig = time_series(
        df_element,
        title=f"Promedio diario",
        cols=columns,
        colors=[histogram_color_maps[col] for col in columns],
        x_label="Fecha",
        y_label=selected_element
    )

    st.plotly_chart(fig, use_container_width=True)

def show_histogram_locations():

    cols = element_cols_map_numeric[selected_element]

    if prov_id == "0":
        avg_df['provincia'] = avg_df['provincia_id'].apply(lambda x: provincias[x]['nombre'])
        sorted_data = avg_df.groupby('provincia')[cols].mean().sort_values(by=cols[0])
    else:
        avg_df['estacion'] = avg_df['idema'].apply(lambda x: estaciones[x]['nombre'])
        sorted_data = avg_df.groupby('estacion')[cols].mean().sort_values(by=cols[0])

    if st.checkbox("MinMax", key=f"{selected_element}_minmax_provincias"):
        scaler = MinMaxScaler()
        sorted_data[cols] = scaler.fit_transform(sorted_data[cols])

    fig = bar_plots(
        sorted_data,
        title=f"Promedio por provincia" if prov_id == "0" else f"Promedio por estación",
        cols=cols,
        x_label="Provincia",
        y_label="Valor promedio",
        label_maps=label_maps,
        colors=[histogram_color_maps[col] for col in cols]
    )

    st.plotly_chart(fig, use_container_width=True)

data = None

with st.sidebar:
    provincia = st.selectbox("Selecciona la provincia", prov_names)
    prov_id = provincia_lookup[provincia]
    if 'prov_id' not in st.session_state:
        st.session_state.prov_id = prov_id

    filtered_idemas = [idema for idema, value in estaciones.items() if str(value['provincia_id']) == str(prov_id)]
    est_names = ['Todas'] + [estaciones[idema]['nombre'] for idema in filtered_idemas]
    estacion = st.selectbox("Selecciona la estación meteorológica", est_names)
    if estacion != 'Todas':
        idema = estacion_lookup[estacion]

    if prov_id != st.session_state.prov_id or st.session_state.graficos_first_run or 'graficos_df' not in st.session_state:
        st.session_state.graficos_first_run = False
        st.session_state.prov_id = prov_id

        with st.spinner("Cargando datos..."):
            if prov_id != "0":
                _data = api.get_historico(
                    columns=['fecha', 'idema', 'tmed', 'tmax', 'tmin', 'prec', 'hr_max','hr_media', 'hr_min', 'sol', 'pres_max', 'pres_min', 'velmedia', 'racha'],
                    fecha_ini=(datetime.now() - timedelta(days=offset_map[list(offset_map.keys())[-3]])).strftime('%Y-%m-%d'),
                    fecha_fin=datetime.now().strftime('%Y-%m-%d'),
                    idemas=filtered_idemas
                )

            else:
                _data = api.get_historico_average(
                    fecha_ini=(datetime.now() - timedelta(days=offset_map[list(offset_map.keys())[-3]])).strftime('%Y-%m-%d'),
                    fecha_fin=datetime.now().strftime('%Y-%m-%d')
                )

            _df = pd.DataFrame(_data)
            _df['fecha'] = pd.to_datetime(_df['fecha'], errors='coerce')
            _df = _df.sort_values('fecha')
            _df = _df.set_index('fecha')
            st.session_state.graficos_df = _df

if "rango_historico" not in st.session_state:
    st.session_state.rango_historico = list(offset_map.keys())[0]

rango_historico = st.pills(
    options=list(offset_map.keys())[:-2],
    label='Rango de la predicción:',
    key="rango",
    default=st.session_state.rango_historico,
    on_change=lambda: st.session_state.update({"rango_historico": st.session_state.rango})
)

if rango_historico is None:
    st.stop()

if 'graficos_df' not in st.session_state:
    st.header("Aplique los filtros para cargar los datos.")
    st.stop()

df = st.session_state.graficos_df
fecha_inicial = df.index.max() - timedelta(days=offset_map[rango_historico])
df = df[df.index >= fecha_inicial]

if len(df) == 0 or df is None:
    st.error("No hay datos disponibles para el rango seleccionado.")
else:
    avg_df = df.copy(deep=True)
    if prov_id != "0":
        avg_df = pd.merge(avg_df, estaciones_df[['idema', 'provincia_id']], on='idema', how='left')
        avg_df = avg_df.drop(columns=['provincia_id'])
        avg_df = convert_numeric(avg_df, numeric_cols)
        if estacion != 'Todas':
            avg_df = avg_df[avg_df['idema'] == idema]
        daily_avg = avg_df.drop(columns=["idema"]).groupby(avg_df.index).mean().reset_index()
        daily_avg = daily_avg.interpolate(method='linear')
    else:
        avg_df = avg_df.drop(columns=['extracted'])
        avg_df['provincia_id'] = avg_df['provincia_id'].astype(str)
        avg_df = convert_numeric(avg_df, numeric_cols)
        avg_df = avg_df[avg_df['provincia_id'] == prov_id] if prov_id != "0" else avg_df
        daily_avg = avg_df.drop(columns=["provincia_id"]).groupby(avg_df.index).mean()


    avg_df_log = avg_df.copy(deep=True)
    avg_df_log = log_transform_df(avg_df_log, numeric_cols)

    show_graphs()
