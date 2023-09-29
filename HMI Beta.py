from cgitb import text
from concurrent.futures import process
from hashlib import new
import tkinter
import tkinter.ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ventana = tkinter.Tk()  #Se crea el objeto Ventana Application   #INICICIALIZA EL OBJETO
ventana.title("CONTROL DE VELOCIDAD Y POSICION")

avance = tkinter.StringVar()
avance.set("0")

incremento = int(10)

def mode(): #Envia la señal de cambio
    global avance
    suma = int(avance.get())+incremento
    if(suma>=180):
        avance.set("ESTABLE")
    else:
        avance.set(str(suma))
    print(str(avance.get()))


ventana.geometry("400x300")  #Dimension de ventana

white_space = tkinter.Label(ventana, text="")
white_space.pack()

etiqueta = tkinter.Label(ventana, text = "HMI Control de Pendulo", bg="green") #Crear texto
etiqueta.pack(fill = tkinter.X)
etiqueta.pack() #Se posiciona el texto

white_space1 = tkinter.Label(ventana, text="")
white_space1.pack(pady="10")

boton1 = tkinter.Button(ventana, text="Press", padx = 20, pady=5, command=mode) #Se crea el objeto boton del tipo tkinter
boton1.pack()


barra_estado = tkinter.ttk.Progressbar(ventana, orient="horizontal", length="200", mode="determinate", maximum="180", variable=avance)
barra_estado.pack()

label1 = tkinter.Label(ventana, textvariable=avance, fg="black")
label1.pack()

scale_int=tkinter.IntVar()

def variador():
    print(str(scale_int.get()))

white_space2 = tkinter.Label(ventana, text="")
white_space2.pack(pady="10")

variador_title = tkinter.Label(ventana, text="VARIADOR", fg="black")
variador_title.pack()

slider = tkinter.Scale(ventana, orient="horizontal", command=lambda value:variador(), length=300, from_=0, to=100, variable = scale_int)
slider.pack()

progress = tkinter.ttk.Progressbar(ventana, orient="horizontal", length="200", mode="determinate", maximum="100", variable=scale_int)
progress.pack()


ventana.mainloop()

    