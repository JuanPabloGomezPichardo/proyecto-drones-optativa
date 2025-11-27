# execute.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from coordinador import Coordinador
from drone import Drone
from mision import Mision
from usuario import Usuario
from db_connection import get_connection

class App:
    def __init__(self):
        self.coordinador = Coordinador()
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Drones - Juan Pablo Gómez Pichardo - ISW-25")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0d1117")
        self.root.resizable(True, True)
        self.inicio()

    def limpiar(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def inicio(self):
        self.limpiar()
        tk.Label(self.root, text="SISTEMA DE GESTION DE DRONES", font=("Arial", 32, "bold"), fg="#58a6ff", bg="#0d1117").pack(pady=100)
        tk.Label(self.root, text="Juan Pablo Gómez Pichardo - ISW-25 - 022000396", font=("Arial", 14), fg="#8b949e", bg="#0d1117").pack(pady=10)

        tk.Button(self.root, text="INICIAR SESIÓN", command=self.pantalla_login, width=35, height=3, bg="#238636", fg="white", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Button(self.root, text="REGISTRARSE", command=self.pantalla_registro, width=35, height=3, bg="#1f6feb", fg="white", font=("Arial", 16, "bold")).pack(pady=15)

    def pantalla_login(self):
        self.limpiar()
        tk.Label(self.root, text="INICIAR SESIÓN", font=("Arial", 28, "bold"), fg="#58a6ff", bg="#0d1117").pack(pady=80)
        tk.Label(self.root, text="Usuario:", fg="white", bg="#0d1117", font=("Arial", 14)).pack(pady=10)
        self.entry_user = tk.Entry(self.root, font=("Arial", 14), width=35, justify="center")
        self.entry_user.pack(pady=10)
        # self.entry_user.insert(0, "admin")

        tk.Label(self.root, text="Contraseña:", fg="white", bg="#0d1117", font=("Arial", 14)).pack(pady=10)
        self.entry_pass = tk.Entry(self.root, font=("Arial", 14), width=35, justify="center", show="*")
        self.entry_pass.pack(pady=10)
        # self.entry_pass.insert(0, "admin123")

        tk.Button(self.root, text="INGRESAR", command=self.login, bg="#238636", fg="white", font=("Arial", 16, "bold"), width=30).pack(pady=30)
        tk.Button(self.root, text="Volver", command=self.inicio, bg="#8b949e", fg="white").pack(pady=10)

    def pantalla_registro(self):
        self.limpiar()
        tk.Label(self.root, text="REGISTRARSE", font=("Arial", 28, "bold"), fg="#58a6ff", bg="#0d1117").pack(pady=60)

        tk.Label(self.root, text="Nombre de usuario:", fg="white", bg="#0d1117").pack(pady=10)
        self.reg_user = tk.Entry(self.root, width=35, font=("Arial", 14))
        self.reg_user.pack(pady=10)

        tk.Label(self.root, text="Contraseña:", fg="white", bg="#0d1117").pack(pady=10)
        self.reg_pass = tk.Entry(self.root, width=35, font=("Arial", 14), show="*")
        self.reg_pass.pack(pady=10)

        tk.Label(self.root, text="Selecciona tu rol:", fg="white", bg="#0d1117", font=("Arial", 14)).pack(pady=20)
        self.rol_var = tk.StringVar(value="rescatista")
        roles = [("Administrador", "admin"), ("Operador", "operador"), ("Rescatista", "rescatista")]
        for texto, valor in roles:
            tk.Radiobutton(self.root, text=texto, variable=self.rol_var, value=valor, bg="#0d1117", fg="white", selectcolor="#21262d").pack()

        tk.Button(self.root, text="CREAR CUENTA", command=self.registrar, bg="#1f6feb", fg="white", font=("Arial", 16, "bold")).pack(pady=30)
        tk.Button(self.root, text="Volver", command=self.inicio, bg="#8b949e", fg="white").pack()

    def registrar(self):
        nombre = self.reg_user.get().strip()
        password = self.reg_pass.get()
        rol = self.rol_var.get()
        if not nombre or not password:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        try:
            Usuario.crear(nombre, rol, password)
            messagebox.showinfo("Éxito", f"Usuario {nombre} ({rol}) creado correctamente")
            self.inicio()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def login(self):
        if self.coordinador.login(self.entry_user.get(), self.entry_pass.get()):
            self.menu_principal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def menu_principal(self):
        self.limpiar()
        user = self.coordinador.usuario_actual
        tk.Label(self.root, text=f"Bienvenido {user.nombre}", font=("Arial", 26), fg="#58a6ff", bg="#0d1117").pack(pady=20)
        tk.Label(self.root, text=f"Rol: {user.role.upper()}", font=("Arial", 18), fg="#8b949e", bg="#0d1117").pack(pady=10)

        if user.role == "admin":
            tk.Button(self.root, text="Crear Drone", command=self.crear_drone, width=50, height=2, bg="#238636", fg="white").pack(pady=10)
            tk.Button(self.root, text="Eliminar Drone", command=self.eliminar_drone, width=50, height=2, bg="#da3633", fg="white").pack(pady=10)

        if user.role == "operador":
            tk.Button(self.root, text="Asignar Drone a Misión", command=self.asignar_mision, width=50, height=2, bg="#1f6feb", fg="white").pack(pady=15)

        if user.role == "rescatista":
            tk.Button(self.root, text="Completar Misión", command=self.completar_mision, width=50, height=2, bg="#f0883e", fg="white").pack(pady=15)

        tk.Button(self.root, text="Ver Drones", command=self.ver_drones, width=50, height=2).pack(pady=10)
        tk.Button(self.root, text="Ver Misiones", command=self.ver_misiones, width=50, height=2).pack(pady=10)
        tk.Button(self.root, text="Cerrar Sesión", command=self.inicio, bg="#8b949e", fg="white", height=2).pack(pady=40)

    def ver_drones(self):
        drones = Drone.todos()
        lista = "\n".join([f"ID: {d.id} | {d.modelo} | {'OCUPADO' if not d.disponible else 'DISPONIBLE'}" for d in drones])
        messagebox.showinfo("Drones", lista or "No hay drones registrados")

    def crear_drone(self):
        modelo = simpledialog.askstring("Nuevo Drone", "Modelo del drone:")
        if modelo and modelo.strip():
            Drone.crear(modelo.strip())
            messagebox.showinfo("Éxito", f"Drone {modelo} creado")

    def eliminar_drone(self):
        drones = Drone.todos()
        if not drones:
            messagebox.showinfo("Info", "No hay drones")
            return
        lista = "\n".join([f"{d.id} - {d.modelo}" for d in drones])
        id_elim = simpledialog.askinteger("Eliminar", f"{lista}\n\nID a eliminar:")
        if id_elim:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM drones WHERE id = %s", (id_elim,))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Éxito", "Drone eliminado")

    def asignar_mision(self):
        drones = [d for d in Drone.todos() if d.disponible]
        if not drones:
            messagebox.showwarning("Sin drones", "No hay drones disponibles")
            return
        lista = "\n".join([f"{d.id} - {d.modelo}" for d in drones])
        drone_id = simpledialog.askinteger("Seleccionar Drone", f"{lista}\n\nID del drone:")
        if not drone_id:
            return
        tipo = simpledialog.askstring("Tipo de Misión", "búsqueda / suministros / vigilancia / mapeo").strip().lower()
        if tipo not in ["búsqueda", "suministros", "vigilancia", "mapeo"]:
            messagebox.showerror("Error", "Tipo inválido")
            return

        mision = Mision.crear(tipo, self.coordinador.usuario_actual.id)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE drones SET disponible = 0 WHERE id = %s", (drone_id,))
        conn.commit()
        cur.close()
        conn.close()

        messagebox.showinfo("ÉXITO", f"Misión {tipo.upper()} asignada\nDrone marcado como OCUPADO\nBatería: 100% | Prioridad: ALTA")

    def completar_mision(self):
        misiones = Mision.listar_todos()
        pendientes = [m for m in misiones if m.estado != "completada"]
        if not pendientes:
            messagebox.showinfo("Info", "No hay misiones pendientes")
            return
        lista = "\n".join([f"{m.id} - {m.tipo.upper()}" for m in pendientes])
        mision_id = simpledialog.askinteger("Completar", f"{lista}\n\nID de la misión:")
        if not mision_id:
            return
        mision = next((m for m in pendientes if m.id == mision_id), None)
        if mision:
            mision.completar(self.coordinador.usuario_actual.id)
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE drones SET disponible = 1 WHERE disponible = 0")
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("ÉXITO", f"Misión {mision_id} completada\nDrone liberado")

    def ver_misiones(self):
        misiones = Mision.listar_todos()
        lista = "\n".join([str(m) for m in misiones]) if misiones else "No hay misiones"
        messagebox.showinfo("Misiones", lista)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    App().run()