import os
import pandas as pd
from helpers.config import script_dir
import streamlit.components.v1 as components


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

    tab_metrics = pd.read_csv(os.path.join(script_dir, f"../data/model_res/metrics/{model}.csv"))
    tab.write(tab_metrics)

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
