from typing import List, Optional

from helpers.config import api_url
from helpers.http_request import get

table_url = api_url + "/db/{table}"
historico_url = api_url + "/db/historico"
historico_earliest_url = api_url + "/db/historico/date/earliest"
historico_latest_url = api_url + "/db/historico/date/latest"
historico_avg_url = api_url + "/db/historico_average"
latest_fetch_url = api_url + "/db/historico/latest-fetch"
fetch_latest_url = api_url + "/db/historico/fetch-latest"

def get_table(table: str):
    return get(table_url['table'].format(table=table))[0]

def get_historico(
        elementos: Optional[List[str]] = None,
        idemas: Optional[List[str]] = None,
        fecha_ini: Optional[str] = None,
        fecha_fin: Optional[str] = None
):
    params = {
        'elementos': ",".join(elementos) if elementos else None,
        'idemas': ",".join(idemas) if idemas else None,
        'fecha_ini': fecha_ini,
        'fecha_fin': fecha_fin
    }
    return get(url=historico_url, params=params)[0]

def get_historico_average(
        elementos: Optional[List[str]] = None,
        provincia_ids: Optional[List[str]] = None,
        fecha_ini: Optional[str] = None,
        fecha_fin: Optional[str] = None
):
    params = {
        'elementos': ",".join(elementos) if elementos else None,
        'provincia_ids': ",".join(provincia_ids) if provincia_ids else None,
        'fecha_ini': fecha_ini,
        'fecha_fin': fecha_fin
    }
    return get(url=historico_avg_url, params=params)[0]

def get_earliest_historical_date():
    return get(url=historico_earliest_url)[0]

def get_latest_historical_date():
    return get(url=historico_latest_url)[0]

def get_latest_fetch():
    return get(url=latest_fetch_url)[0][0]

def fetch_latest():
    return get(url=fetch_latest_url)[0]
