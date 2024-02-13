from os import environ

from sqlalchemy import create_engine

db = create_engine(
    f"postgresql://cubecrit:{environ['DB_PASSWORD']}@{environ['DB_ADDRESS']}/cubecrit"
)
