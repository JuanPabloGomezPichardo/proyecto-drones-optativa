# mision.py
from db_connection import get_connection

class Mision:
    def __init__(self, id, tipo, operador_id, estado="pendiente"):
        self.id = id
        self.tipo = tipo
        self.operador_id = operador_id
        self.estado = estado

    @classmethod
    def crear(cls, tipo, operador_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO misiones (tipo, operador_id) VALUES (%s, %s)", (tipo, operador_id))
        conn.commit()
        mision_id = cur.lastrowid
        cur.close()
        conn.close()
        return cls(mision_id, tipo, operador_id)