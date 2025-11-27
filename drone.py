# drone.py
from db_connection import get_connection

class Drone:
    def __init__(self, id, modelo, bateria=100, ubicacion="Base central", disponible=True):
        self.id = id
        self.modelo = modelo
        self.bateria = max(0, min(100, bateria))
        self.ubicacion = ubicacion
        self.disponible = disponible

    @classmethod
    def crear(cls, modelo):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO drones (modelo) VALUES (%s)", (modelo,))
        conn.commit()
        drone_id = cur.lastrowid
        cur.close()
        conn.close()
        return cls(drone_id, modelo)

    @classmethod
    def todos(cls):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, modelo, bateria, ubicacion, disponible FROM drones")
        drones = [cls(*row) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return drones

    def __str__(self):
        return f"{self.modelo} – {self.bateria}% – {'Disponible' if self.disponible else 'En misión'}"