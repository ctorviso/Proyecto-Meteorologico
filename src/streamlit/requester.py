from src.api.services import http_request
from src.streamlit.config import api_url

def get_request(endpoint: str):
    url = f"{api_url}{endpoint}"
    response = http_request.make_request(url=url, method='get')

    data = response[0]
    status = response[1]

    if status != 200:
        return None
    else:
        return data