from helpers.config import script_dir
import os
import pandas as pd
import streamlit as st
from src.streamlit_app.Pages.ML.Graphs import show_graphs

metrics_df = pd.read_csv(os.path.join(script_dir, "../data/model_res/metrics.csv"))

def intro():

    st.markdown("""
    ## :thermometer: Desarrollo de Modelos de Machine Learning para la Predicción de Temperatura Media Diaria para Estaciones Meteorológicas en España
    ###### Los conjuntos de datos finales pueden ser encontrados en la pestaña 'Datos ML'
    ---
    """)

    col1, col2 = st.columns(2)

    col1.markdown("""
    #### Variable Objetivo: 
    - tmed: Temperatura Media Diaria (ºC)
    #### Variables de Entrada:
    - tmin: Temperatura Mínima Diaria (ºC)
    - tmax: Temperatura Máxima Diaria (ºC)
    - prec: Precipitación Diaria (mm)
    - hr_media: Humedad Relativa Media Diaria (%)
    - hr_max: Humedad Relativa Máxima Diaria (%)
    - latitud: Latitud de la Estación (º)
    - altitud: Altitud de la Estación (m)
    - fecha: Fecha de la Observación
    """)

    col2.markdown("""
    #### Años Utilizados: 
    - Completo: 2010 - 2025
    - Train: 2010 - 2020
    - Validation: 2021 - 2022
    - Test: 2023 - 2025
    """)

    col2.markdown("""
    #### Modelos Utilizados:
    - SimpleRNN
    - Long Short-Term Memory (LSTM)
    - Gated Recurrent Unit (GRU)
    - Facebook Prophet
    """)

