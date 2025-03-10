import os
import pandas as pd
from helpers.config import script_dir
import streamlit.components.v1 as components


def show(tab, model):

    if model != "prophet":
        tab.markdown(
            """ ##### Para la implementación de este modelo, se ha utilizado la librería de Keras. A continuación, se muestra un resumen de los resultados obtenidos""")

        tab.markdown("""---""")

    else:
        tab.markdown(
            """ ##### Para la implementación de este modelo, se ha utilizado la librería de Facebook Prophet. A continuación, se muestra un resumen de los resultados obtenidos""")

        tab.markdown("""---""")

    tab_metrics = pd.read_csv(os.path.join(script_dir, f"../data/model_res/metrics/{model}.csv"))
    tab.write(tab_metrics)

    tab.markdown("""---""")

    tab.markdown(
        f"""
        ### Análisis de Residuos
        En la siguiente imagen se muestra un análisis de comparación entre los valores reales y los valores predichos por el modelo {model}:
        """
    )

    daily_stats_fig_tab = open(os.path.join(script_dir, f"../data/model_res/daily_stats/figures/{model}.html"), "r").read()
    components.html(daily_stats_fig_tab, height=650)

    tab.markdown("""---""")

    tab.markdown(
        f"""
        ### Histograma de Error
        En la siguiente imagen se muestra el histograma de los errores residuales del modelo {model}:
        """
    )

    error_hist_fig_tab = open(os.path.join(script_dir, f"../data/model_res/differences/{model}.html"), "r").read()
    components.html(error_hist_fig_tab, height=650, width=1200)

    tab.markdown("""---""")

    if model != "prophet":

        tab.markdown(
            f"""
            ### Historial de Entrenamiento
            En la siguiente imagen se muestra el historial de las métricas durante el entrenamiento del modelo {model}:
            """
        )

        history_fig_tab = open(os.path.join(script_dir, f"../data/model_res/history/figures/{model}.html"), "r").read()
        components.html(history_fig_tab, height=1200)

        history_scaled_fig_tab = open(os.path.join(script_dir, f"../data/model_res/history/figures/{model}_scaled.html"),
                                      "r").read()

        components.html(history_scaled_fig_tab, height=600)

    if model == "prophet":

        tab.markdown(
            """
            ### Forecast
            En la siguiente imagen se muestra el pronóstico de la serie temporal utilizando el modelo Prophet:
        
            """
        )

        forecast_fig = open(os.path.join(script_dir, "../data/model_res/daily_stats/figures/prophet_forecast.html"),
                            "r").read()

        components.html(forecast_fig, height=800)
