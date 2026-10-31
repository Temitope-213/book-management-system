import psycopg
from psycopg.rows import dict_row

from app.core.config import DATABASE_URL


def get_connection():
    # Opens a connection to Neon; rows come back as dictionaries
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)