from cgitb import text
from concurrent.futures import process
from hashlib import new
#######################################
import tkinter
import tkinter.ttk
import serial
import time
import threading


ser=serial.Serial('COM3',115200)

ventana = tkinter.Tk()  #Se crea el objeto Ventana Application   #INICICIALIZA EL OBJETO
ventana.title("CONTROL DE VELOCIDAD Y POSICION")

estado = tkinter.StringVar()
estado.set("POSICION")
value = ("0")
mode=("p")
datos = ("")
lectura = ("")
dato_retorno = ("")

def trama(): #IMPRIME LA TRAMA DE DATOS
    global lectura
    datos=mode+';'+str(scale_int.get())+';'+'f'
    print(datos)
    ser.write(datos.encode())
    time.sleep(0.01)


def read_serial():
    global dato_retorno
    while True:
        try:
            dato_retorno = ser.readline().decode().rstrip()
            if(mode=="v"):
                retorno.config(text="Velocidad: " + dato_retorno + " rpm")
            else:
                retorno.config(text="Posicion: " + dato_retorno + " grado")
        except Exception as e:
            print("Error reading serial data:", str(e))
            break

serial_thread = threading.Thread(target=read_serial)
serial_thread.daemon = True  #CREA EL HILO MIENTRAS SE CORRE EL PROGRAMA PRINCIPAL
ventana.after(100, serial_thread.start)

def controlde(): #INDICA LA VARIABLE DE CONTROL
    global estado
    global mode
    if(str(estado.get())!="VELOCIDAD"):
        estado.set("VELOCIDAD")
        mode="v"
    else:
        estado.set("POSICION")
        mode="p"
    trama()


def variador():  #ASIGNA LA POTENCIA DEL CONTROL
    global value
    value=str(scale_int.get())
    trama()

ventana.geometry("400x400")  #Dimension de ventana

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

slider = tkinter.Scale(ventana, orient="horizontal", command=lambda value:variador(), length=300, from_=0, to=1023, variable = scale_int)
slider.pack()

progress = tkinter.ttk.Progressbar(ventana, orient="horizontal", length="200", mode="determinate", maximum="1023", variable=scale_int)
progress.pack()

white_space3 = tkinter.Label(ventana, text="")
white_space3.pack(pady="10")

retorno = tkinter.Label(ventana, textvariable=dato_retorno, fg="black", bg="yellow")
retorno.pack()

ventana.mainloop()

ser.close()    