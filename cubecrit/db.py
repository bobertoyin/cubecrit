"""The database engine."""
from os import environ

from sqlalchemy import create_engine

db = create_engine(environ["DB_ADDRESS"])
