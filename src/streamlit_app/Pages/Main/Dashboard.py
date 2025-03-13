import streamlit as st


st.title(':lightning: Análisis Meteorológico')
st.markdown("""---""")

st.markdown("""##### <u>Secciones</u>:""", unsafe_allow_html=True)

st.markdown("""          
* **Principal**: Introducción, presentación del equipo y contacto.  

* **Análisis Exploratorio de Datos**: Visualizaciones de los principales datos meteorológicos y un mapa coroplético para visualizar estos mismos datos por provincia.  

* **Machine Learning**: Predicciones de la temperatura utilizando diferentes modelos de machine learning.  
            
* **Datos**: Acceso a los datos que se han extraído de la AEMET para la realización de este proyecto, incluyendo los datos procesados y modelos de machine learning.  
            
* **Framework**: Información técnica sobre la estructura detrás de la página, tanto sobre la API cómo la BBDD.

""", unsafe_allow_html=True)

st.markdown("""---""")

st.markdown("""
Para personas técnicas con curiosidad sobre el código, pueden acceder al repositorio en el siguiente enlace:
""")
st.link_button('Repositorio GitHub', 'https://github.com/HAB-Equipo-Meteorologia/Proyecto-Meteorologico')
