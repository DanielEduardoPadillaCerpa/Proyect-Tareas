import tkinter as tk
from tkinter import ttk, messagebox
import json
import mysql.connector

# Clase de gestión de tareas
class TaskManager:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="gestion_tareas"
        )
        self.cursor = self.db.cursor()
        
    def add_task(self, title, description):
        sql = "INSERT INTO tareas (titulo, descripcion, completada) VALUES (%s, %s, %s)"
        values = (title, description, False)
        self.cursor.execute(sql, values)
        self.db.commit()

    def list_tasks(self):
        self.cursor.execute("SELECT id, titulo, descripcion, completada FROM tareas")
        return self.cursor.fetchall()
    
    def complete_task(self, task_id):
        sql = "UPDATE tareas SET completada = %s WHERE id = %s"
        values = (True, task_id)
        self.cursor.execute(sql, values)
        self.db.commit()

    def delete_task(self, task_id):
        sql = "DELETE FROM tareas WHERE id = %s"
        self.cursor.execute(sql, (task_id,))
        self.db.commit()

    def save_tasks(self, filename):
        tasks = self.list_tasks()
        with open(filename, 'w') as file:
            json.dump(tasks, file)

    def load_tasks(self, filename):
        with open(filename, 'r') as file:
            tasks = json.load(file)
            for task in tasks:
                self.add_task(task[1], task[2])  # title, description

# Clase de ventana de inicio de sesión
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("300x200")
        self.root.configure(bg="#003366")  # Azul oscuro
        self.root.resizable(False, False)  # Desactivar la opción de maximizar
        self.setup_ui()

    def setup_ui(self):
        self.label_username = ttk.Label(self.root, text="Usuario:", background="#003366", foreground="white", font=("Arial", 12, "bold"))
        self.label_username.pack(pady=5)
        self.entry_username = ttk.Entry(self.root)
        self.entry_username.pack(pady=5)

        self.label_password = ttk.Label(self.root, text="Contraseña:", background="#003366", foreground="white", font=("Arial", 12, "bold"))
        self.label_password.pack(pady=5)
        self.entry_password = ttk.Entry(self.root, show="*")
        self.entry_password.pack(pady=5)

        self.login_button = tk.Button(self.root, text="Iniciar Sesión", command=self.login, bg="#F44336", fg="white", font=("Arial", 10, "bold"))  # Botón rojo
        self.login_button.pack(pady=20)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        # Aquí deberías validar el usuario y la contraseña
        if username == "Daniel" and password == "12345":  # Ejemplo de validación, la o las personas que esten utilizando este programa podran cambiar esta parte
            self.root.destroy()  # Cierra la ventana de inicio de sesión
            self.open_task_app()  # Abre la aplicación de gestión de tareas
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def open_task_app(self):
        task_root = tk.Tk()
        task_app = TaskApp(task_root)
        task_root.mainloop()

