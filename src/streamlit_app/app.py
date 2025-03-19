import streamlit as st
from src.streamlit_app.background import check_latest


def main():

    st.set_page_config(page_title="Análisis Meteorológico", page_icon=":lightning:", layout="wide", initial_sidebar_state="expanded")

    st.markdown("""
    <style>
        :root {
            --primary-color: #00AEEF;
            --background-color: #121212;
            --secondary-background-color: #1E1E1E;
            --text-color: #E0E0E0;
            --font: sans-serif;
        }
        [data-testid="stSidebar"] {
            max-width: 200px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    pages = {
        "Principal": [
            st.Page("src/streamlit_app/Pages/Main/Dashboard.py", title="👋 Introducción"),
            st.Page("src/streamlit_app/Pages/Main/About_us.py", title="👩‍💻 Equipo de Desarrollo"),
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
        "Framework": [
            st.Page("src/streamlit_app/Pages/Framework/API Docs.py", title="📜 API Docs"),
            st.Page("src/streamlit_app/Pages/Framework/BBDD.py", title="📑 Esquema BBDD"),
            st.Page("src/streamlit_app/Pages/Framework/Arquitectura.py", title="🏗️ Arquitectura"),
            #st.Page("src/streamlit_app/Pages/Framework/Futuro.py", title="🚀 Ideas a Futuro"),
        ]
    }

    check_latest()

    pg = st.navigation(pages)
    pg.run()
