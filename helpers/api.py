from helpers.config import api_url
from helpers.http_request import get

table_url = api_url + "/db/{table}"
historico_url = api_url + "/db/historico"
latest_fetch_url = api_url + "/db/historico/latest-fetch"
fetch_latest_url = api_url + "/db/historico/fetch-latest"

def get_table(table: str):
    return get(table_url['table'].format(table=table))[0]


def get_estacion_historico(idema: str, elemento: str):
    params = {
        'idema': idema,
        'elementos': elemento
    }
    return get(url=historico_url, params=params)[0]


def get_estaciones_historico(elemento: str):
    params = {
        'elementos': elemento
    }
    return get(url=historico_url, params=params)[0]


def get_estacion_historico_rango(idema: str, elemento: str, fecha_ini: str, fecha_fin: str):
    params = {
        'idema': idema,
        'elementos': elemento,
        'fecha_ini': fecha_ini,
        'fecha_fin': fecha_fin
    }
    return get(url=historico_url, params=params)[0]

def get_estaciones_historico_rango(elemento: str, fecha_ini: str, fecha_fin: str):
    params = {
        'elementos': elemento,
        'fecha_ini': fecha_ini,
        'fecha_fin': fecha_fin
    }
    return get(url=historico_url, params=params)[0]

def get_latest_fetch():
    return get(url=latest_fetch_url)[0][0]

def fetch_latest():
    return get(url=fetch_latest_url)[0]