def pipeline():

    st.markdown("""
    ---
    ### Pipeline de Procesamiento de Datos
    ###### El siguiente esquema detalla el proceso de limpieza y preparación de los datos meteorológicos históricos para su uso en los modelos de predicción.
    ---
    #### 1. Proceso de Limpieza:
    - Concatenación de tablas de todos los años en un único conjunto de datos
    - Conversión de columnas de fecha y dirección del viento a representaciones de seno y coseno
    - Extracción de valores de año y normalización: 1950 → 0.0, 2050 → 1.0 (2000 = 0.5)
    - Fusión de metadatos de estaciones (IDEMA*, latitud, longitud, altitud)
    - Conversión de columnas numéricas a formatos apropiados
    - Redondeo de todos los valores a 4 decimales
    *IDEMA - Identificación Estación Meteorológica (AEMET Station ID)
    ---
    #### 2. Selección de Características:
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Correlación de todas las características")
        st.image(os.path.join(script_dir, "../data/model_res/feature_selection/corr1.png"))

    with col2:
        st.markdown("##### Correlación de las características seleccionadas")
        st.image(os.path.join(script_dir, "../data/model_res/feature_selection/corr2.png"))

    st.markdown("---")

    col1, col2, _ = st.columns(3)

    col1.markdown("##### Características Seleccionadas")
    col1.write(pd.read_csv(os.path.join(script_dir, "../data/model_res/feature_selection/cols_conservadas.csv")))

    col2.markdown("##### Características Eliminadas")
    col2.write(pd.read_csv(os.path.join(script_dir, "../data/model_res/feature_selection/cols_eliminadas.csv")))

    st.markdown("---")

    st.markdown("""
    #### 3. Búsqueda de Estación más Cercana:
    - Creación de un mapeo de cada estación a todas las demás estaciones en orden desde la más cercana a la más lejana
    - Distancia calculada utilizando latitud, longitud y altitud después de aplicar StandardScaler
    ---
    #### 4. Imputación por Estación más Cercana:
    - Imputación de todos los valores NaN utilizando la media de las 5 estaciones más cercanas para cada día
    - Este enfoque previene la filtración de datos entre conjuntos, ya que solo utiliza datos del mismo día
    - Columnas imputadas y sus porcentajes de valores faltantes:
    """)
    st.write(pd.read_csv(os.path.join(script_dir, "../data/model_res/feature_selection/nans.csv")))
    st.markdown("""
    ---
    #### 5. División Train-Validation-Test:
    - División de los datos finales en 4 conjuntos distintos:
      1. **Entrenamiento** (2010-2020): 3,249,868 filas (70.91%) - Utilizado para el entrenamiento inicial del modelo
      2. **Validación** (2021-2022): 633,758 filas (13.83%) - Utilizado para evaluación de rendimiento durante el entrenamiento
      3. **Prueba** (2023-2025): 699,154 filas (15.26%) - Conjunto ciego para evaluación final del modelo y métricas
      4. **Completo** (2010-2025): 4,582,780 filas (100%) - Conjunto de datos completo utilizado para el entrenamiento final del modelo desplegado
    ---
    #### 6. Escalado MinMax:
    - Escalado de todos los valores en los 4 conjuntos de datos de 0 a 1 utilizando MinMaxScaler
    - Creación y guardado de 2 escaladores separados:
      1. **Escalador de Entrenamiento**: Ajustado en el conjunto de entrenamiento y aplicado a los conjuntos de entrenamiento, validación y prueba
      2. **Escalador Completo**: Ajustado en el conjunto completo para transformar entradas reales de usuarios en el modelo desplegado
    """)

def results():
    st.markdown("---")
    st.header("Introducción a los Modelos Utilizados")

    st.markdown("""
    Para la implementación de las Redes Neuronales Recurrentes (RNNs), se han utilizado los modelos SimpleRNN, LSTM y GRU. \
    Estos modelos son capaces de capturar patrones complejos en los datos. \
    Además, se ha utilizado el modelo Prophet, desarrollado por Facebook, \
    """)

    st.markdown("""
    #### Modelo SimpleRNN
    El modelo SimpleRNN es una variante más simple de las redes neuronales recurrentes (RNN). \
    A diferencia de las RNN tradicionales, las SimpleRNN no tienen puertas de reinicio o actualización. \
    Esto significa que las SimpleRNN tienen más dificultades para recordar información a largo plazo y pueden sufrir de desaparición del gradiente. \
    Sin embargo, las SimpleRNN son más fáciles de entrenar y computacionalmente más eficientes que las RNN tradicionales.
    """)

    st.markdown("""
    #### Modelo Long Short-Term Memory (LSTM)
    El modelo LSTM es una variante de las redes neuronales recurrentes (RNN) que intenta resolver el problema de la desaparición del gradiente. \
    A diferencia de las RNN tradicionales, las LSTM tienen una estructura más compleja y tienen tres puertas: una de reinicio, una de actualización y una de olvido. \
    Estas puertas permiten que las LSTM "olviden" o "recuerden" información de manera más eficiente que las RNN tradicionales.
    """)

    st.markdown("""
    #### Modelo Gated Recurrent Unit (GRU)
    El modelo GRU es una variante de las redes neuronales recurrentes (RNN) que también intenta resolver el problema de la desaparición del gradiente. \
    A diferencia de LSTM, las GRU tienen una estructura más simple y solo tienen dos puertas: una de reinicio y otra de actualización. \
    Esto hace que las GRU sean más fáciles de entrenar y computacionalmente más eficientes que las LSTM.
    """)

    st.markdown("""
    #### Modelo Prophet
    Prophet es una librería de código abierto desarrollada por Facebook. \
    Está diseñada para realizar pronósticos de series temporales de manera sencilla y eficiente. Prophet es capaz de manejar series temporales con tendencias, estacionalidades y días festivos. \
    Además, Prophet es capaz de manejar datos faltantes y outliers de manera eficiente. \
    """)

    st.markdown("---")
    st.header("Resultados de los Modelos")

    st.markdown("##### Métricas de Evaluación:")

    st.write(metrics_df)

    st.markdown(""" 
    * **MSE**: Error Cuadrático Medio. Mide la media de los errores al cuadrado, es decir, cuánto se desvían las predicciones de los valores reales en promedio, elevando esas diferencias al cuadrado. Cuanto más bajo es el MSE, mejor es el ajuste del modelo.
    * **MAE**: Error Absoluto Medio. Mide el promedio de la magnitud de los errores, es decir, la diferencia promedio absoluta entre las predicciones y los valores reales. Cuanto más bajo es el MAE, más cerca están las predicciones de los valores reales.
    * **RMSE**: Raíz del Error Cuadrático Medio. Es la raíz cuadrada del MSE y se interpreta de la misma manera. Devuelve el error en la misma escala que los datos originales y, como el MSE, penaliza más los errores grandes.
    * **R2**: Coeficiente de Determinación. Indica qué proporción de la variabilidad de los datos está explicada por el modelo. El R2 está entre 0 y 1. Un valor de 1 significa una predicción perfecta, mientras que un valor de 0 significa que el modelo no consigue capturar bien la relación entre las variables.
    """)

    st.markdown("---")
    st.markdown("### Análisis de Resultados")

    st.markdown("Ambos GRU y LSTM cuentan con un MSE y RMSE bajo, y un R2 superior a los demás. \
    En este caso, los resultados son muy similares, lo cual no se puede claramente determinar cuál es mejor. \
    Ambos modelos son capaces de capturar patrones complejos en los datos, \
    y explican más del 60% de la variabilidad de los datos. \
    ")
    st.markdown("SimpleRNN Muestra un MSE y un RMSE algo más alto que GRU y LSTM, \
    y su R2 también es ligeramente inferior. \
    Tendrá menos capacidad para capturar patrones complejos que GRU y LSTM, \
    pero sigue siendo un modelo competente, \
    especialmente si se tiene en cuenta que es el más sencillo de los tres RNNs. \
    ")
    st.markdown(
    "Prophet, aunque presente un MSE y RMSE relativamente alto en comparación con los modelos de RNN, \
    el MAE es el más bajo, lo que sugiere que la mayoría de las predicciones están bastante cerca de los valores reales. \
    Esto es debido a que es un modelo que mide más la media en lugar de valores específicos, \
    por lo que es más robusto a los outliers. \
    Su R2 también está ligeramente por debajo de los modelos de RNN, \
    no obstante, sigue explicando más de la mitad de la variabilidad de los datos.")

    st.markdown("---")
    st.markdown("### Visualización de Resultados")

    gru, lstm, simplernn, prophet = st.tabs(["GRU", "LSTM", "SimpleRNN", "Prophet"])

    with gru:
        show_graphs(gru, "gru")

    with lstm:
        show_graphs(lstm, "lstm")

    with simplernn:
        show_graphs(simplernn, "simplernn")

    with prophet:
        show_graphs(prophet, "prophet")

intro()
pipeline()
results()