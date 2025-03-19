import io
import os
from datetime import datetime, timedelta

import joblib
import pandas as pd
import requests
import streamlit as st
from keras.api.models import load_model

from helpers import api
from helpers.config import script_dir
from helpers.lookups import prov_names, provincia_lookup, estacion_lookup, estaciones, offset_map, estaciones_df
from ml.scripts import clean, impute, scale
from ml.scripts.create_sequence import create_sequences
from ml.scripts.graphs import plot_forecast

model_path = os.path.join(script_dir, '../ml/models')
scaler_path = os.path.join(script_dir, '../ml/scalers')

if "ml_first_run" not in st.session_state:
    st.session_state.ml_first_run = True

st.title(":brain: Predicciones ML")

cols = st.columns(2)

with cols[0]:
    provincia = st.selectbox("Selecciona la provincia", prov_names[1:], index=14)
    prov_id = provincia_lookup[provincia]
    if 'prov_id' not in st.session_state:
        st.session_state.prov_id = prov_id

with cols[1]:
    filtered_idemas = [idema for idema, value in estaciones.items() if str(value['provincia_id']) == str(prov_id)]
    est_names = ['Todas'] + [estaciones[idema]['nombre'] for idema in filtered_idemas]
    estacion = st.selectbox("Selecciona la estación meteorológica", est_names)
    if estacion != 'Todas':
        idema = estacion_lookup[estacion]
    
if prov_id != st.session_state.prov_id or st.session_state.ml_first_run or 'ml_df' not in st.session_state:
    st.session_state.ml_first_run = False
    st.session_state.prov_id = prov_id
    
    with st.spinner("Cargando datos..."):
        _ml_data = api.get_historico(
            columns=['fecha', 'idema', 'tmed', 'prec', 'tmin', 'tmax', 'hr_max','hr_media'],
            fecha_ini=(datetime.now() - timedelta(days=offset_map[list(offset_map.keys())[-3]])).strftime('%Y-%m-%d'),
            fecha_fin=datetime.now().strftime('%Y-%m-%d'),
            idemas=filtered_idemas
        )

        _df = pd.DataFrame(_ml_data)
        _df = _df.sort_values('fecha')
        idemas = _df['idema']
        _df = clean.clean_df(_df)
        _df = impute.impute_knn(_df)
        _df['idema'] = idemas

        st.session_state.ml_df = _df

    st.rerun()

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

df = st.session_state.ml_df

if len(df) == 0 or df is None:
    st.error("No hay datos disponibles para el rango seleccionado.")
    st.stop()

start_date = df['fecha'].max() - timedelta(days=offset_map[rango_historico])
end_date = df['fecha'].max() + timedelta(days=offset_map[rango_historico]-1)

if estacion != 'Todas':
    df = df[df['idema'] == idema]
    df = df.drop(columns=['idema'])
else:
    df = pd.merge(df, estaciones_df[['idema', 'provincia_id']], on='idema', how='left')
    df = df.drop(columns=['idema'])
    df = df.groupby(['fecha', 'provincia_id']).mean().reset_index()
    df = df.drop(columns=['provincia_id'])

@st.cache_resource
def load_gru():
    return load_model(os.path.join(model_path, 'gru.keras'))

@st.cache_resource
def load_simple_rnn():
    return load_model(os.path.join(model_path, 'simplernn.keras'))

@st.cache_resource
def load_lstm():
    return load_model(os.path.join(model_path, 'lstm.keras'))

@st.cache_resource
def load_prophet():
    url = "https://rednvrsdcuwtwyfxtjru.supabase.co/storage/v1/object/public/ml//prophet.pkl"

    try:
        response = requests.get(url, timeout=20)

        if response.status_code == 200:
            try:
                model = joblib.load(io.BytesIO(response.content))
                return model
            except Exception as e:
                st.error(f"Error al cargar el modelo Prophet: {str(e)}")
        else:
            st.error(f"Error al descargar el modelo Prophet: {response.status_code}")

    except Exception as e:
        st.error(f"Error al descargar el modelo Prophet: {str(e)}")

    return None


@st.cache_resource
def load_scalers():
    _scaler_X = joblib.load(os.path.join(scaler_path, 'scaler_X_full.joblib'))
    _scaler_y = joblib.load(os.path.join(scaler_path, 'scaler_y_full.joblib'))

    return _scaler_X, _scaler_y

gru = load_gru()
simple_rnn = load_simple_rnn()
lstm = load_lstm()
prophet = load_prophet()

scaler_X, scaler_y = load_scalers()


def predict_keras(model):
    df_scaled = df.copy()

    df_scaled = df_scaled.set_index('fecha')
    df_scaled = scale.scale_df(df_scaled, scaler_X, scaler_y)

    target = 'tmed'

    X = df_scaled.drop(columns=[target])
    y = df_scaled[target]

    X_seq, y_seq, dates_seq = create_sequences(X, y, df_scaled.index)

    y_pred = model.predict(X_seq)
    y_pred_inverse = scaler_y.inverse_transform(y_pred).flatten()

    last_date = df_scaled.index[-1]
    future_dates = [last_date + pd.Timedelta(days=i+1) for i in range(len(y_pred_inverse))]

    return pd.DataFrame({
        'fecha': future_dates,
        'tmed': y_pred_inverse
    })


def predict_prophet():
    days_ahead = offset_map[rango_historico]
    last_historical_date = df['fecha'].max()

    future_dates = pd.date_range(
        start=last_historical_date + pd.Timedelta(days=1),
        periods=days_ahead,
        freq='D'
    )

    future = pd.DataFrame({'ds': future_dates})

    forecast = prophet.predict(future)

    return pd.DataFrame({
        'fecha': forecast['ds'],
        'tmed': forecast['yhat']
    })


def make_prediction():
    df_gru = predict_keras(gru)
    df_lstm = predict_keras(lstm)
    df_simple_rnn = predict_keras(simple_rnn)
    df_prop = predict_prophet()
    df_hist = pd.DataFrame({
        'fecha': df['fecha'],
        'tmed': df['tmed']
    })

    # add the last date from hist onto start of gru and prop
    df_gru = pd.concat([df_hist.tail(1), df_gru])
    df_lstm = pd.concat([df_hist.tail(1), df_lstm])
    df_simple_rnn = pd.concat([df_hist.tail(1), df_simple_rnn])
    df_prop = pd.concat([df_hist.tail(1), df_prop])

    result = df_hist.rename(columns={'tmed': 'historical_tmed'})

    result = pd.merge(
        result,
        df_gru.rename(columns={'tmed': 'gru_tmed'}),
        on='fecha',
        how='outer'
    )

    result = pd.merge(
        result,
        df_lstm.rename(columns={'tmed': 'lstm_tmed'}),
        on='fecha',
        how='outer'
    )

    result = pd.merge(
        result,
        df_simple_rnn.rename(columns={'tmed': 'simple_rnn_tmed'}),
        on='fecha',
        how='outer'
    )

    result = pd.merge(
        result,
        df_prop.rename(columns={'tmed': 'prop_tmed'}),
        on='fecha',
        how='outer'
    )

    result = result.sort_values('fecha')

    predict_start = df['fecha'].values[-1]

    fig = plot_forecast(result, predict_start, start_date, end_date)

    st.plotly_chart(fig)


if df['tmed'].isna().mean() >= 0.5:
    st.error("No hay suficientes datos disponibles para el rango seleccionado.")
    st.stop()

make_prediction()