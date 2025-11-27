# coordinador.py
from usuario import Usuario
from drone import Drone
from mision import Mision

class Coordinador:
    def __init__(self):
        self.usuario_actual = None

    def login(self, usuario, password):
        self.usuario_actual = Usuario.autenticar(usuario, password)
        return self.usuario_actual is not None

    def es_admin(self):
        return self.usuario_actual and self.usuario_actual.role == "admin"

    def listar_drones(self):
        return Drone.todos()

    def crear_drone(self, modelo):
        if self.es_admin():
            return Drone.crear(modelo)