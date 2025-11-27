# execute.py
import tkinter as tk
from tkinter import ttk, messagebox
from coordinador import Coordinador
from drone import Drone

class App:
    def __init__(self):
        self.coordinador = Coordinador()
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Drones – Juan Pablo Gómez")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")

        self.crear_login()

    def crear_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="SISTEMA DE DRONES", font=("Arial", 20), bg="#2c3e50", fg="white").pack(pady=50)
        tk.Label(self.root, text="Usuario:", bg="#2c3e50", fg="white").pack()
        self.entry_user = tk.Entry(self.root)
        self.entry_user.pack(pady=5)
        self.entry_user.insert(0, "admin")

        tk.Label(self.root, text="Contraseña:", bg="#2c3e50", fg="white").pack()
        self.entry_pass = tk.Entry(self.root, show="*")
        self.entry_pass.pack(pady=5)
        self.entry_pass.insert(0, "admin123")

        tk.Button(self.root, text="INGRESAR", command=self.login, bg="#e74c3c", fg="white", font=("Arial", 12)).pack(pady=20)

    def login(self):
        if self.coordinador.login(self.entry_user.get(), self.entry_pass.get()):
            messagebox.showinfo("Éxito", f"Bienvenido {self.entry_user.get()}")
            self.menu_principal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def menu_principal(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="MENÚ PRINCIPAL", font=("Arial", 18), bg="#2c3e50", fg="white").pack(pady=20)

        tk.Button(self.root, text="Ver Drones", command=self.ver_drones, width=30, height=2).pack(pady=10)
        tk.Button(self.root, text="Crear Drone", command=self.crear_drone_dialog, width=30, height=2).pack(pady=10)
        tk.Button(self.root, text="Salir", command=self.root.quit, width=30, height=2).pack(pady=50)

    def ver_drones(self):
        drones = self.coordinador.listar_drones()
        texto = "\n".join(str(d) for d in drones) if drones else "No hay drones"
        messagebox.showinfo("Drones Registrados", texto)

    def crear_drone_dialog(self):
        if not self.coordinador.es_admin():
            messagebox.showwarning("Acceso denegado", "Solo admin puede crear drones")
            return
        modelo = tk.simpledialog.askstring("Nuevo Drone", "Modelo del drone:")
        if modelo:
            Drone.crear(modelo)
            messagebox.showinfo("Éxito", f"Drone {modelo} creado")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    App().run()