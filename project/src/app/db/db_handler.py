from sqlalchemy import create_engine
import helpers

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

        self.URL = f"postgresql+psycopg2://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DBNAME}?sslmode=require"
        self.engine = create_engine(self.URL)

