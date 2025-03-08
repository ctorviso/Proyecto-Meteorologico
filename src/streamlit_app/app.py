import streamlit as st
from src.streamlit_app.background import check_latest

st.set_page_config(page_title="Análisis Meteorológico", page_icon=":lightning:", layout="wide",
                   initial_sidebar_state="expanded")


def main():
    pages = {
        "Principal": [
            st.Page("src/streamlit_app/Pages/Main/Dashboard.py", title="👋 Bienvenidos"),
            st.Page("src/streamlit_app/Pages/Main/About_us.py", title="👩‍💻 Sobre nosotras"),
        ],
        "Análisis Exploratorio de Datos": [
            st.Page("src/streamlit_app/Pages/EDA/Graficos.py", title="📈 Gráficos"),
            st.Page("src/streamlit_app/Pages/EDA/Mapa.py", title="🗺️ Mapa"),
        ],
        "Machine Learning": [
            st.Page("src/streamlit_app/Pages/ML/ML-Intro.py", title="🤖 Introducción"),
            st.Page("src/streamlit_app/Pages/ML/ML-Modelos.py", title="🧠 Modelos"),
        ],
        "Datos": [
            st.Page("src/streamlit_app/Pages/Datasets/Datasets-Historico.py", title="📚 Datos Históricos"),
            st.Page("src/streamlit_app/Pages/Datasets/Datasets-ML.py", title="📊 Datos ML"),
        ],
        "API": [
            st.Page("src/streamlit_app/Pages/API/API Docs.py", title="📜 API Docs")
        ]
    }

    check_latest()

    pg = st.navigation(pages)
    pg.run()
