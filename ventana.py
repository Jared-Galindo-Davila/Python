import tkinter as tk
from tkinter import messagebox

# Función para abrir la ventana emergente si la contraseña es correcta
def verificar_contrasena():
    contrasena = entrada_contrasena.get()
    if contrasena == "contrasena":  # Cambia "mi_password" por la contraseña que desees
        abrir_ventana_emergente()
        ventana_contrasena.destroy()  # Cierra la ventana de ingreso de contraseña
    else:
        messagebox.showerror("Error", "Contraseña incorrecta")

# Función para abrir la ventana emergente
def abrir_ventana_emergente():
    ventana_emergente = tk.Toplevel(ventana)
    ventana_emergente.title("Ventana Emergente")
    ventana_emergente.geometry("200x100")

    # Crear un botón en la ventana emergente para cerrarla
    btn_cerrar = tk.Button(ventana_emergente, text="Cerrar", command=ventana_emergente.destroy)
    btn_cerrar.pack(pady=20)

# Función para abrir la ventana de ingreso de contraseña
def abrir_ventana_contrasena():
    global ventana_contrasena
    ventana_contrasena = tk.Toplevel(ventana)
    ventana_contrasena.title("Ingreso de Contraseña")
    ventana_contrasena.geometry("300x150")

    # Crear una etiqueta, un campo de entrada y un botón en la ventana de ingreso de contraseña
    etiqueta = tk.Label(ventana_contrasena, text="Ingrese la contraseña:")
    etiqueta.pack(pady=10)

    global entrada_contrasena
    entrada_contrasena = tk.Entry(ventana_contrasena, show="*")
    entrada_contrasena.pack(pady=10)

    btn_confirmar = tk.Button(ventana_contrasena, text="Confirmar", command=verificar_contrasena)
    btn_confirmar.pack(pady=10)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Ventana Principal")
ventana.geometry("400x300")

# Crear un botón en la ventana principal para abrir la ventana de ingreso de contraseña
btn_abrir_contrasena = tk.Button(ventana, text="Abrir Ventana Emergente", command=abrir_ventana_contrasena)
btn_abrir_contrasena.pack(pady=20)

# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()