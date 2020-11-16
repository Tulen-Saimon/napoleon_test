from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


SQL_DB_HOST = os.environ.get('SQL_DB_HOST')
SQL_DB_PORT = os.environ.get('SQL_DB_PORT')
SQL_DB_NAME = os.environ.get('SQL_DB_NAME')
SQL_DB_USER = os.environ.get('SQL_DB_USER')
SQL_DB_PASSWORD = os.environ.get('SQL_DB_PASSWORD')
SECRET = os.environ.get('SECRET')