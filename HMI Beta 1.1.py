from cgitb import text
from concurrent.futures import process
from hashlib import new
#######################################
import tkinter
import tkinter.ttk

ventana = tkinter.Tk()  #Se crea el objeto Ventana Application   #INICICIALIZA EL OBJETO
ventana.title("CONTROL DE VELOCIDAD Y POSICION")

estado = tkinter.StringVar()
estado.set("POSICION")
value = ("0")
mode=("p")

def trama():
    print(mode+';'+str(scale_int.get())+';'+'f')

def controlde(): #IMPRIME LOS INCREMENTOS DEL BOTÓN
    global estado
    global mode
    if(str(estado.get())!="VELOCIDAD"):
        estado.set("VELOCIDAD")
        mode="v"
    else:
        estado.set("POSICION")
        mode="p"
    trama()


def variador():  #IMPRIME EL VALOR DEL SLIDER
    global value
    value=str(scale_int.get())
    trama()


ventana.geometry("400x300")  #Dimension de ventana

white_space = tkinter.Label(ventana, text="")
white_space.pack()

etiqueta = tkinter.Label(ventana, text = "CONTROL DE POSICION Y VELOCIDAD", bg="green") #Crear texto
etiqueta.pack(fill = tkinter.X)
etiqueta.pack() #Se posiciona el texto

white_space1 = tkinter.Label(ventana, text="")
white_space1.pack(pady="10")

boton1 = tkinter.Button(ventana, text="Press", padx = 20, pady=5, command=controlde) #Se crea el objeto boton del tipo tkinter
boton1.pack()


label1 = tkinter.Label(ventana, textvariable=estado, fg="black")
label1.pack()

scale_int=tkinter.IntVar()


white_space2 = tkinter.Label(ventana, text="")
white_space2.pack(pady="10")

variador_title = tkinter.Label(ventana, text="VARIADOR", fg="black")
variador_title.pack()

slider = tkinter.Scale(ventana, orient="horizontal", command=lambda value:variador(), length=300, from_=0, to=1024, variable = scale_int)
slider.pack()

progress = tkinter.ttk.Progressbar(ventana, orient="horizontal", length="200", mode="determinate", maximum="1024", variable=scale_int)
progress.pack()


ventana.mainloop()

    