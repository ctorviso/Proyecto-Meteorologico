from fastapi import FastAPI
from src.api.routes import aemet_routes
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import db_routes
from src.shared.helpers import get_env_var, DEV_MODE

if DEV_MODE:
    api_url = f"http://{get_env_var('API_HOST')}:{get_env_var('API_PORT')}/api"
    streamlit_url = f"http://{get_env_var('STREAMLIT_HOST')}:{get_env_var('STREAMLIT_PORT')}"
else:
    api_url = f"https://{get_env_var('API_HOST')}/api"
    streamlit_url = f"https://{get_env_var('STREAMLIT_HOST')}"

app = FastAPI(title="Proyecto Meteorológico API", docs_url="/api/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[api_url, streamlit_url],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Accept",
        "Accept-Encoding",
        "Accept-Language",
        "Origin",
        "Referer",
        "User-Agent",
        "Cache-Control",
        "Access-Control-Allow-Origin",
    ],
)

@app.get("/")
def read_root():
    return {
        "Site": f"{streamlit_url}",
        "Docs": f"{api_url}/docs"
    }

app.include_router(aemet_routes.router, prefix="/api/aemet")
app.include_router(db_routes.router, prefix="/api/db")
