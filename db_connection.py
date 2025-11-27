# db_connection.py
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling

load_dotenv()

config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'juandev123'),
    'database': os.getenv('DB_NAME', 'gestion_drones_db'),
    'autocommit': True
}

try:
    pool = pooling.MySQLConnectionPool(pool_name="drone_pool", pool_size=5, **config)
    print("Base de datos conectada")
except Exception as e:
    print("Error de conexión:", e)
    pool = None

def get_connection():
    if pool:
        return pool.get_connection()
    raise Exception("No hay conexión a BD")