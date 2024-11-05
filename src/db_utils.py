import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up the database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
        return conn
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        raise

# Get the user's connection mode by Cognito ID
def get_user_connection_mode(cognito_sub):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            query = """
            SELECT connection_mode FROM "user"
            WHERE cognito_sub = %s
            """
            cursor.execute(query, (cognito_sub,))
            result = cursor.fetchone()
            if result:
                return result[0]  # connection_mode
            else:
                raise ValueError("User not found in the database")
    finally:
        conn.close()
