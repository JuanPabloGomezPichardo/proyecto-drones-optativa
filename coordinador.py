# coordinador.py
from usuario import Usuario
from drone import Drone
from mision import Mision

class Coordinador:
    def __init__(self):
        self.usuario_actual = None

    def login(self, nombre, password):
        self.usuario_actual = Usuario.autenticar(nombre, password)
        return self.usuario_actual is not None

    def es_admin(self):
        return self.usuario_actual and self.usuario_actual.role == "admin"

    def listar_drones(self):
        return Drone.todos()

    def crear_drone(self, modelo):
        if self.es_admin():
            return Drone.crear(modelo)

    def listar_misiones(self):
        return Mision.listar_todos()

    def completar_mision(self, mision_id):
        mision = next((m for m in self.listar_misiones() if m.id == mision_id), None)
        if mision:
            mision.completar()
            return True
        return False

    def asignar_drone_a_mision(self, drone_id, mision_id):
        drone = next((d for d in self.listar_drones() if d.id == drone_id), None)
        if drone and drone.disponible:
            drone.disponible = False
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE drones SET disponible = 0 WHERE id = %s", (drone_id,))
            conn.commit()
            cur.close()
            conn.close()
            return True
        return False