import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read variables from the environment
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        # print("Connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection 

# Use variables loaded from .env
connection = create_connection(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
