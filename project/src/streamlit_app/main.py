import streamlit as st

st.set_page_config(page_title="Análisis Meteorológico", page_icon=":lightning:", layout="wide", initial_sidebar_state="expanded")

def main():
    
    pages = {
        "Main": [
            st.Page("Pages/Main/Dashboard.py", title="Dashboard"),
            st.Page("Pages/Main/API Docs.py", title="API Docs")
        ]
    }

    pg = st.navigation(pages)
    pg.run()

if __name__ == "__main__":
    main()