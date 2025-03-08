import joblib
import os
import pandas as pd
import streamlit as st
from helpers import api
from helpers.lookups import prov_names, provincia_lookup, estacion_lookup, estaciones
from ml.scripts.graphs import plot_forecast
from ml.scripts.create_sequence import create_sequences
from src.streamlit_app.components.filters import date_range_filter
from ml.scripts import clean, impute, scale
from helpers.config import script_dir
from keras.api.models import load_model


model_path = os.path.join(script_dir, '../ml/models')
scaler_path = os.path.join(script_dir, '../ml/scalers')

if "ml_first_run" not in st.session_state:
    st.session_state.ml_first_run = True

columns = ['fecha', 'idema', 'tmed', 'prec', 'tmin', 'tmax', 'hr_max','hr_media']

@st.cache_resource
def load_models():
    return load_model(os.path.join(model_path, 'gru.keras'))

@st.cache_resource
def load_scalers():
    _scaler_X = joblib.load(os.path.join(scaler_path, 'scaler_X_train.joblib'))
    _scaler_y = joblib.load(os.path.join(scaler_path, 'scaler_y_train.joblib'))

    return _scaler_X, _scaler_y

gru = load_models()
scaler_X, scaler_y = load_scalers()

models = ["GRU"]
model_map = {
    "GRU": gru
}

def prepare_data():
    df_scaled = scale.scale_df(df, scaler_X, scaler_y)
    target = 'tmed'

    X = df_scaled.drop(columns=[target])
    y = df_scaled[target]

    return create_sequences(X, y, df_scaled.index)

def make_prediction():
    model = model_map[selected_model]

    X_seq, y_seq, dates_seq = prepare_data()

    y_pred = model.predict(X_seq)
    y_pred_inverse = scaler_y.inverse_transform(y_pred.reshape(-1, 1)).flatten()

    future_dates = pd.date_range(start=df.index[-1], periods=len(y_pred_inverse) + 1, freq='D')[1:]

    predict_start = future_dates[0]

    fig = plot_forecast(df.index, df['tmed'], future_dates, y_pred_inverse, predict_start)

    st.plotly_chart(fig)


with st.sidebar:
    selected_model = st.selectbox("Selecciona un modelo:", models)

    fecha_inicial, fecha_final = date_range_filter('gráficos')
    provincia = st.selectbox("Selecciona la provincia", prov_names[1:])
    prov_id = provincia_lookup[provincia]

    filtered_idemas = [idema for idema, value in estaciones.items() if str(value['provincia_id']) == str(prov_id)]
    est_names = [estaciones[idema]['nombre'] for idema in filtered_idemas]
    estacion = st.selectbox("Selecciona la estación", est_names)
    idema = [estacion_lookup[estacion]]


    if st.button("Aplicar") or st.session_state.first_run:
        st.session_state.first_run = False

        with st.spinner("Cargando datos..."):
            st.session_state.ml_data = api.get_historico(
                columns=columns,
                idemas=idema,
                fecha_ini=fecha_inicial,
                fecha_fin=fecha_final
            )

if 'ml_data' not in st.session_state:
    st.header("Aplique los filtros para cargar los datos.")
    st.stop()

data = st.session_state.ml_data

if len(data) == 0:
    st.error("No hay datos disponibles para el rango seleccionado.")
else:
    df = pd.DataFrame(data)
    df = clean.clean_df(df)
    df = impute.impute_knn(df)
    df.set_index('fecha', inplace=True)

    make_prediction()