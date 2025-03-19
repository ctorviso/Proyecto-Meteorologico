import numpy as np
import streamlit as st
import pandas as pd
import requests
from io import StringIO

from sklearn.preprocessing import MinMaxScaler

BASE_URL = "https://rednvrsdcuwtwyfxtjru.supabase.co/storage/v1/object/public/historical"

years = list(range(1997, 2026))

st.title("📚 Datasets Históricos de la AEMET")
st.markdown("Datos meteorológicos históricos para España de los años 1997-2025 extraídos de AEMET.")

tab1, tab2, tab3 = st.tabs(["Navegador de Archivos", "Previsualización de Datos", "Comparador de Años"])

with tab1:
    st.header("Archivos Disponibles")
    all_files = [f"{year}.csv" for year in years] + [f"{year}_avg.csv" for year in years]
    all_files.sort()
    with st.columns(2)[0]:
        file_name = st.selectbox("Seleccionar Dataset:", all_files, key="year")

    if "avg" in file_name:
        file_url = f"{BASE_URL}/historico_avg/{file_name.replace('_avg', '')}"
    else:
        file_url = f"{BASE_URL}/historico/{file_name}"

    if st.button("Visualizar y Descargar"):
        with st.spinner("Cargando archivo..."):
            file = requests.get(file_url).text
            if file:
                data = pd.read_csv(StringIO(file))
                st.subheader("Muestra de Datos")
                st.write(data.head(5))
                st.download_button("Descargar", file, f"{file_name}", "csv")

with tab2:
    st.header("Previsualización de Datos")

    data_category = st.radio("Seleccionar categoría:", ["historico", "historico_avg"])
    selected_year = st.select_slider("Seleccionar Año:", years)

    selected_url = f"{BASE_URL}/{data_category}/{selected_year}.csv"

    if st.button("Previsualizar Datos"):
        try:
            st.info(f"Cargando preview para {data_category}/{selected_year}.csv...")

            response = requests.get(selected_url)

            if response.status_code == 200:
                data = pd.read_csv(StringIO(response.text))

                st.subheader("Estadísticas")
                st.write(data.describe())

                st.subheader("Información de Columnas")
                col_info = pd.DataFrame({
                    'Columna': data.columns,
                    'Data Type': data.dtypes.values,
                    'Non-Null Count': data.count().values,
                    'Null Count': data.isna().sum().values
                })
                st.write(col_info)

                st.subheader(f"Muestra de {selected_year}")
                st.write(data.head(10))
            else:
                st.error(f"Error en cargar. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Error al intentar previsualizar: {str(e)}")

with tab3:
    st.header("Comparador de Años")

    compare_category = st.radio("Selecciona la categoría:", ["historico", "historico_avg"],
                                key="compare_category")

    compare_years = st.multiselect("Selecciona los años a comparar:", years, default=[years[-1], years[-2]])

    if st.button("Comparar Años"):
        if len(compare_years) < 1:
            st.warning("Por favor seleccione al menos un año para comparar.")
        else:
            try:
                all_data = {}

                for year in compare_years:
                    url = f"{BASE_URL}/{compare_category}/{year}.csv"
                    response = requests.get(url)

                    if response.status_code == 200:
                        df = pd.read_csv(StringIO(response.text))
                        all_data[year] = df
                    else:
                        st.error(f"Error en cargar año {year}. Status code: {response.status_code}")

                if all_data:
                    if len(all_data) > 1:

                        st.header("Mapa de Calor")

                        for year, df in all_data.items():
                            st.subheader(year)

                            num_cols = df.select_dtypes(include=['float64', 'int64']).columns
                            corr = df[num_cols].corr()
                            mask = np.triu(np.ones_like(corr, dtype=bool))
                            heatmap = corr.style.background_gradient(cmap='coolwarm', axis=None)
                            heatmap.data = heatmap.data.mask(mask)

                            st.write(heatmap)

                        st.markdown("---")

                        st.header("Resumen de Datos")

                        for year, df in all_data.items():
                            st.subheader(year)
                            st.write(df.describe())

            except Exception as e:
                st.error(f"Error al comparar años: {str(e)}")

st.markdown("---")
