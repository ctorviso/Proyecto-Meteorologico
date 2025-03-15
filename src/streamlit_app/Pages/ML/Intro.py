from helpers.config import script_dir
import os
import pandas as pd

def show(tab):

    tab.markdown("""
    ## :thermometer: Desarrollo de Modelos de Machine Learning para la Predicción de Temperatura Media Diaria para Estaciones Meteorológicas en España
    ###### Los conjuntos de datos finales pueden ser encontrados en la pestaña 'Datos ML'
    ---
    """)

    col1, col2 = tab.columns(2)

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

    tab.markdown("""
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
    tab.write("Correlación de todas las características")
    tab.image(os.path.join(script_dir, "../data/model_res/images/corr1.png"))
    tab.write("Correlación de las características seleccionadas")
    tab.image(os.path.join(script_dir, "../data/model_res/images/corr2.png"))

    tab.markdown("---")

    col1, col2, _ = tab.columns(3)

    col1.markdown("##### Características Seleccionadas")
    col1.write(pd.read_csv(os.path.join(script_dir, "../data/model_res/tables/cols_conservadas.csv")))

    col2.markdown("##### Características Eliminadas")
    col2.write(pd.read_csv(os.path.join(script_dir, "../data/model_res/tables/cols_eliminadas.csv")))

    tab.markdown("---")

    tab.markdown("""
    #### 3. Búsqueda de Estación más Cercana:
    - Creación de un mapeo de cada estación a todas las demás estaciones en orden desde la más cercana a la más lejana
    - Distancia calculada utilizando latitud, longitud y altitud después de aplicar StandardScaler
    ---
    #### 4. Imputación por Estación más Cercana:
    - Imputación de todos los valores NaN utilizando la media de las 5 estaciones más cercanas para cada día
    - Este enfoque previene la filtración de datos entre conjuntos, ya que solo utiliza datos del mismo día
    - Columnas imputadas y sus porcentajes de valores faltantes:
      
    | Columna   | % NaN | Correlación con tmed |
    |-----------|-------|--------------------- |
    | tmed      | 2.27% | - |
    | tmax      | 2.23% | 96% |
    | tmin      | 2.24% | 94% |
    | hr_media  | 5.60% | -47% |
    | hr_max    | 5.90% | -44% |
    | prec      | 3.64% | -27% |
    
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