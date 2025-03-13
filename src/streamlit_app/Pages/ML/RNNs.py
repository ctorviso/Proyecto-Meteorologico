import os
import pandas as pd
import streamlit as st

from helpers.config import script_dir
import streamlit.components.v1 as components

@st.cache_data
def load_resources(model):
    metrics = pd.read_csv(os.path.join(script_dir, f"../data/model_res/metrics/{model}.csv"))

    error_hist_fig_tab = open(os.path.join(script_dir, f"../data/model_res/differences/{model}.html"), "r",
                              encoding='utf-8').read()

    daily_stats_fig_tab = open(os.path.join(script_dir, f"../data/model_res/daily_stats/figures/{model}.html"), "r",
                               encoding='utf-8').read()

    
    if model == "prophet":
        forecast_fig = open(os.path.join(script_dir, "../data/model_res/daily_stats/figures/prophet_forecast.html"),
                            "r", encoding='utf-8').read()

        return metrics, forecast_fig, error_hist_fig_tab, daily_stats_fig_tab
    
    else:
        history_fig_tab = open(os.path.join(script_dir, f"../data/model_res/history/figures/{model}.html"), "r",
                               encoding='utf-8').read()
        history_scaled_fig_tab = open(
            os.path.join(script_dir, f"../data/model_res/history/figures/{model}_scaled.html"),
            "r", encoding='utf-8').read()

        return metrics, history_fig_tab, history_scaled_fig_tab, error_hist_fig_tab, daily_stats_fig_tab

metrics_gru, history_fig_gru, history_scaled_fig_gru, error_hist_fig_gru, daily_stats_fig_gru = load_resources("gru")
metrics_lstm, history_fig_lstm, history_scaled_fig_lstm, error_hist_fig_lstm, daily_stats_fig_lstm = load_resources("lstm")
metrics_simplernn, history_fig_simplernn, history_scaled_fig_simplernn, error_hist_fig_simplernn, daily_stats_fig_simplernn = load_resources("simplernn")
metrics_prophet, forecast_fig_prophet, error_hist_fig_prophet, daily_stats_fig_prophet = load_resources("prophet")

model_resources = {
    "gru": {
        'metrics': metrics_gru,
        'history': history_fig_gru,
        'history_scaled': history_scaled_fig_gru,
        'error_hist': error_hist_fig_gru,
        'daily_stats': daily_stats_fig_gru
    },
    "lstm": {
        'metrics': metrics_lstm,
        'history': history_fig_lstm,
        'history_scaled': history_scaled_fig_lstm,
        'error_hist': error_hist_fig_lstm,
        'daily_stats': daily_stats_fig_lstm
    },
    "simplernn": {
        'metrics': metrics_simplernn,
        'history': history_fig_simplernn,
        'history_scaled': history_scaled_fig_simplernn,
        'error_hist': error_hist_fig_simplernn,
        'daily_stats': daily_stats_fig_simplernn
    },
    "prophet": {
        'metrics': metrics_prophet,
        'error_hist': error_hist_fig_prophet,
        'daily_stats': daily_stats_fig_prophet,
        'forecast': forecast_fig_prophet
    }
}

def show(tab, model):

    if model != "prophet":
        tab.markdown(
            """ ##### Para la implementación de este modelo, se ha utilizado la librería de Keras. A continuación, se muestra un resumen de los resultados obtenidos.""")

        tab.markdown("""---""")

    else:
        tab.markdown(
            """ ##### Para la implementación de este modelo, se ha utilizado la librería de Facebook Prophet. A continuación, se muestra un resumen de los resultados obtenidos.""")

        tab.markdown("""---""")

    tab.markdown(""" 
    * **MSE**: Error Cuadrático Medio. Mide la media de los errores al cuadrado, es decir, cuánto se desvían las predicciones de los valores reales en promedio, elevando esas diferencias al cuadrado. Cuanto más bajo es el MSE, mejor es el ajuste del modelo.
    * **MAE**: Error Absoluto Medio. Mide el promedio de la magnitud de los errores, es decir, la diferencia promedio absoluta entre las predicciones y los valores reales. Cuanto más bajo es el MAE, más cerca están las predicciones de los valores reales.
    * **RMSE**: Raíz del Error Cuadrático Medio. Es la raíz cuadrada del MSE y se interpreta de la misma manera. Devuelve el error en la misma escala que los datos originales y, como el MSE, penaliza más los errores grandes.
    * **R2**: Coeficiente de Determinación. Indica qué proporción de la variabilidad de los datos está explicada por el modelo. El R2 está entre 0 y 1. Un valor de 1 significa una predicción perfecta, mientras que un valor de 0 significa que el modelo no consigue capturar bien la relación entre las variables.
                 """)
    
    tab.markdown(f"""En la siguiente tabla se muestran las métricas del modelo {model}:""")

    tab.write(model_resources[model]['metrics'])

    if model == "gru":
        tab.markdown("Este modelo muestra un MSE bajo y un RMSE también bajo, indicando que, de media, se equivoca poco a la hora de predecir. Con un R2 de 0.689, el modelo GRU explica cerca del 69% de la variabilidad de los datos, lo que indica un buen ajuste.")
    elif model == "lstm":
        tab.markdown("Tiene resultados muy similares a GRU, con un MSE y RMSE bajos y un R2 ligeramente superiro (0.694), lo que nos sugiere que el modelo se ajusta ligeramente mejor a los datos.")
    elif model == "prophet":
        tab.markdown("Aunque presenta un MSE relativamente alto (y más alto que en el resto de los modelos que estamos estudiando), el MAE es el más bajo (0.0314), lo que sugiere que la mayoría de las predicciones están bastante cerca de los valores reales, pero algunos errores grandes provocan que se eleve el MSE y RMSE. Su R2 está por debajo de los modelos de redes neuronales (0.5912), aunque sigue explicando más de la mitad de la variabilidad de los datos.")
    elif model == "simplernn":
        tab.markdown("Muestra un MSE (0.00528) y un RMSE (0.07268), algo más altos que GRU y LSTM, y su R2 (0.6705) es ligeramente inferior. Aún así, sigue siendo un modelo aceptable, pero con menos capacidad para capturar patrones complejos que GRU y LSTM.")

    tab.markdown("""---""")

    tab.markdown(
        f"""
        ### Análisis de Residuos
        En la siguiente imagen se muestra un análisis de comparación entre los valores reales y los valores predichos por el modelo {model}:
        """
    )

    st.components.v1.html(
        f"""
        <div style="width: 100%; height: 520px; overflow: hidden;">
            <div style="width: 125%; height: 125%; overflow: hidden; transform: scale(0.8); transform-origin: 0 0;">
                {model_resources[model]['daily_stats']}
            </div>
        </div>
        """,
        height=520
    )

    tab.markdown("""---""")

    tab.markdown(
        f"""
        ### Histograma de Error
        En la siguiente imagen se muestra el histograma de los errores residuales del modelo {model}:
        """
    )

    components.html(model_resources[model]['error_hist'], height=500)

    tab.markdown("""---""")

    if model != "prophet":

        tab.markdown(
            f"""
            ### Historial de Entrenamiento
            En la siguiente imagen se muestra el historial de las métricas durante el entrenamiento del modelo {model}:
            """
        )

        components.html(model_resources[model]['history'], height=1200)
        components.html(model_resources[model]['history_scaled'], height=600)

    if model == "prophet":

        tab.markdown(
            """
            ### Forecast
            En la siguiente imagen se muestra el pronóstico de la serie temporal utilizando el modelo Prophet:
        
            """
        )

        components.html(model_resources[model]['forecast'], height=600)
