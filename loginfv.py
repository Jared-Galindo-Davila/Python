import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from mtcnn.mtcnn import MTCNN
import numpy as np
import speech_recognition as sr

# Función para mostrar gráficos
def ventanasistema(fondo_imagen):
    # Datos de ejemplo para mostrar gráficos
    data = {
        'Administracion': [10, 20, 30, 40],
        'Operadores': [15, 25, 35, 45],
        'Jefes': [20, 30, 40, 50]
    }

    def show_administracion():
        df = pd.DataFrame({'Administracion': data['Administracion']})
        df.plot(kind='bar')
        plt.title("Gráfico de Administración")
        plt.ylabel("Valores")
        plt.xlabel("Categorías")
        plt.show()

    def show_operadores():
        df = pd.DataFrame({'Operadores': data['Operadores']})
        df.plot(kind='bar')
        plt.title("Gráfico de Operadores")
        plt.ylabel("Valores")
        plt.xlabel("Categorías")
        plt.show()

    def show_jefes():
        df = pd.DataFrame({'Jefes': data['Jefes']})
        df.plot(kind='bar')
        plt.title("Gráfico de Jefes")
        plt.ylabel("Valores")
        plt.xlabel("Categorías")
        plt.show()

    def cerrar_sesion():
        root.destroy()
        pantalla.deiconify()

    root = tk.Tk()
    root.title("Interfaz de Gestión")
    root.geometry("650x750")

    img_width = 100
    img_height = 100

    def load_image(path):
        try:
            img = Image.open(path)
            img = img.resize((img_width, img_height), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except FileNotFoundError:
            print(f"Error: La imagen {path} no se encuentra.")
            return None

    img_administracion = load_image("admin.png")
    img_operadores = load_image("operador.png")
    img_jefes = load_image("jefess.png")

    fondo = Image.open(fondo_imagen)
    fondo = fondo.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
    fondo_img = ImageTk.PhotoImage(fondo)
    fondo_label = tk.Label(root, image=fondo_img)
    fondo_label.place(relwidth=1, relheight=1)

    frame = tk.Frame(root, bg='white')
    frame.pack(pady=20)

    btn_administracion = tk.Button(frame, text="Administración", image=img_administracion, compound="top", command=show_administracion)
    btn_operadores = tk.Button(frame, text="Operadores", image=img_operadores, compound="top", command=show_operadores)
    btn_jefes = tk.Button(frame, text="Jefes", image=img_jefes, compound="top", command=show_jefes)

    btn_administracion.grid(row=0, column=0, padx=10)
    btn_operadores.grid(row=0, column=1, padx=10)
    btn_jefes.grid(row=0, column=2, padx=10)

    cerrar_sesion_btn = tk.Button(root, text="Cerrar Sesión", command=cerrar_sesion, font=("Helvetica", 12), bg="#f44336", fg="white")
    cerrar_sesion_btn.pack(pady=20)

    root.mainloop()

# Función para fondo de pantalla
def cargar_fondo(pantalla, imagen):
    def actualizar_fondo(event=None):
        img = Image.open(imagen)
        img = img.resize((pantalla.winfo_width(), pantalla.winfo_height()), Image.LANCZOS)
        img_fondo = ImageTk.PhotoImage(img)
        fondo.config(image=img_fondo)
        fondo.image = img_fondo

    fondo = tk.Label(pantalla)
    fondo.place(x=0, y=0, relwidth=1, relheight=1)
    actualizar_fondo()
    pantalla.bind('<Configure>', actualizar_fondo)

# Funciones de registro y login
def mostrar_mensaje(titulo, mensaje, tipo="info"):
    if tipo == "info":
        messagebox.showinfo(titulo, mensaje)
    elif tipo == "error":
        messagebox.showerror(titulo, mensaje)
    elif tipo == "warning":
        messagebox.showwarning(titulo, mensaje)

def registrar_usuario():
    usuario_info = usuario.get()
    contra_info = contra.get()
    with open(usuario_info + ".txt", "w") as archivo:
        archivo.write(contra_info)
    usuario_entrada.delete(0, tk.END)
    contra_entrada.delete(0, tk.END)
    mostrar_mensaje("Registro Exitoso", "Usuario registrado correctamente")

def registro_facial():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Registro Facial', frame)
        if cv2.waitKey(1) == 27:
            break
    usuario_img = usuario.get()
    cv2.imwrite(usuario_img + ".jpg", frame)
    cap.release()
    cv2.destroyAllWindows()

    def reg_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1, y1, ancho, alto = lista_resultados[i]['box']
            x2, y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i + 1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg, (150, 200), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(usuario_img + ".jpg", cara_reg)
            pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = usuario_img + ".jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    reg_rostro(img, caras)

def reconocimiento_voz(mensaje):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        mostrar_mensaje("Reconocimiento de Voz", mensaje)
        audio = r.listen(source)
        try:
            texto = r.recognize_google(audio)
            return texto
        except sr.UnknownValueError:
            mostrar_mensaje("Error", "No se entendió el audio", "error")
            return None
        except sr.RequestError:
            mostrar_mensaje("Error", "Error al solicitar resultados", "error")
            return None

def registrar_usuario_voz():
    texto = reconocimiento_voz("Por favor, diga su nombre de usuario")
    if texto:
        usuario.set(texto)
    texto = reconocimiento_voz("Por favor, diga su contraseña")
    if texto:
        contra.set(texto)
    registrar_usuario()

def login_usuario_voz():
    texto = reconocimiento_voz("Por favor, diga su nombre de usuario")
    if texto:
        verificacion_usuario.set(texto)
    texto = reconocimiento_voz("Por favor, diga su contraseña")
    if texto:
        verificacion_contra.set(texto)
    verificacion_login()
    
def login_facial():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Login Facial', frame)
        if cv2.waitKey(1) == 27:
            break
    usuario_login = verificacion_usuario.get()
    cv2.imwrite(usuario_login + "LOG.jpg", frame)
    cap.release()
    cv2.destroyAllWindows()

    def log_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1, y1, ancho, alto = lista_resultados[i]['box']
            x2, y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i + 1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg, (150, 200), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(usuario_login + "LOG.jpg", cara_reg)
            pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = usuario_login + "LOG.jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    log_rostro(img, caras)

    def orb_sim(img1, img2):
        orb = cv2.ORB_create()
        kpa, descr_a = orb.detectAndCompute(img1, None)
        kpb, descr_b = orb.detectAndCompute(img2, None)
        comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = comp.match(descr_a, descr_b)
        regiones_similares = [i for i in matches if i.distance < 70]
        if len(matches) == 0:
            return 0
        return len(regiones_similares) / len(matches)

    im_archivos = os.listdir()
    if usuario_login + ".jpg" in im_archivos:
        rostro_reg = cv2.imread(usuario_login + ".jpg", 0)
        rostro_log = cv2.imread(usuario_login + "LOG.jpg", 0)
        similitud = orb_sim(rostro_reg, rostro_log)
        if similitud >= 0.98:
            iniciar_sesion()
        else:
            Label(pantalla2, text="Incompatibilidad de rostros", fg="red", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)
    else:
        Label(pantalla2, text="Usuario no encontrado", fg="red", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)

def registro():
    global usuario
    global contra
    global usuario_entrada
    global contra_entrada
    global pantalla1
    pantalla1 = tk.Toplevel(pantalla)
    pantalla1.title("Registro")
    pantalla1.geometry("400x350")
    cargar_fondo(pantalla1, 'img/fondo.jpg')
    usuario = tk.StringVar()
    contra = tk.StringVar()
    tk.Label(pantalla1, text="Usuario *", font=("Helvetica", 10), bg="#f0f0f0").pack(pady=5)
    usuario_entrada = tk.Entry(pantalla1, textvariable=usuario, font=("Helvetica", 10))
    usuario_entrada.pack(pady=5)
    tk.Label(pantalla1, text="Contraseña *", font=("Helvetica", 10), bg="#f0f0f0").pack(pady=5)
    contra_entrada = tk.Entry(pantalla1, textvariable=contra, show="*", font=("Helvetica", 10))
    contra_entrada.pack(pady=5)
    tk.Button(pantalla1, text="Registro Tradicional", width=20, height=2, command=registrar_usuario, font=("Helvetica", 10), bg="#4CAF50", fg="white").pack(pady=10)
    tk.Button(pantalla1, text="Registro Facial", width=20, height=2, command=registro_facial, font=("Helvetica", 10), bg="#2196F3", fg="white").pack(pady=10)
    tk.Button(pantalla1, text="Registro por Voz", width=20, height=2, command=registrar_usuario_voz, font=("Helvetica", 10), bg="#FF5722", fg="white").pack(pady=10)

def verificacion_login():
    log_usuario = verificacion_usuario.get()
    log_contra = verificacion_contra.get()
    try:
        with open(log_usuario + ".txt", "r") as archivo:
            almacen_contra = archivo.read()
            if almacen_contra == log_contra:
                mostrar_mensaje("Inicio de Sesión", "Inicio de sesión exitoso")
                pantalla1.destroy()
                ventanasistema("img/fondo.jpg")
            else:
                mostrar_mensaje("Error", "Contraseña incorrecta", "error")
    except FileNotFoundError:
        mostrar_mensaje("Error", "Usuario no encontrado", "error")

def login():
    global verificacion_usuario
    global verificacion_contra
    global usuario_entrada
    global contra_entrada
    global pantalla1
    pantalla1 = tk.Toplevel(pantalla)
    pantalla1.title("Login")
    pantalla1.geometry("400x350")
    cargar_fondo(pantalla1, 'img/fondo.jpg')
    verificacion_usuario = tk.StringVar()
    verificacion_contra = tk.StringVar()
    tk.Label(pantalla1, text="Usuario *", font=("Helvetica", 10), bg="#f0f0f0").pack(pady=5)
    usuario_entrada = tk.Entry(pantalla1, textvariable=verificacion_usuario, font=("Helvetica", 10))
    usuario_entrada.pack(pady=5)
    tk.Label(pantalla1, text="Contraseña *", font=("Helvetica", 10), bg="#f0f0f0").pack(pady=5)
    contra_entrada = tk.Entry(pantalla1, textvariable=verificacion_contra, show="*", font=("Helvetica", 10))
    contra_entrada.pack(pady=5)
    tk.Button(pantalla1, text="Login Tradicional", width=20, height=2, command=verificacion_login, font=("Helvetica", 10), bg="#4CAF50", fg="white").pack(pady=10)
    tk.Button(pantalla1, text="Login por Voz", width=20, height=2, command=login_usuario_voz, font=("Helvetica", 10), bg="#FF5722", fg="white").pack(pady=10)
    tk.Button(pantalla1, text="Iniciar Sesión Facial", width=20, height=2, command=login_facial, font=("Helvetica", 10), bg="#9C27B0", fg="white").pack(pady=10)

pantalla = tk.Tk()
pantalla.title("Login")
pantalla.geometry("500x500")
cargar_fondo(pantalla, 'img/fondo.jpg')

tk.Label(pantalla, text="Inicio de Sesión", font=("Helvetica", 20), bg="#f0f0f0").pack(pady=20)
tk.Button(pantalla, text="Registrar", width=20, height=2, command=registro, font=("Helvetica", 12), bg="#4CAF50", fg="white").pack(pady=10)
tk.Button(pantalla, text="Iniciar Sesión", width=20, height=2, command=login, font=("Helvetica", 12), bg="#2196F3", fg="white").pack(pady=10)

pantalla.mainloop()
