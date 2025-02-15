from sqlalchemy import create_engine, text
from src.shared import helpers


class DBHandler:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBHandler, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):

        try:
            self.USER = helpers.get_env_var("DB_USER")
            self.PASSWORD = helpers.get_env_var("DB_PASSWORD")
            self.HOST = helpers.get_env_var("DB_HOST")
            self.PORT = helpers.get_env_var("DB_PORT")
            self.DBNAME = helpers.get_env_var("DB_NAME")
        except KeyError as e:
            raise ValueError(f"Missing environment variable: {str(e)}")

        self.URL = f"postgresql+psycopg2://{self.USER}:{self.PASSWORD}@[{self.HOST}]:{self.PORT}/{self.DBNAME}?sslmode=require"
        self.engine = create_engine(self.URL)

    def insert_data(self, table_name: str, data: dict):
        '''Inserta datos en una tabla de la base de datos'''
        query = text(f"INSERT INTO {table_name} (name) VALUES (:name)")
        with self.engine.connect() as connection:
            connection.execute(query, **data)

    def get_table_data(self, table_name: str):
        '''Consulta de datos de una tabla en la base de datos'''
        query = text(f"SELECT * FROM {table_name}")
        with self.engine.connect() as connection:
            result = connection.execute(query)
            return [{"id": row[0], "name": row[1]} for row in result]
    
    