import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

# Read DATABASE_URL from the .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    # Opens a connection to Neon; rows come back as dictionaries
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)