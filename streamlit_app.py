import streamlit as st

st.set_page_config(page_title="Análisis Meteorológico", page_icon=":lightning:", layout="wide", initial_sidebar_state="expanded")

def main():
    
    pages = {
        "Main": [
            st.Page("src/streamlit/Pages/Main/Dashboard.py", title="Welcome"),
            st.Page("src/streamlit/Pages/Main/API Docs.py", title="API Docs")
        ],
        "AEMET": [
            st.Page("src/streamlit/Pages/AEMET/Live Data.py", title="Dashboard")
        ],
    }

    pg = st.navigation(pages)
    pg.run()

if __name__ == "__main__":
    main()