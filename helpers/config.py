import os
import toml
from dotenv import load_dotenv, find_dotenv

from helpers.logger import setup_logger

logger = setup_logger('config')
script_dir = os.path.dirname(os.path.realpath(__file__))

if bool(find_dotenv()):
    load_dotenv()
    DEV_MODE = os.getenv('DEV') == 'true'
else:
    DEV_MODE = False

logger.debug(f"DEV MODE: {DEV_MODE}")

try:
    import streamlit as st

    streamlit_dict = st.__dict__
    st_secrets = toml.load(".streamlit/secrets.toml")

    STREAMLIT_MODE = 'secrets' in streamlit_dict and st_secrets
except (FileNotFoundError, ImportError):
    STREAMLIT_MODE = False

logger.debug(f"STREAMLIT MODE: {STREAMLIT_MODE}")

def get_env_var(key: str) -> str:
    """Retrieve environment variable from .env (dev) or Streamlit secrets (prod)."""
    value = None

    if STREAMLIT_MODE:
        try:
            value = st.secrets[key]
        except KeyError:
            logger.warning(f"Warning: {key} not found in Streamlit secrets")

    else:
        value = os.getenv(key)
        if value is None:
            logger.warning(f"Warning: {key} not found in .env file")

    return value


api_host = get_env_var("API_HOST")
streamlit_host = get_env_var("STREAMLIT_HOST")

if DEV_MODE:
    api_port = get_env_var("API_PORT")
    streamlit_port = get_env_var("STREAMLIT_PORT")
    api_url = f"http://{api_host}:{api_port}/api"
    streamlit_url = f"http://{streamlit_host}:{streamlit_port}"
else:
    api_url = f"https://{api_host}/api"
    streamlit_url = f"https://{streamlit_host}"

logger.debug(f"API URL: {api_url}")
logger.debug(f"Streamlit URL: {streamlit_url}")