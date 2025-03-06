from datetime import datetime, timedelta, timezone
import streamlit as st
from helpers import api

st.set_page_config(page_title="Análisis Meteorológico", page_icon=":lightning:", layout="wide",
                   initial_sidebar_state="expanded")

def check_latest():
    res = api.get_latest_fetch()
    if res:
        fetched_time = datetime.fromisoformat(res['fetched'])
        if datetime.now(timezone.utc) - fetched_time > timedelta(hours=1):
            with st.spinner("Fetching latest data..."):
                api.fetch_latest()
            st.rerun()

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
        "Datos": [
            st.Page("src/streamlit_app/Pages/Datasets/Historico.py", title="📚 Datos Históricos"),
            st.Page("src/streamlit_app/Pages/Datasets/ML.py", title="📊 Datos ML"),
        ],
        "API": [
            st.Page("src/streamlit_app/Pages/API/API Docs.py", title="📜 API Docs")
        ]
    }

    check_latest()

    pg = st.navigation(pages)
    pg.run()
