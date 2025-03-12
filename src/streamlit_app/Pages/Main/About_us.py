import streamlit as st

st.title(":female-technologist: Sobre nosotras")

linkedin_logo = "https://cdn-icons-png.flaticon.com/512/174/174857.png"
github_logo = "https://cdn-icons-png.flaticon.com/512/733/733609.png" 


claudia_linkedin = "https://www.linkedin.com/in/claudiatorviso/"
paola_linkedin = "https://www.linkedin.com/in/ana-paola-gutierrez-102096106/"
sara_linkedin = "https://www.linkedin.com/in/saragarcia6123/"

claudia_github = "https://github.com/ctorviso"
paola_github = "https://github.com/PaoPaoGuti"
sara_github = "https://github.com/saragarcia6123"

st.markdown("""
#### ¿Quiénes somos?:
Somos tres estudiantes de Data Science en Hack A Boss que nos hemos unido para implementar nuestros conocimientos adquiridos durante el bootcamp en un proyecto con datos reales.
            """)

st.markdown("""---""")
st.markdown("""                    
#### Nuestro Equipo:
""")
            
st.markdown(
    f"* **Claudia Torviso** <a href='{claudia_linkedin}' target='_blank'><img src='{linkedin_logo}' width='20'></a> <a href='{claudia_github}' target='_blank'><img src='{github_logo}' width='20' style='filter: invert(100%);'></a>",
    unsafe_allow_html=True
)

st.markdown(
    f"* **Ana Paola Gutiérrez** <a href='{paola_linkedin}' target='_blank'><img src='{linkedin_logo}' width='20'></a> <a href='{paola_linkedin}' target='_blank'><img src='{github_logo}' width='20' style='filter: invert(100%);'></a>",
    unsafe_allow_html=True
)

st.markdown(
    f"* **Sara García** <a href='{sara_linkedin}' target='_blank'><img src='{linkedin_logo}' width='20'></a> <a href='{sara_github}' target='_blank'><img src='{github_logo}' width='20' style='filter: invert(100%);'></a>",
    unsafe_allow_html=True
)

st.markdown("""---""")

st.markdown("""
#### Nuestra misión:
Desarrollar una herramienta que pueda ser utilizada por personas interesadas en la meteorología o personas que necesiten un pronóstico del tiempo, en concreto de la temperatura, en una ubicación concreta para un rango temporal concreto.
            
¡Muchas gracias por visitar nuestro proyecto y no dudes en ponerte en contacto con nosotras!
""")

st.markdown("""---""")