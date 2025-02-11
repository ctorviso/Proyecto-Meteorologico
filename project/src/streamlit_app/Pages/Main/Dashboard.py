import streamlit as st

st.title('Análisis Meteorológico')

repo_url = 'https://github.com/HAB-Equipo-Meteorologia/Proyecto-Meteorologico'
st.link_button('Repositorio GitHub', repo_url)

docs_url = 'http://localhost:8000/docs'
st.link_button('Documentación API', docs_url)
