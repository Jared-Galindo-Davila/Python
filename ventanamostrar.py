import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sqlite3

# Función para verificar la contraseña y abrir la ventana emergente
def verificar_contrasena():
    contrasena = entrada_contrasena.get()
    if contrasena == "contrasena":  # Cambia "contrasena" por la contraseña que desees
        abrir_ventana_emergente()
        ventana_contrasena.destroy()  # Cierra la ventana de ingreso de contraseña
    else:
        messagebox.showerror("Error", "Contraseña incorrecta")

# Función para actualizar la hora en tiempo real
def actualizar_hora():
    ahora = datetime.now()
    hora_actual = ahora.strftime('%H:%M:%S')
    label_hora.config(text=f"Hora actual: {hora_actual}")
    ventana_emergente.after(1000, actualizar_hora)  # Actualiza cada 1000 ms (1 segundo)

# Función para abrir la ventana emergente con el formulario
def abrir_ventana_emergente():
    global hora_entrada
    hora_entrada = datetime.now()  # Guarda la hora de entrada

    ventana_emergente = tk.Toplevel(ventana)
    ventana_emergente.title("Ventana Emergente con Formulario")
    ventana_emergente.geometry("600x400")  # Aumentar el tamaño de la ventana
    ventana_emergente.configure(bg="#f0f0f0")  # Color de fondo

    # Crear un formulario en la ventana emergente
    tk.Label(ventana_emergente, text="Nombre:", bg="#f0f0f0", font=("Helvetica", 12, "bold"), fg="#ff0000").grid(row=0, column=0, padx=15, pady=15, sticky="e")
    entrada_nombre = tk.Entry(ventana_emergente)
    entrada_nombre.grid(row=0, column=1, padx=15, pady=15, sticky="w")

    tk.Label(ventana_emergente, text="Edad:", bg="#f0f0f0", font=("Helvetica", 12, "bold"), fg="#ff0000").grid(row=1, column=0, padx=15, pady=15, sticky="e")
    entrada_edad = tk.Entry(ventana_emergente)
    entrada_edad.grid(row=1, column=1, padx=15, pady=15, sticky="w")

    tk.Label(ventana_emergente, text="Sexo:", bg="#f0f0f0", font=("Helvetica", 12, "bold"), fg="#ff0000").grid(row=2, column=0, padx=15, pady=15, sticky="e")
    opciones_sexo = tk.StringVar(value="Seleccionar")
    menu_sexo = tk.OptionMenu(ventana_emergente, opciones_sexo, "Masculino", "Femenino", "Otro")
    menu_sexo.grid(row=2, column=1, padx=15, pady=15, sticky="w")

    tk.Label(ventana_emergente, text="Comentarios:", bg="#f0f0f0", font=("Helvetica", 12, "bold"), fg="#ff0000").grid(row=3, column=0, padx=15, pady=15, sticky="ne")
    entrada_comentarios = tk.Text(ventana_emergente, height=6, width=40)
    entrada_comentarios.grid(row=3, column=1, padx=15, pady=15, sticky="w")

    # Etiqueta para mostrar la hora actual
    global label_hora
    label_hora = tk.Label(ventana_emergente, text="", bg="#f0f0f0", font=("Helvetica", 12, "bold"))
    label_hora.grid(row=4, column=0, columnspan=2, pady=20)
    actualizar_hora()  # Iniciar la actualización de la hora

    # Botón para enviar el formulario
    def enviar_formulario():
        hora_salida = datetime.now()  # Guarda la hora de salida
        nombre = entrada_nombre.get()
        edad = entrada_edad.get()
        sexo = opciones_sexo.get()
        comentarios = entrada_comentarios.get("1.0", tk.END).strip()

        # Validar datos
        if not nombre or not edad or sexo == "Seleccionar":
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        # Guardar datos en la base de datos
        conexion = sqlite3.connect("datos_formulario.db")
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO formulario (nombre, edad, sexo, comentarios, hora_entrada, hora_salida)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, edad, sexo, comentarios, hora_entrada.strftime('%Y-%m-%d %H:%M:%S'), hora_salida.strftime('%Y-%m-%d %H:%M:%S')))
        conexion.commit()
        conexion.close()

        # Imprimir los datos del formulario y las horas
        print(f"Nombre: {nombre}")
        print(f"Edad: {edad}")
        print(f"Sexo: {sexo}")
        print(f"Comentarios: {comentarios}")
        print(f"Hora de entrada: {hora_entrada.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Hora de salida: {hora_salida.strftime('%Y-%m-%d %H:%M:%S')}")

        messagebox.showinfo("Formulario Enviado", "¡Formulario enviado con éxito!")
        ventana_emergente.destroy()  # Cierra la ventana emergente

    btn_enviar = tk.Button(ventana_emergente, text="Enviar", command=enviar_formulario, bg="#007bff", fg="#ffffff", font=("Helvetica", 12, "bold"))
    btn_enviar.grid(row=5, column=1, pady=20, sticky="e")

# Función para abrir la ventana de ingreso de contraseña
def abrir_ventana_contrasena():
    global ventana_contrasena
    ventana_contrasena = tk.Toplevel(ventana)
    ventana_contrasena.title("Ingreso de Contraseña")
    ventana_contrasena.geometry("400x200")  # Aumentar el tamaño de la ventana
    ventana_contrasena.configure(bg="#f0f0f0")  # Color de fondo

    tk.Label(ventana_contrasena, text="Ingrese la contraseña:", bg="#f0f0f0", font=("Helvetica", 12, "bold"), fg="#ff0000").pack(pady=20)

    global entrada_contrasena
    entrada_contrasena = tk.Entry(ventana_contrasena, show="*")
    entrada_contrasena.pack(pady=10)

    btn_confirmar = tk.Button(ventana_contrasena, text="Confirmar", command=verificar_contrasena, bg="#007bff", fg="#ffffff", font=("Helvetica", 12, "bold"))
    btn_confirmar.pack(pady=20)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Ventana Principal")
ventana.geometry("600x400")  # Aumentar el tamaño de la ventana
ventana.configure(bg="#f0f0f0")  # Color de fondo

# Crear un botón en la ventana principal para abrir la ventana de ingreso de contraseña
btn_abrir_contrasena = tk.Button(ventana, text="Abrir Ventana Emergente", command=abrir_ventana_contrasena, bg="#007bff", fg="#ffffff", font=("Helvetica", 12, "bold"))
btn_abrir_contrasena.pack(pady=30)

# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()