import os
from dotenv import load_dotenv
import pymysql
import pytest


if 'ENV' in os.environ:
    env_file = os.environ['ENV']
    load_dotenv(env_file)
else:
    load_dotenv()


@pytest.fixture(scope="session")
def setup_db():
    db_settings = {
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT")),
        "user": os.getenv("DB_USERNAME"),
        "password": os.getenv("DB_PASSWORD"),
        "db": os.getenv("DB_NAME"),
        "charset": "utf8"
    }
    conn = pymysql.connect(**db_settings)
    yield conn
    conn.close()
