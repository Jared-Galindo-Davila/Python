import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt

def ventanasistema(fondo_imagen):
    # Datos de ejemplo para mostrar gráficos
    data = {
        'Administracion': [10, 20, 30, 40],
        'Operadores': [15, 25, 35, 45],
        'Jefes': [20, 30, 40, 50]
    }

    # Función para mostrar gráfico de Administración
    def show_administracion():
        df = pd.DataFrame({'Administracion': data['Administracion']})
        df.plot(kind='bar')
        plt.title("Gráfico de Administración")
        plt.ylabel("Valores")
        plt.xlabel("Categorías")
        plt.show()

    # Función para mostrar gráfico de Operadores
    def show_operadores():
        df = pd.DataFrame({'Operadores': data['Operadores']})
        df.plot(kind='bar')
        plt.title("Gráfico de Operadores")
        plt.ylabel("Valores")
        plt.xlabel("Categorías")
        plt.show()

    # Función para mostrar gráfico de Jefes
    def show_jefes():
        df = pd.DataFrame({'Jefes': data['Jefes']})
        df.plot(kind='bar')
        plt.title("Gráfico de Jefes")
        plt.ylabel("Valores")
        plt.xlabel("Categorías")
        plt.show()

    # Crear la ventana principal
    root = tk.Tk()
    root.title("Interfaz de Gestión")

    # Tamaño deseado para las imágenes
    img_width = 100
    img_height = 100

    # Función para cargar y redimensionar imágenes
    def load_image(path):
        img = Image.open(path)
        img = img.resize((img_width, img_height), Image.LANCZOS)  # Redimensionar la imagen
        return ImageTk.PhotoImage(img)

    # Cargar y redimensionar las imágenes
    img_administracion = load_image("admin.png")
    img_operadores = load_image("operador.png")
    img_jefes = load_image("jefess.png")

    # Cargar y aplicar la imagen de fondo
    fondo = Image.open(fondo_imagen)
    fondo = fondo.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
    fondo_img = ImageTk.PhotoImage(fondo)
    fondo_label = tk.Label(root, image=fondo_img)
    fondo_label.place(relwidth=1, relheight=1)

    # Crear un Frame para organizar los botones horizontalmente
    frame = tk.Frame(root, bg='white')  # Ajusta el color de fondo si es necesario
    frame.pack(pady=20)

    # Crear botones para cada opción con imágenes y texto, y organizarlos en el Frame
    btn_administracion = tk.Button(frame, text="Administración", image=img_administracion, compound="top", command=show_administracion)
    btn_operadores = tk.Button(frame, text="Operadores", image=img_operadores, compound="top", command=show_operadores)
    btn_jefes = tk.Button(frame, text="Jefes", image=img_jefes, compound="top", command=show_jefes)

    # Colocar los botones en el Frame de forma horizontal
    btn_administracion.grid(row=0, column=0, padx=10)
    btn_operadores.grid(row=0, column=1, padx=10)
    btn_jefes.grid(row=0, column=2, padx=10)

    # Ejecutar el bucle principal de la interfaz
    root.mainloop()
