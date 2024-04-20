"""The database engine."""
from os import environ

from sqlalchemy import create_engine

db = create_engine(
    f"postgresql://cubecrit:{environ.get('DB_PASSWORD')}@{environ.get('DB_ADDRESS')}/cubecrit"
)
