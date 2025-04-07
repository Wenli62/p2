from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

mysql_user = os.environ.get("MYSQL_ROOT_USERNAME")
mysql_pass = os.environ.get("MYSQL_ROOT_PASSWORD")
mysql_host = os.environ.get("MYSQL_HOST")
mysql_port = os.environ.get("MYSQL_PORT")
mysql_db = os.environ.get("MYSQL_DATABASE")
SECRET_KEY = os.environ.get("secret_key")

engine = create_engine(f"mysql://{mysql_user}:{mysql_pass}@{mysql_host}:{mysql_port}/{mysql_db}")

def make_session():
    return sessionmaker(bind=engine)()