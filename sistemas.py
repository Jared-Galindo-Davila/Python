from tkinter import *
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import numpy as np

#------------------------ Función para registrar el usuario -----------------------
def registrar_usuario():
    usuario_info = usuario.get()
    contra_info = contra.get()

    with open(usuario_info, "w") as archivo:
        archivo.write(usuario_info + "\n")
        archivo.write(contra_info)

    # Limpiamos los campos de entrada
    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)

    # Mensaje de éxito
    Label(pantalla1, text="Registro Convencional Exitoso", fg="green", font=("Calibri", 11)).pack(pady=10)

#------------------------ Función para registro facial -----------------------
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

    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)
    Label(pantalla1, text="Registro Facial Exitoso", fg="green", font=("Calibri", 11)).pack(pady=10)

    # Detectamos el rostro y exportamos los pixeles
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

#------------------------ Función para asignar al botón de registro -----------------------
def registro():
    global usuario
    global contra
    global usuario_entrada
    global contra_entrada
    global pantalla1
    pantalla1 = Toplevel(pantalla)
    pantalla1.title("Registro")
    pantalla1.geometry("350x300")
    pantalla1.configure(bg='#f0f0f0')

    # Creación de las entradas
    usuario = StringVar()
    contra = StringVar()

    Label(pantalla1, text="Registro Facial", font=("Calibri", 14, "bold"), bg='#f0f0f0').pack(pady=10)
    Label(pantalla1, text="Ingrese un nombre de usuario:", bg='#f0f0f0').pack(pady=5)
    usuario_entrada = Entry(pantalla1, textvariable=usuario, width=30)
    usuario_entrada.pack(pady=5)
    Label(pantalla1, text="Ingrese una contraseña:", bg='#f0f0f0').pack(pady=5)
    contra_entrada = Entry(pantalla1, textvariable=contra, show='*', width=30)
    contra_entrada.pack(pady=5)

    Button(pantalla1, text="Registro Tradicional", width=20, height=2, command=registrar_usuario, bg='#4CAF50', fg='white').pack(pady=10)
    Button(pantalla1, text="Registro Facial", width=20, height=2, command=registro_facial, bg='#2196F3', fg='white').pack(pady=10)

#------------------------ Función para verificar los datos ingresados en el login -----------------------
def verificacion_login():
    log_usuario = verificacion_usuario.get()
    log_contra = verificacion_contra.get()

    usuario_entrada2.delete(0, END)
    contra_entrada2.delete(0, END)

    lista_archivos = os.listdir()
    if log_usuario in lista_archivos:
        with open(log_usuario, "r") as archivo2:
            verificacion = archivo2.read().splitlines()
            if log_contra in verificacion:
                Label(pantalla2, text="Inicio de Sesión Exitoso", fg="green", font=("Calibri", 11)).pack(pady=10)
            else:
                Label(pantalla2, text="Contraseña Incorrecta", fg="red", font=("Calibri", 11)).pack(pady=10)
    else:
        Label(pantalla2, text="Usuario no encontrado", fg="red", font=("Calibri", 11)).pack(pady=10)

#------------------------ Función para el login facial -----------------------
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

    usuario_entrada2.delete(0, END)
    contra_entrada2.delete(0, END)

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
            Label(pantalla2, text="Inicio de Sesión Exitoso", fg="green", font=("Calibri", 11)).pack(pady=10)
        else:
            Label(pantalla2, text="Incompatibilidad de rostros", fg="red", font=("Calibri", 11)).pack(pady=10)
    else:
        Label(pantalla2, text="Usuario no encontrado", fg="red", font=("Calibri", 11)).pack(pady=10)

#------------------------ Función para el login -----------------------
def login():
    global pantalla2
    global verificacion_usuario
    global verificacion_contra
    global usuario_entrada2
    global contra_entrada2

    pantalla2 = Toplevel(pantalla)
    pantalla2.title("Login")
    pantalla2.geometry("350x300")
    pantalla2.configure(bg='#f0f0f0')

    Label(pantalla2, text="Login Facial", font=("Calibri", 14, "bold"), bg='#f0f0f0').pack(pady=10)
    Label(pantalla2, text="Ingrese un nombre de usuario:", bg='#f0f0f0').pack(pady=5)
    verificacion_usuario = StringVar()
    verificacion_contra = StringVar()
    usuario_entrada2 = Entry(pantalla2, textvariable=verificacion_usuario, width=30)
    usuario_entrada2.pack(pady=5)
    Label(pantalla2, text="Ingrese una contraseña:", bg='#f0f0f0').pack(pady=5)
    contra_entrada2 = Entry(pantalla2, textvariable=verificacion_contra, show='*', width=30)
    contra_entrada2.pack(pady=5)

    Button(pantalla2, text="Inicio Tradicional", width=20, height=2, command=verificacion_login, bg='#4CAF50', fg='white').pack(pady=10)
    Button(pantalla2, text="Inicio Facial", width=20, height=2, command=login_facial, bg='#2196F3', fg='white').pack(pady=10)

#------------------------ Función de la pantalla principal -----------------------
def pantalla_principal():
    global pantalla
    pantalla = Tk()
    pantalla.geometry("300x250")
    pantalla.title("Proyecto")
    pantalla.configure(bg='#e0e0e0')

    Label(text="Login Inteligente", bg="#4CAF50", fg="white", width="300", height="2", font=("Verdana", 16)).pack()

    Button(text="Registro", height="2", width="30", command=registro, bg='#4CAF50', fg='white').pack(pady=10)
    Button(text="Login", height="2", width="30", command=login, bg='#2196F3', fg='white').pack(pady=10)

    pantalla.mainloop()

#------------------------ Ejecutamos la pantalla principal -----------------------
pantalla_principal()

