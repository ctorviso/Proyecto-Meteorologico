import streamlit as st
import pandas as pd
import json
from src.api.services import http_request
from src.shared import helpers

host = helpers.get_env_var("HOST")

if host == "localhost":
    aemet_url = f"http://{host}:8000/api/aemet"
    db_url = f"http://{host}:8000/api/db"
else:
    aemet_url = f"https://{host}/api/aemet"
    db_url = f"https://{host}/api/db"


endpoint = "/tiempo-actual/{idema}"
idema = st.text_input("Introduce el ID de la estación meteorológica")

if st.button("Obtener datos"):
    url = aemet_url + endpoint.format(idema=idema)
    response = http_request.make_request(url=url, method='get')

    data = json.loads(response[0]['datos'][0])
    df = pd.DataFrame(data)
    st.write(df)