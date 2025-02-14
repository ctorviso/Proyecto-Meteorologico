# --- Configuration --- #

import os
from dotenv import load_dotenv, find_dotenv

if bool(find_dotenv()):
    load_dotenv()
    DEV_MODE = os.getenv('DEV') == 'true'
else:
    DEV_MODE = False

try:
    import streamlit as st
    STREAMLIT_MODE = 'secrets' in st.__dict__ and bool(st.secrets)
except (FileNotFoundError, ImportError):
    STREAMLIT_MODE = False

def get_env_var(key: str) -> str:
    """Retrieve environment variable from .env (dev) or Streamlit secrets (prod)."""

    if STREAMLIT_MODE:
        try:
            value = st.secrets[key]
        except KeyError:
            raise ValueError(f"Error: {key} not found in Streamlit secrets")

    else:
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"Error: {key} not found in .env file")

    return value

# --- HTTP  --- #

from urllib.parse import urlencode, urlparse

def replace_url_params(url, **kwargs) -> str:
    try:
        return url.format(**kwargs)
    except KeyError as e:
        raise ValueError(f"Missing required parameter: {e}")

def combine_url_params(url: str, params: dict) -> str:
    if not params:
        return url

    parsed = urlparse(url)
    separator = "&" if parsed.query else "?"

    return f"{url}{separator}{urlencode(params)}"