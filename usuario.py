# usuario.py
import hashlib
from db_connection import get_connection

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

class Usuario:
    def __init__(self, id: int, nombre: str, role: str):
        self.id = id
        self.nombre = nombre
        self.role = role  # admin, operador, rescatista

    @classmethod
    def crear(cls, nombre: str, role: str, password: str):
        if role not in ["admin", "operador", "rescatista"]:
            raise ValueError("Rol inválido")
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO usuarios (nombre, role, password) VALUES (%s, %s, %s)",
                (nombre, role, hash_password(password))
            )
            conn.commit()
            user_id = cur.lastrowid
            cur.close()
            conn.close()
            return cls(user_id, nombre, role)
        except Exception as e:
            raise ValueError(f"Error al crear usuario: {str(e)}")

    @classmethod
    def autenticar(cls, nombre: str, password: str):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, nombre, role FROM usuarios WHERE nombre=%s AND password=%s",
                (nombre, hash_password(password))
            )
            row = cur.fetchone()
            if row:
                return cls(row[0], row[1], row[2])
            return None
        finally:
            cur.close()
            conn.close()

    def __str__(self):
        return f"{self.nombre} ({self.role})"