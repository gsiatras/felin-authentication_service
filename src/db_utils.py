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


def get_user_id_by_sub(user_sub):
    """Retrieve the user_id from the user table based on the user's Cognito sub."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT user_id FROM "user" WHERE cognito_sub = %s
            """
            cursor.execute(query, (user_sub,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                raise ValueError("User with the provided Cognito sub not found.")
    finally:
        connection.close()


def update_user_connection_mode(user_id, new_mode):
    """Update the connection_mode in the user table based on user_id."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                UPDATE "user" SET connection_mode = %s WHERE user_id = %s
            """
            cursor.execute(
                query,
                (new_mode, user_id)
            )
            connection.commit()
    finally:
        connection.close()


def upsert_trader(user_id, trader_data):
    """Insert or update the trader entry based on user_id."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Check if the user already exists in the trader table
            cursor.execute("SELECT trader_type FROM trader WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()

            if result:
                # Update the existing trader entry
                cursor.execute("""
                    UPDATE trader SET
                        name = %s,
                        afm = %s,
                        address = %s,
                        occupation = %s,
                        zipcode = %s,
                        city = %s,
                        phone1 = %s,
                        trader_type = 'both'
                    WHERE user_id = %s
                """, (
                    trader_data['name'],
                    trader_data['afm'],
                    trader_data['address'],
                    trader_data['occupation'],
                    trader_data['zipcode'],
                    trader_data['city'],
                    trader_data['phone1'],
                    user_id
                ))
                connection.commit()
                return 'both'
            else:
                # Insert a new trader entry with trader_type as 'supplier'
                cursor.execute("""
                    INSERT INTO trader (user_id, name, afm, address, occupation, zipcode, city, phone1, trader_type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'supplier')
                """, (
                    user_id,
                    trader_data['name'],
                    trader_data['afm'],
                    trader_data['address'],
                    trader_data['occupation'],
                    trader_data['zipcode'],
                    trader_data['city'],
                    trader_data['phone1']
                ))
                connection.commit()
                return 'supplier'
    finally:
        connection.close()