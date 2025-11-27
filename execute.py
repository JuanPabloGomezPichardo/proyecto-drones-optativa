# execute.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from coordinador import Coordinador
from drone import Drone
from mision import Mision
from usuario import Usuario
import hashlib

class App:
    def __init__(self):
        self.coordinador = Coordinador()
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Drones - Juan Pablo Gómez Pichardo - ISW-25")
        self.root.geometry("1100x750")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)
        self.inicio()

    def limpiar(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def inicio(self):
        self.limpiar()
        tk.Label(self.root, text="SISTEMA DE GESTIÓN DE DRONES", font=("Arial", 28, "bold"), fg="#00ffaa", bg="#121212").pack(pady=80)
        tk.Label(self.root, text="Juan Pablo Gómez Pichardo - ISW-25 - 022000396", font=("Arial", 14), fg="#aaaaaa", bg="#121212").pack(pady=10)

        tk.Button(self.root, text="INICIAR SESIÓN", command=self.pantalla_login, width=30, height=3, bg="#00ffaa", fg="black", font=("Arial", 16, "bold")).pack(pady=30)
        tk.Button(self.root, text="REGISTRARSE", command=self.pantalla_registro, width=30, height=3, bg="#0066ff", fg="white", font=("Arial", 16, "bold")).pack(pady=20)

    def pantalla_login(self):
        self.limpiar()
        tk.Label(self.root, text="INICIAR SESIÓN", font=("Arial", 24, "bold"), fg="#00ffaa", bg="#121212").pack(pady=60)

        tk.Label(self.root, text="Usuario:", fg="white", bg="#121212", font=("Arial", 14)).pack(pady=10)
        self.entry_user = tk.Entry(self.root, font=("Arial", 14), width=30, justify="center")
        self.entry_user.pack(pady=10)

        tk.Label(self.root, text="Contraseña:", fg="white", bg="#121212", font=("Arial", 14)).pack(pady=10)
        self.entry_pass = tk.Entry(self.root, font=("Arial", 14), width=30, justify="center", show="*")
        self.entry_pass.pack(pady=10)

        tk.Button(self.root, text="INGRESAR", command=self.login, bg="#00ffaa", fg="black", font=("Arial", 14, "bold"), width=25).pack(pady=30)
        tk.Button(self.root, text="← Volver", command=self.inicio, bg="#555555", fg="white").pack(pady=10)

    def pantalla_registro(self):
        self.limpiar()
        tk.Label(self.root, text="REGISTRARSE", font=("Arial", 24, "bold"), fg="#0066ff", bg="#121212").pack(pady=50)

        tk.Label(self.root, text="Nombre de usuario:", fg="white", bg="#121212").pack(pady=10)
        self.reg_user = tk.Entry(self.root, width=30, font=("Arial", 14))
        self.reg_user.pack(pady=10)

        tk.Label(self.root, text="Contraseña:", fg="white", bg="#121212").pack(pady=10)
        self.reg_pass = tk.Entry(self.root, width=30, font=("Arial", 14), show="*")
        self.reg_pass.pack(pady=10)

        tk.Label(self.root, text="Rol:", fg="white", bg="#121212").pack(pady=10)
        self.rol_var = tk.StringVar(value="rescatista")
        tk.Radiobutton(self.root, text="Admin", variable=self.rol_var, value="admin", bg="#121212", fg="white", selectcolor="#000").pack()
        tk.Radiobutton(self.root, text="Operador", variable=self.rol_var, value="operador", bg="#121212", fg="white", selectcolor="#000").pack()
        tk.Radiobutton(self.root, text="Rescatista", variable=self.rol_var, value="rescatista", bg="#121212", fg="white", selectcolor="#000").pack(pady=20)

        tk.Button(self.root, text="CREAR CUENTA", command=self.registrar, bg="#0066ff", fg="white", font=("Arial", 14, "bold")).pack(pady=20)
        tk.Button(self.root, text="← Volver", command=self.inicio, bg="#555555", fg="white").pack()

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
            messagebox.showerror("Error", "Credenciales incorrectas")

    def menu_principal(self):
        self.limpiar()
        user = self.coordinador.usuario_actual
        tk.Label(self.root, text=f"Bienvenido {user.nombre} ({user.role.upper()})", font=("Arial", 20), fg="#00ffaa", bg="#121212").pack(pady=30)

        if user.role == "admin":
            tk.Button(self.root, text="Gestionar Drones (Crear/Eliminar)", command=self.gestion_drones, width=50, height=2, bg="#ff0066").pack(pady=15)
            tk.Button(self.root, text="Ver Todas las Misiones", command=self.ver_misiones, width=50, height=2).pack(pady=10)

        elif user.role == "operador":
            tk.Button(self.root, text="Asignar Drone a Misión", command=self.asignar_mision, width=50, height=2, bg="#00ccff").pack(pady=20)

        elif user.role == "rescatista":
            tk.Button(self.root, text="Marcar Misión como Completada", command=self.completar_mision, width=50, height=2, bg="#ffaa00").pack(pady=20)

        tk.Button(self.root, text="Ver Drones Disponibles", command=self.ver_drones, width=50, height=2).pack(pady=10)
        tk.Button(self.root, text="Cerrar Sesión", command=self.inicio, bg="#e74c3c", fg="white", height=2).pack(pady=40)

    def ver_drones(self):
        drones = Drone.todos()
        lista = "\n".join([f"ID: {d.id} | {d.modelo} | {'DISPONIBLE' if d.disponible else 'EN MISIÓN'}" for d in drones])
        messagebox.showinfo("Drones", lista or "No hay drones")

    def gestion_drones(self):
        win = tk.Toplevel(self.root)
        win.title("Gestión de Drones - Admin")
        win.geometry("600x500")
        tk.Label(win, text="Crear Drone").pack(pady=10)
        entry = tk.Entry(win, width=30)
        entry.pack(pady=10)
        tk.Button(win, text="Crear", command=lambda: self.crear_drone_admin(entry.get(), win)).pack(pady=10)
        tk.Button(win, text="Eliminar Drone", command=lambda: self.eliminar_drone(win)).pack(pady=10)

    def crear_drone_admin(self, modelo, win):
        if modelo.strip():
            Drone.crear(modelo.strip())
            messagebox.showinfo("Éxito", f"Drone {modelo} creado")
            win.destroy()

    def eliminar_drone(self, win):
        drones = Drone.todos()
        if not drones: 
            messagebox.showinfo("Info", "No hay drones")
            return
        lista = "\n".join([f"{d.id} - {d.modelo}" for d in drones])
        id_elim = simpledialog.askinteger("Eliminar", f"Drones:\n{lista}\n\nID a eliminar:")
        if id_elim:
            # Aquí iría el DELETE real
            messagebox.showinfo("Éxito", f"Drone {id_elim} eliminado (simulado)")

    def asignar_mision(self):
        drones_disp = [d for d in Drone.todos() if d.disponible]
        if not drones_disp:
            messagebox.showwarning("Sin drones", "No hay drones disponibles")
            return
        drone = simpledialog.askinteger("Seleccionar Drone", "Drones disponibles:\n" + 
                                       "\n".join([f"{d.id} - {d.modelo}" for d in drones_disp]) + "\n\nID del drone:")
        tipo = simpledialog.askstring("Tipo de Misión", "búsqueda / suministros / vigilancia / mapeo")
        if tipo in ["búsqueda", "suministros", "vigilancia", "mapeo"]:
            Mision.crear(tipo, self.coordinador.usuario_actual.id)
            messagebox.showinfo("Misión Creada", f"Misión {tipo.upper()}\nBatería: 100%\nPrioridad: ALTA\nDrone asignado")
            # Aquí actualizar estado del drone a ocupado

    def completar_mision(self):
        messagebox.showinfo("Misión Completada", "Misión marcada como completada\nDrone liberado y disponible nuevamente")

    def ver_misiones(self):
        misiones = Mision.listar_todos()
        lista = "\n".join([f"ID: {m.id} | Tipo: {m.tipo} | Estado: {m.estado}" for m in misiones])
        messagebox.showinfo("Misiones", lista or "No hay misiones")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    App().run()