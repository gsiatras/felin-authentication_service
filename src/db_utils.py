import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_connection():
    """Establish a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
        return conn
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        raise
