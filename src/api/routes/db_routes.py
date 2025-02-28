from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Query

from helpers.lookups import element_cols_map, elements
from src.db.db_handler import DBHandler

db = DBHandler()
router = APIRouter()

table_names = ["estaciones", "provincias", "comunidades_autonomas"]

# Dynamic route creation
for table in table_names:
    def make_table_route(table_name: str):
        def route_handler():
            return db.get_table(table_name)

        return route_handler


    def make_columns_route(table_name: str):
        def route_handler(columns: str):
            return db.get_columns(table_name, columns.split(","))

        return route_handler


    router.add_api_route(f"/{table}", make_table_route(table), methods=["GET"])
    router.add_api_route(f"/{table}/columns", make_columns_route(table), methods=["GET"])

elementos_query = Query(None,
    title="Elementos",
    description=f"""Elementos a mostrar separados por coma.\nValores posibles: {', '.join(elements)}""",
    alias="elementos"
)

idemas_query = Query(None,
    title="IDEMA",
    description="IDEMAs de las estaciones a mostrar separados por coma. Ejemplos: 3129, 1387",
    alias="idema"
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
    all_cols = []
    for element in elementos.lower().split(","):
        all_cols.extend(element_cols_map[element.strip()])
    idemas = idemas.replace(" ", "") if idemas else None
    fecha_ini = fecha_ini.strip() if fecha_ini else None
    fecha_fin = fecha_fin.strip() if fecha_fin else None
    all_cols += ["idema", "fecha"]
    return db.get_historico(all_cols, idemas, fecha_ini, fecha_fin)
