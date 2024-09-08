from tkinter import *
from PIL import Image, ImageTk
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import numpy as np

def cargar_fondo(pantalla, imagen):
    def actualizar_fondo(event=None):
        img = Image.open(imagen)
        img = img.resize((pantalla.winfo_width(), pantalla.winfo_height()), Image.LANCZOS)
        img_fondo = ImageTk.PhotoImage(img)
        fondo.config(image=img_fondo)
        fondo.image = img_fondo

    fondo = Label(pantalla)
    fondo.place(x=0, y=0, relwidth=1, relheight=1)
    actualizar_fondo()
    pantalla.bind('<Configure>', actualizar_fondo)

def registrar_usuario():
    usuario_info = usuario.get()
    contra_info = contra.get()
    with open(usuario_info, "w") as archivo:
        archivo.write(usuario_info + "\n")
        archivo.write(contra_info)
    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)
    Label(pantalla1, text="Registro Convencional Exitoso", fg="green", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)

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

def registro():
    global usuario
    global contra
    global usuario_entrada
    global contra_entrada
    global pantalla1
    pantalla1 = Toplevel(pantalla)
    pantalla1.title("Registro")
    pantalla1.geometry("400x350")
    cargar_fondo(pantalla1, 'img/fondo.jpg')
    usuario = StringVar()
    contra = StringVar()
    Label(pantalla1, text="Usuario *", font=("Helvetica", 10), bg="#f0f0f0").pack(pady=5)
    usuario_entrada = Entry(pantalla1, textvariable=usuario, font=("Helvetica", 10))
    usuario_entrada.pack(pady=5)
    Label(pantalla1, text="Contraseña *", font=("Helvetica", 10), bg="#f0f0f0").pack(pady=5)
    contra_entrada = Entry(pantalla1, textvariable=contra, show="*", font=("Helvetica", 10))
    contra_entrada.pack(pady=5)
    Button(pantalla1, text="Registro Tradicional", width=20, height=2, command=registrar_usuario, font=("Helvetica", 10), bg="#4CAF50", fg="white").pack(pady=10)
    Button(pantalla1, text="Registro Facial", width=20, height=2, command=registro_facial, font=("Helvetica", 10), bg="#2196F3", fg="white").pack(pady=10)

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
            iniciar_sesion()
        else:
            Label(pantalla2, text="Contraseña Incorrecta", fg="red", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)
    else:
        Label(pantalla2, text="Usuario no encontrado", fg="red", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)

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

def iniciar_sesion():
    global pantalla2
    global pantalla_principal
    if pantalla1:
        pantalla1.destroy()
    if pantalla2:
        pantalla2.destroy()
    pantalla_principal = Toplevel(pantalla)
    pantalla_principal.title("Pantalla Principal")
    pantalla_principal.geometry("650x800")
    cargar_fondo(pantalla_principal, 'img/fondo.jpg')
    Label(pantalla_principal, text="Bienvenido al sistema", bg="gray", width="400", height="2", font=("Verdana", 16)).pack(pady=20)
    Button(pantalla_principal, text="Cerrar Sesión", width=20, height=2, command=lambda: cerrar_sesion(pantalla_principal), font=("Helvetica", 12), bg="#f44336", fg="white").pack(pady=10)

def cerrar_sesion(pantalla_principal):
    pantalla_principal.destroy()
    pantalla_principal()

def login():
    global pantalla2
    global verificacion_usuario
    global verificacion_contra
    global usuario_entrada2
    global contra_entrada2
    
    pantalla2 = Toplevel(pantalla)
    pantalla2.title("Login")
    pantalla2.geometry("400x350")
    cargar_fondo(pantalla2, 'img/fondo.jpg')
    verificacion_usuario = StringVar()
    verificacion_contra = StringVar()
    Label(pantalla2, text="Usuario *", font=("Helvetica", 10), bg="#f0f0f0").pack(pady=5)
    usuario_entrada2 = Entry(pantalla2, textvariable=verificacion_usuario, font=("Helvetica", 10))
    usuario_entrada2.pack(pady=5)
    Label(pantalla2, text="Contraseña *", font=("Helvetica", 10), bg="#f0f0f0").pack(pady=5)
    contra_entrada2 = Entry(pantalla2, textvariable=verificacion_contra, show="*", font=("Helvetica", 10))
    contra_entrada2.pack(pady=5)
    Button(pantalla2, text="Inicio de Sesion Tradicional", width=20, height=2, command=verificacion_login, font=("Helvetica", 10), bg="#4CAF50", fg="white").pack(pady=10)
    Button(pantalla2, text="Inicio de Sesion Facial", width=20, height=2, command=login_facial, font=("Helvetica", 10), bg="#2196F3", fg="white").pack(pady=10)

def pantalla_principal():
    global pantalla
    pantalla = Tk()
    pantalla.geometry("400x350")
    pantalla.title("Proyecto")
    cargar_fondo(pantalla, 'img/fondo.jpg')
    Label(pantalla, text="Login y Registro", bg="gray", width="400", height="2", font=("Verdana", 16)).pack(pady=20)
    Button(pantalla, text="Iniciar Sesion", height="2", width="30", command=login, font=("Helvetica", 12), bg="#4CAF50", fg="white").pack(pady=10)
    Button(pantalla, text="Registro", height="2", width="30", command=registro, font=("Helvetica", 12), bg="#2196F3", fg="white").pack(pady=10)
    pantalla.mainloop()

pantalla_principal()
