from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Query, Request
from etl_scripts.pipeline import run_etl_latest
from helpers.config import get_env_var
from helpers.lookups import element_cols_map, elements, element_cols_map_numeric
from helpers.preprocessing import truncate_date_range
from src.db.db_handler import DBHandler

db = DBHandler()
router = APIRouter()

table_names = ["estaciones", "provincias", "comunidades_autonomas", 'historico', 'historico_avg']

# Dynamic route creation
for table in table_names:
    def make_table_route(table_name: str):
        def get_table(columns: Optional[str] = None):
            columns = columns.replace(' ', '') if columns else None
            columns = columns.split(',') if columns else None
            return db.get_columns(table_name, columns)

        return get_table

    def make_schema_route(table_name: str):
        def get_schema():
            return db.get_schema(table_name)

        return get_schema

    if table not in ['historico', 'historico_avg']:
        router.add_api_route(f"/table/{table}", make_table_route(table), methods=["GET"])
    router.add_api_route(f"/schema/{table}", make_schema_route(table), methods=["GET"])


elementos_query = Query(None,
    title="Elementos",
    description=f"""Elementos a mostrar separados por coma.\nValores posibles: {', '.join(elements)}""",
    alias="elementos"
)

idemas_query = Query(None,
    title="IDEMAs",
    description="IDEMAs de las estaciones a mostrar separados por coma. Ejemplos: 3129, 1387",
    alias="idema"
)

provincia_ids_query = Query(None,
    title="Provincia IDs",
    description="IDs de las provincias a mostrar separados por coma. Ejemplos: 28, 15",
    alias="provincia_id"
)

today = datetime.now().strftime('%Y-%m-%d')
last_week = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

fecha_ini_query = Query(None,
    title="Fecha inicio",
    description=f"Fecha de inicio en formato YYYY-MM-DD. eg. {last_week}",
    alias="fecha_ini"
)

fecha_fin_query = Query(None,
    title="Fecha fin",
    description=f"Fecha de fin en formato YYYY-MM-DD. eg. {today}",
    alias="fecha_fin"
)

@router.get("/historico")
def get_historico(
        elementos: Optional[str] = elementos_query,
        idemas: Optional[str] = idemas_query,
        fecha_ini: Optional[str] = fecha_ini_query,
        fecha_fin: Optional[str] = fecha_fin_query
):
    all_cols = [] if elementos else None
    if elementos:
        for element in elementos.lower().split(","):
            all_cols.extend(element_cols_map[element.strip()])
        all_cols += ["idema", "fecha"]

    idemas = idemas.replace(" ", "") if idemas else None
    fecha_ini = fecha_ini.strip() if fecha_ini else None
    fecha_fin = fecha_fin.strip() if fecha_fin else None

    fecha_ini, fecha_fin = truncate_date_range(fecha_ini, fecha_fin)

    return db.get_historico(all_cols, idemas, fecha_ini, fecha_fin)

@router.get("/historico_average")
def get_historico_average(
        elementos: Optional[str] = elementos_query,
        provincia_ids: Optional[str] = provincia_ids_query,
        fecha_ini: Optional[str] = fecha_ini_query,
        fecha_fin: Optional[str] = fecha_fin_query
):
    all_cols = [] if elementos else None
    if elementos:
        for element in elementos.lower().split(","):
            all_cols.extend(element_cols_map_numeric[element.strip()])
        all_cols += ["provincia_id", "fecha"]

    provincia_ids = provincia_ids.replace(" ", "") if provincia_ids else None
    fecha_ini = fecha_ini.strip() if fecha_ini else None
    fecha_fin = fecha_fin.strip() if fecha_fin else None

    fecha_ini, fecha_fin = truncate_date_range(fecha_ini, fecha_fin)

    return db.get_historico_average(all_cols, provincia_ids, fecha_ini, fecha_fin)


@router.get("/historico/date/earliest")
def get_earliest_historical_date():
    return db.get_earliest_historical_date()

@router.get("/historico/date/latest")
def get_latest_historical_date():
    return db.get_latest_historical_date()


@router.get("/historico/fetch-latest")
async def fetch_latest_historical(request: Request):
    if not get_env_var("AEMET_API_KEY") and not get_env_var("AEMET_API_KEY_1"):
        return {'message': 'No AEMET API Key is present.'}
    response = await run_etl_latest(request.client.host)
    return {'message': response}

@router.get("/historico/latest-fetch")
def get_latest_fetch():
    return db.get_latest_fetch()
