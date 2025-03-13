import streamlit as st

st.title("📑 Esquema de la Base de Datos")

dbml = 'https://dbdiagram.io/e/67d2183575d75cc844e028ca/67d2369175d75cc844e26ae3'

st.markdown("---")

st.markdown(f'<iframe width="100%" height="800" src="{dbml}" title="DBML"></iframe>', unsafe_allow_html=True)
