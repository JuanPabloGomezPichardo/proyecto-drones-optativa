# mision.py
from db_connection import get_connection

class Mision:
    def __init__(self, id: int, tipo: str, operador_id: int, estado: str = "pendiente"):
        self.id = id
        self.tipo = tipo
        self.operador_id = operador_id
        self.estado = estado

    @classmethod
    def crear(cls, tipo: str, operador_id: int):
        tipos_validos = ["búsqueda", "suministros", "vigilancia", "mapeo"]
        if tipo.lower() not in tipos_validos:
            raise ValueError("Tipo de misión inválido")
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO misiones (tipo, operador_id, estado) VALUES (%s, %s, 'pendiente')",
                (tipo.lower(), operador_id)
            )
            conn.commit()
            mision_id = cur.lastrowid
            return cls(mision_id, tipo.lower(), operador_id)
        finally:
            cur.close()
            conn.close()

    @classmethod
    def listar_todos(cls):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, tipo, operador_id, estado FROM misiones")
            return [cls(*row) for row in cur.fetchall()]
        finally:
            cur.close()
            conn.close()

    def completar(self):
        self.estado = "completada"
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE misiones SET estado='completada' WHERE id=%s", (self.id,))
        conn.commit()
        cur.close()
        conn.close()