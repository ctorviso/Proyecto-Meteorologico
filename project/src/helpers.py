# --- Configuration --- #

import os
from dotenv import load_dotenv, find_dotenv

DEV_MODE = bool(find_dotenv())
if DEV_MODE:
    load_dotenv()

def get_env_var(key: str) -> str:
    """Retrieve environment variable from .env (dev) or Streamlit secrets (prod)."""
    if DEV_MODE:
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"Error: {key} not found in .env file")
    else:
        try:
            import streamlit as st
            value = st.secrets[key]
        except KeyError:
            raise ValueError(f"Error: {key} not found in Streamlit secrets")

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