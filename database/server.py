import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "vinea123",
    "database": "v1"
}

def get_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print("Database connection error:", e)
        return None
