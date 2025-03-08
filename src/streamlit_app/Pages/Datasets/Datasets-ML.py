import streamlit as st
import pandas as pd
import requests
from io import StringIO


BASE_URL = "https://rednvrsdcuwtwyfxtjru.supabase.co/storage/v1/object/public/ml"

files = [
    {"name": "train.csv", "description": "Training dataset", "url": f"{BASE_URL}/train.csv"},
    {"name": "validation.csv", "description": "Validation dataset", "url": f"{BASE_URL}/validation.csv"},
    {"name": "test.csv", "description": "Testing dataset", "url": f"{BASE_URL}/test.csv"},
    {"name": "train_scaled.csv", "description": "Scaled training dataset", "url": f"{BASE_URL}/train_scaled.csv"},
    {"name": "validation_scaled.csv", "description": "Scaled validation dataset", "url": f"{BASE_URL}/validation_scaled.csv"},
    {"name": "test_scaled.csv", "description": "Scaled testing dataset", "url": f"{BASE_URL}/test_scaled.csv"},

    {"name": "scaler_X_full.joblib", "description": "Scaler for X_full", "url": f"{BASE_URL}/scaler_X_full.joblib"},
    {"name": "scaler_y_full.joblib", "description": "Scaler for y_full", "url": f"{BASE_URL}/scaler_y_full.joblib"},
    {"name": "scaler_X_train.joblib", "description": "Scaler for X_train", "url": f"{BASE_URL}/scaler_X_train.joblib"},
    {"name": "scaler_y_train.joblib", "description": "Scaler for y_train", "url": f"{BASE_URL}/scaler_y_train.joblib"},
]

st.title("📊 Datasets para los modelos de Machine Learning")
st.markdown("En esta sección puedes descargar los datasets que se utilizaron para entrenar los modelos de Machine Learning.")

tab1, tab2 = st.tabs(["Navegador de Archivos", "Visualización de datos"])

with tab1:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Datos Crudos")
        for file in files[:3]:
            with st.expander(file["name"]):
                st.write(file["description"])
                st.markdown(f"[Descargar {file['name']}]({file['url']})")

    with col2:
        st.subheader("Datos Escalados")
        for file in files[3:]:
            with st.expander(file["name"]):
                st.write(file["description"])
                st.markdown(f"[Descargar {file['name']}]({file['url']})")

with tab2:
    st.header("Visualización de datos")

    selected_file = st.selectbox("Seleccionar un archivo a visualizar:", [file["name"] for file in files])

    selected_url = next(file["url"] for file in files if file["name"] == selected_file)

    if st.button("Visualizar"):
        try:
            st.info(f"Cargando {selected_file}...")

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

                st.subheader("Muestra de las primeras 10 filas")
                st.write(data.head(10))
            else:
                st.error(f"Error en cargar el archivo. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Error en visualizar el archivo: {str(e)}")

st.markdown("---")
