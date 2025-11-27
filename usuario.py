# usuario.py
import hashlib
from db_connection import get_connection

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

class Usuario:
    def __init__(self, id, nombre, role):
        self.id = id
        self.nombre = nombre
        self.role = role

    @classmethod
    def autenticar(cls, nombre, password):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, role FROM usuarios WHERE nombre=%s AND password=%s",
                    (nombre, hash_password(password)))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return cls(row[0], row[1], row[2]) if row else None

    def __str__(self):
        return f"{self.nombre} ({self.role})"