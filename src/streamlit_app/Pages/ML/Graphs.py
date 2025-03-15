import streamlit as st
import streamlit.components.v1 as components
from sklearn.preprocessing import MinMaxScaler
from ml.scripts import graphs
import pandas as pd
import os
from helpers.config import script_dir

model_name_map = {
    "gru": "GRU",
    "lstm": "LSTM",
    "simplernn": "SimpleRNN",
    "prophet": "Prophet"
}

@st.cache_data
def load_resources(model_id):
    differences_img = open(os.path.join(script_dir, f"../data/model_res/differences/{model_id}.png"), "rb").read()
    daily_stats_df = pd.read_csv(os.path.join(script_dir, f"../data/model_res/daily_stats/{model_id}.csv"))
    daily_stats_fig = graphs.daily_stats_comparison(model_name_map[model_id], daily_stats_df).to_html()

    if model_id == "prophet":
        forecast_img = open(os.path.join(script_dir, f"../data/model_res/daily_stats/prophet_forecast.png"),"rb").read()

        return differences_img, daily_stats_fig, forecast_img

    else:
        scaler = MinMaxScaler()

        training_history_df = pd.read_csv(os.path.join(script_dir, f"../data/model_res/training_history/{model_id}.csv"))
        training_history_scaled_df = pd.DataFrame(scaler.fit_transform(training_history_df), columns=training_history_df.columns)

        training_history_fig = graphs.training_history(model_name_map[model_id], training_history_df).to_html()
        training_history_scaled_fig = graphs.training_history_scaled(model_name_map[model_id], training_history_scaled_df, training_history_df).to_html()

        return differences_img, daily_stats_fig, training_history_fig, training_history_scaled_fig


metrics_df = pd.read_csv(os.path.join(script_dir, f"../data/model_res/metrics.csv"))

differences_img_gru, daily_stats_fig_gru, training_history_fig_gru, training_history_scaled_fig_gru = load_resources("gru")
differences_img_lstm, daily_stats_fig_lstm, training_history_fig_lstm, training_history_scaled_fig_lstm = load_resources("lstm")
differences_img_simplernn, daily_stats_fig_simplernn, training_history_fig_simplernn, training_history_scaled_fig_simplernn = load_resources("simplernn")
differences_img_prophet, daily_stats_fig_prophet, forecast_img_prophet = load_resources("prophet")

model_resources = {
    "gru": {
        'differences': differences_img_gru,
        'daily_stats': daily_stats_fig_gru,
        'training_history': training_history_fig_gru,
        'training_history_scaled': training_history_scaled_fig_gru
    },
    "lstm": {
        'differences': differences_img_lstm,
        'daily_stats': daily_stats_fig_lstm,
        'training_history': training_history_fig_lstm,
        'training_history_scaled': training_history_scaled_fig_lstm
    },
    "simplernn": {
        'differences': differences_img_simplernn,
        'daily_stats': daily_stats_fig_simplernn,
        'training_history': training_history_fig_simplernn,
        'training_history_scaled': training_history_scaled_fig_simplernn
    },
    "prophet": {
        'differences': differences_img_prophet,
        'daily_stats': daily_stats_fig_prophet,
        'forecast': forecast_img_prophet
    }
}

def show_graphs(tab, model_id):

    tab.markdown("### Prediccion Media Diaria")

    components.html(f"""
    <div style="width: 100%; height: 520px; overflow: hidden;">
        <div style="width: 125%; height: 125%; overflow: hidden; transform: scale(0.8); transform-origin: 0 0;">
            {model_resources[model_id]['daily_stats']}
        </div>
    </div>""", height=520)

    tab.markdown("""---""")
    tab.markdown("### Histograma de Error")
    tab.image(model_resources[model_id]['differences'], use_container_width=True)

    st.markdown("---")
    if model_id != "prophet":
        st.markdown("### Historial de Entrenamiento")
        # noinspection PyUnboundLocalVariable
        components.html(model_resources[model_id]['training_history'], height=1200)

        st.markdown("### Historial de Entrenamiento Escalado")
        # noinspection PyUnboundLocalVariable
        components.html(model_resources[model_id]['training_history_scaled'], height=600)

    if model_id == "prophet":
        st.markdown("### Forecast")
        # noinspection PyUnboundLocalVariable
        st.image(model_resources[model_id]['forecast'], use_container_width=True)
