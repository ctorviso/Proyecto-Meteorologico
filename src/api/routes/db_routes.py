from src.db.db_handler import DBHandler
from fastapi import APIRouter

db = DBHandler()
router = APIRouter()

table_names = ["estaciones", "provincias", "municipios", "comunidades_autonomas"]

# Dynamic route creation
for table in table_names:
    route = f"/{table}"

    def make_route(table_name: str):
        def route_handler():
            return db.get_table_data(table_name)
        return route_handler

    router.add_api_route(route, make_route(table), methods=["GET"])