# Clase de gestión de tareas
class TaskApp:
    def __init__(self, root):
        self.manager = TaskManager()

        self.root = root
        self.root.title("Gestión de Tareas")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.setup_styles()
        self.setup_header()
        self.setup_input_fields()
        self.setup_buttons()
        self.setup_task_list()
        self.setup_action_buttons()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 10, "bold"), padding=5)
        style.configure("TEntry", font=("Arial", 12))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

    def setup_header(self):
        self.header_frame = tk.Frame(self.root, bg="#0078D7", height=50)
        self.header_frame.pack(fill=tk.X)
        self.title_label = ttk.Label(self.header_frame, text="Gestión de Tareas", font=("Arial", 18, "bold"), foreground="white", background="#0078D7")
        self.title_label.pack(pady=10)
        self.logout_button = tk.Button(self.header_frame, text="Cerrar Sesión", bg ="#F44336", fg="white", font=("Arial", 10, "bold"), command=self.logout)
        self.logout_button.pack(side=tk.RIGHT, padx=10)

    def setup_input_fields(self):
        self.title_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.title_frame.pack(pady=5)

        self.title_label = ttk.Label(self.title_frame, text="Título:")
        self.title_label.grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(self.title_frame, width=50)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        self.desc_label = ttk.Label(self.title_frame, text="Descripción:")
        self.desc_label.grid(row=1, column=0, padx=5, pady=5)
        self.desc_entry = ttk.Entry(self.title_frame, width=50)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)

    def setup_buttons(self):
        self.button_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(self.button_frame, text="Agregar Tarea", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=self.add_task)
        self.add_button.grid(row=0, column=0, padx=5)

        self.list_button = tk.Button(self.button_frame, text="Listar Tareas", bg="#2196F3", fg="white", font=("Arial", 10, "bold"), command=self.update_task_list)
        self.list_button.grid(row=0, column=1, padx=5)

        self.save_button = tk.Button(self.button_frame, text="Guardar Tareas", bg="#FFC107", fg="black", font=("Arial", 10, "bold"), command=self.save_tasks)
        self.save_button.grid(row=0, column=2, padx=5)

        self.load_button = tk.Button(self.button_frame, text="Cargar Tareas", bg="#FF5722", fg="white", font=("Arial", 10, "bold"), command=self.load_tasks)
        self.load_button.grid(row=0, column=3, padx=5)

    def setup_task_list(self):
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=("Número", "Título", "Descripción", "Estado"), show="headings")
        self.tree.heading("Número", text="Número")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Estado", text="Estado")
        self.tree.column("Número", width=50, anchor=tk.CENTER)
        self.tree.column("Título", width=150, anchor=tk.W)
        self.tree.column("Descripción", width=250, anchor=tk.W)
        self.tree.column("Estado", width=100, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)

    def setup_action_buttons(self):
        self.action_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.action_frame.pack(pady=10)

        self.complete_button = tk.Button(self.action_frame, text="Completar Tarea", bg="#8BC34A", fg="white", font=("Arial", 10, "bold"), command=self.complete_task)
        self.complete_button.grid(row=0, column=0, padx=10)

        self.delete_button = tk.Button(self.action_frame, text="Eliminar Tarea", bg="#F44336", fg="white", font=("Arial", 10, "bold"), command=self.delete_task)
        self.delete_button.grid(row=0, column=1, padx=10)

    def add_task(self):
        title = self.title_entry.get()
        description = self.desc_entry.get()
        if title and description:
            self.manager.add_task(title, description)
            self.title_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.update_task_list()
        else:
            messagebox.showwarning("Error", "Debe ingresar un título y una descripción")

    def complete_task(self):
        try:
            selected_item = self.tree.selection()[0]
            task_id = self.tree.item(selected_item)["values"][0]
            self.manager.complete_task(task_id)
            self.update_task_list()
        except IndexError:
            messagebox.showwarning("Error", "Debe seleccionar una tarea")

    def delete_task(self):
        try:
            selected_item = self.tree.selection()[0]
            task_id = self.tree.item(selected_item)["values"][0]
            self.manager.delete_task(task_id)
            self.update_task_list()
        except IndexError:
            messagebox.showwarning("Error", "Debe seleccionar una tarea")

    def save_tasks(self):
        filename = "tareas.json"
        self.manager.save_tasks(filename)
        messagebox.showinfo("Info", f"Tareas guardadas exitosamente en {filename}")

    def load_tasks(self):
        filename = "tareas.json"
        self.manager.load_tasks(filename)
        self.update_task_list()
        messagebox.showinfo("Info", f"Tareas cargadas exitosamente desde {filename}")

    def update_task_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, task in enumerate(self.manager.list_tasks()):
            status = "Completada" if task[3] else "Pendiente"
            self.tree.insert("", "end", values=(task[0], task[1], task[2], status))

    def logout(self):
        self.root.destroy()  # Cierra la ventana de gestión de tareas
        self.open_login_window()  # Abre la ventana de inicio de sesión

    def open_login_window(self):
        login_root = tk.Tk()
        login_app = LoginWindow(login_root)
        login_root.mainloop()

# Ejecutar aplicativo
if __name__ == "__main__":
    login_root = tk.Tk()
    login_app = LoginWindow(login_root)
    login_root.mainloop()