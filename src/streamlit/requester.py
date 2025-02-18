from src.api.services import http_request
import streamlit as st
from src.streamlit.config import api_url

def get_request(endpoint: str):
    url = f"{api_url}{endpoint}"
    response = http_request.make_request(url=url, method='get')

    data = response[0]
    status = response[1]

    if status != 200:
        st.error(f"Error al obtener los datos: {status}")
        return None
    else:
        st.success("Datos obtenidos correctamente")
        return data