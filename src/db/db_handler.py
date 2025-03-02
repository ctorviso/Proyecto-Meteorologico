import datetime
from typing import Optional, List, Union
import psycopg2
import psycopg2.extensions
from sqlalchemy import create_engine, text, Table, MetaData
from helpers.config import get_env_var
from helpers.logger import setup_logger


def adapt_time(time_obj):
    return psycopg2.extensions.AsIs("'%s'::time" % time_obj.strftime('%H:%M:%S'))

psycopg2.extensions.register_adapter(datetime.time, adapt_time)


# noinspection PyMethodMayBeStatic
class DBHandler:

    elementos = ['lluvia', 'temperatura', 'viento', 'humedad']

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBHandler, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(
            self,
            user: str = None,
            password: str = None,
            host: str = None,
            port: str = None,
            dbname: str = None
    ):
        self.logger = setup_logger("db_handler")
        try:
            self.USER = user or get_env_var("DB_USER")
            self.PASSWORD = password or get_env_var("DB_PASSWORD")
            self.HOST = host or get_env_var("DB_HOST")
            self.PORT = port or get_env_var("DB_PORT")
            self.DBNAME = dbname or get_env_var("DB_NAME")
        except KeyError as e:
            raise ValueError(f"Missing environment variable: {str(e)}")

        self.URL = f"postgresql+psycopg2://{self.USER}:{self.PASSWORD}@[{self.HOST}]:{self.PORT}/{self.DBNAME}?sslmode=require"
        self.engine = create_engine(self.URL)
        self.logger.info("DBHandler initialized")

    def insert_data(self, table_name: str, data: dict):
        columns = list(data.keys())
        rows = list(zip(*data.values()))
        placeholders = ", ".join([f":{col}" for col in columns])
        query = text(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})")

        with self.engine.connect() as connection:
            for row in rows:
                connection.execute(query, dict(zip(columns, row)))
            connection.commit()

    def bulk_insert_data(self, table_name: str, data: dict):
        self.logger.info(f"Inserting data into table {table_name}...")
        table = Table(table_name, MetaData(), autoload_with=self.engine)
        records = []
        if data and all(isinstance(v, list) for v in data.values()):
            n_records = len(next(iter(data.values())))
            for i in range(n_records):
                record = {col: data[col][i] for col in data}
                records.append(record)

        with self.engine.begin() as connection:
            result = connection.execute(table.insert(), records)
            self.logger.info(f"Rows affected: {result.rowcount}")

    # In case of insertion mistakes, thanks to the extraction column we can easily revert back
    def delete_extracted_after_date(self, date_threshold):
        self.logger.info(f"Deleting data extracted after {date_threshold}...")
        query = f"GET uuid FROM historico_meta WHERE extracted >= :date_threshold"
        uuids = self.fetch(query, {"date_threshold": date_threshold})
        # Delete from all tables
        for elemento in self.elementos:
            query = f"DELETE FROM {elemento}_historico WHERE uuid IN :uuids"
            self.fetch(query, {"uuids": tuple(uuids)})
        query = f"DELETE FROM historico_meta WHERE extracted >= :date_threshold"
        self.fetch(query, {"date_threshold": date_threshold})

    def get_table(self, table_name: str):
        """Consulta de datos de una tabla en la base de datos"""
        query = text(f"SELECT * FROM {table_name}")
        with self.engine.connect() as connection:
            result = connection.execute(query)
            return [dict(zip(result.keys(), row)) for row in result]

    def get_schema(self, table_name: str):
        query = text(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = :table_name")
        with self.engine.connect() as connection:
            result = connection.execute(query, {"table_name": table_name})
            return [dict(zip(result.keys(), row)) for row in result]

    def get_columns(self, table_name: str, column_names: list):
        """Consulta de datos de una columna en la base de datos"""
        columns = ', '.join(column_names)
        query = text(f"SELECT {columns} FROM {table_name}")
        with self.engine.connect() as connection:
            result = connection.execute(query)
            if result.rowcount == 0:
                return [{'column': col} for col in result.keys()]
            return [dict(zip(result.keys(), row)) for row in result]

    def fetch(self, query: str, params: dict):
        self.logger.info(f"Executing fetch query: {query}\nParams: {params}")
        with self.engine.connect() as connection:
            result = connection.execute(text(query), params)
            self.logger.info(f"Query executed: {query}\nRows fetched: {result.rowcount}.")
            return [dict(zip(result.keys(), row)) for row in result]

    def execute(self, query: str, params: dict):
        self.logger.info(f"Executing query: {query}\nParams: {params}")
        with self.engine.connect() as connection:
            result = connection.execute(text(query), params)
            connection.commit()
            self.logger.info(f"Query executed: {query}\nRows affected: {result.rowcount}")

    def parse_string_or_list(self, input_param: Optional[Union[List[str], str]]) -> Optional[List[str]]:
        if input_param is None:
            return None

        if isinstance(input_param, str):
            return [item.strip() for item in input_param.split(',')]
        elif isinstance(input_param, list):
            return [str(item).strip() for item in input_param]
        else:
            raise TypeError("Parameter must be a list or comma-separated string")

    def _format_query_historico(
            self,
            avg: bool,
            columns: Optional[List[str]] = None,
            ids: Optional[List[str]] = None,
            fecha_ini: Optional[str] = None,
            fecha_fin: Optional[str] = None
    ):
        columns = ", ".join(columns) if columns else "*"
        table_name = "historico_avg" if avg else "historico"
        query = f"SELECT {columns} FROM {table_name}"
        conditions = []

        id_col = 'provincia_id' if avg else 'idema'

        if ids:
            conditions.append(f"{id_col} IN :ids")
        if fecha_ini:
            conditions.append("fecha >= :fecha_ini")
        if fecha_fin:
            conditions.append("fecha <= :fecha_fin")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        params = {}
        if ids:
            params["ids"] = tuple(ids)
        if fecha_ini:
            params["fecha_ini"] = fecha_ini
        if fecha_fin:
            params["fecha_fin"] = fecha_fin

        return query, params

    def get_historico(
            self,
            columns: Optional[Union[List[str], str]] = None,
            idemas: Optional[Union[List[str], str]] = None,
            fecha_ini: Optional[str] = None,
            fecha_fin: Optional[str] = None
    ):
        idemas = self.parse_string_or_list(idemas)
        columns = self.parse_string_or_list(columns)
        query, params = self._format_query_historico(False, columns, idemas, fecha_ini, fecha_fin)
        return self.fetch(query, params)

    def get_historico_average(
            self,
            columns: Optional[Union[List[str], str]] = None,
            provincia_ids: Optional[Union[List[str], str]] = None,
            fecha_ini: Optional[str] = None,
            fecha_fin: Optional[str] = None
    ):
        provincia_ids = self.parse_string_or_list(provincia_ids)
        columns = self.parse_string_or_list(columns)
        query, params = self._format_query_historico(True, columns, provincia_ids, fecha_ini, fecha_fin)
        return self.fetch(query, params)

    def is_empty(self, table_name: str):
        query = text(f"SELECT * FROM {table_name} LIMIT 1")
        with self.engine.connect() as connection:
            result = connection.execute(query)
            return result.fetchone() is None

    def get_earliest_or_latest_historical_date(self, earliest: bool, year: Optional[int] = None):
        table_name = f"historico_{year}" if year else "historico"
        query = text(f"SELECT MIN(fecha) FROM {table_name}") \
            if earliest else text(f"SELECT MAX(fecha) FROM {table_name}")
        with self.engine.connect() as connection:
            result = connection.execute(query)
            if result.rowcount == 0:
                return [{'column': col} for col in result.keys()]
            return result.fetchone()[0]

    def get_earliest_historical_date(self, year: Optional[int] = None) -> datetime.date:
        return self.get_earliest_or_latest_historical_date(True, year)

    def get_latest_historical_date(self, year: Optional[int] = None) -> datetime.date:
        return self.get_earliest_or_latest_historical_date(False, year)

    def historical_exists(self, fecha: str):
        query = text(f"SELECT * FROM historico WHERE fecha = :fecha LIMIT 1")
        with self.engine.connect() as connection:
            result = connection.execute(query, {"fecha": fecha})
            return result.fetchone() is not None

    def table_exists(self, table_name: str):
        query = text(f"SELECT * FROM information_schema.tables WHERE table_name = :table_name")
        with self.engine.connect() as connection:
            result = connection.execute(query, {"table_name": table_name})
            exists = result.fetchone() is not None
            self.logger.info(f"Table {table_name} exists: {exists}")
            return True if exists else False

    def create_table(self, table_name: str, columns: List[str]):
        if self.table_exists(table_name):
            self.logger.info(f"Table {table_name} already exists.")
            return
        query = f"CREATE TABLE {table_name} ({', '.join(columns)})"
        self.execute(query, {})
        self.logger.info(f"Table {table_name} created.")

    def create_historical_table(self, year: int):
        if self.table_exists(f'historico_{year}'):
            self.logger.info(f"Table historico_{year} already exists.")
            return

        query = f"""SELECT create_historical_table(:year)"""
        self.execute(query, {"year": year})
        self.enable_rls(f'historico_{year}')
        self.add_readonly_policy(f'historico_{year}')
        self.add_year_to_historico_view(year)
        self.logger.info(f"Table historico_{year} created and added to view historico.")

    def enable_rls(self, table_name: str):
        query = f"ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY"
        self.execute(query, {})
        self.logger.info(f"RLS enabled for table {table_name}.")

    def add_readonly_policy(self, table_name: str):
        query = "SELECT create_read_only_policy_for_table(:table_name)"
        self.execute(query, {"table_name": table_name})
        self.logger.info(f"Read-only policy added for table {table_name}.")

    def add_year_to_historico_view(self, year: int):
        query = "SELECT create_historico_view(:earliest_year, :latest_year)"

        earliest_year = self.get_earliest_historical_date().year
        latest_year = self.get_latest_historical_date().year

        before = year < earliest_year

        if before:
            self.execute(query, {"earliest_year": year, "latest_year": latest_year})
        else:
            self.execute(query, {"earliest_year": earliest_year, "latest_year": year})

        self.logger.info("Historico view updated.")
