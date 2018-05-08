#!usr/bin/env python
# -*- coding: cp1252 -*-

from Tkinter import *   #Interfaz
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import wave
import pyaudio
import sounddevice as sd #activa el dispositivo de audio
import numpy as np
from itertools import izip_longest #herramientas de operatibilidad
from sklearn import preprocessing #procesamiento de datos
from itertools import izip
import easygui as eg

global data0, dataf, g
chunk=1024                                  #cantidad de datos
FORMAT = pyaudio.paInt16                    #8 o 16 Bits
CHANNELS = 1                                #Mono o Estereo
RATE = 44100                                #Frecuencia de grabacion
RECORD_SECONDS = 5                          #Tiempo de Grabacion
#samples = (44100/1024)*RECORD_SECONDS      #Muestras
g=1

extension = ["*.wav"]
    
   
def play_1():                   #Funcion Play 1
    
    global data0,fs
    sd.play(data0, fs)
#Fin Funcion Play1
    
def play_2():                   #Funcion Play 2
    
    global dataf,fs  
    sd.play(dataf, fs)
#Fin Funcion Play2

def Abrir():            #Abrir Archivo
    global data0, fs, g
    print ("Abrir")
    archivo = eg.fileopenbox(msg="Abrir archivo",
                             title="Control: fileopenbox",
                             default='',
                             filetypes=extension)

    fs, data0 = wavfile.read(archivo)
    
##  normailzación
    data0 = (preprocessing.normalize(data0[:,np.newaxis], axis=0).ravel())*100

    plt.subplot(2,1,1)
    plt.cla()
    plt.plot(data0)
    plt.xlim(0, len(data0))
    plt.show()                           
    print(archivo)
#Fin Función abrir#
    
def Guardar():                  #Guardar Archivo
    
    global dataf,fs
    print ("Guardar")
    archivo = eg.filesavebox(msg="Guardar archivo",
                             title="Control: filesavebox",
                             default='',
                             filetypes=extension)
    wavfile.write(archivo+'.wav', fs, dataf)
    print(archivo)
#Fin Funcion Guardar#
    
def Amplificar():
    
    global dataf
    x = np.asarray(plt.ginput(2))
    x1 = x[0]
    x2 = x[1]
    num = eg.integerbox(msg='Digite un numero:', title='Amplificar',default='1', lowerbound=0,upperbound=99)
    data1 = dataf[int(x1[0]):int(x2[0])]
    dataf = np.concatenate((dataf[:int(x1[0])],int(num)*data1,dataf[int(x2[0]):]),axis=0)
    plt.subplot(2, 1, 2)
    plt.cla()
    plt.plot(dataf, color='g')
    plt.xlim(0, len(dataf))
    plt.show()
#final de Amplificar
    
def Insertar():
    
    global data0, dataf
    x = np.asarray(plt.ginput(3))
    x1 = x[0]
    x2 = x[1]
    x3 = x[2]
    data1 = data0[int(x1[0]):int(x2[0])]    
    dataf = np.concatenate((dataf[:int(x3[0])],data1,dataf[int(x3[0]):]),axis=0)
    plt.subplot(2,1,2)
    plt.cla()
    plt.plot(dataf)
    plt.xlim(0, len(dataf))
    plt.show()
#final de Insertar
    
def Editar():
    
    global data0, dataf
    x = np.asarray(plt.ginput(2))
    x1 = x[0]
    x2 = x[1]
    dataf = data0[int(x1[0]):int(x2[0])]
    plt.subplot(2,1,2)
    plt.cla()
    plt.plot(dataf, color='g')
    plt.xlim(0, len(dataf))
    plt.show()
#final de Editar

def Mezclar():
    
    global data0, dataf
    x = np.asarray(plt.ginput(3))
    x1 = x[0]
    x2 = x[1]
    x3 = x[2]
    valor1 = data0[int(x1[0]):int(x2[0])]
    valor2 = dataf[int(x3[0]):]
    mezcla = map(sum,izip_longest(valor1,valor2, fillvalue=0))
    dataf = np.concatenate((dataf[:int(x3[0])], mezcla),axis=0)
##    mezcla = map(sum,izip(valor1,valor2))
##    dataf = np.concatenate((dataf[:int(x3[0])], mezcla,dataf[int(x3[0])+int(len(mezcla)):]),axis=0)
    plt.subplot(2,1,2)
    plt.cla()
    plt.plot(dataf , color='g')
    plt.xlim(0, len(dataf))
    plt.show()
#Fin Funcion Mezclar#
                
def Grabar():
    
    global data0, fs
    campos = ['Canales', 'Frecuencia', 'Tiempo (s)']
    datos = []
    datos = eg.multenterbox(msg='Ingrese los datos de grabación',
                            title='Grabacion',
                            fields=campos, values=('1','44100','5'))
    cadena = ''
    if datos != None:
        for cam, dat in zip(campos,datos):
            cadena = cadena + cam + ': ' + dat+ '\n'
       
    print(datos)
    cnls= int(datos[0])
    fs=int(datos[1])
    samples=(fs/chunk)*(int(datos[2])+1)
    
    p = pyaudio.PyAudio()
    stream  = p.open(format=FORMAT,channels=cnls,rate =fs,input=True,frames_per_buffer=chunk)
    stream1 = p.open(format=FORMAT,channels=cnls,rate =fs,output=True,frames_per_buffer=chunk)

    print "*grabando"

    arreglo = []
    for i in range(0, samples):
            data0 = stream.read(chunk)
            arreglo.append(data0)

    stream.stop_stream()
    stream.close()
    stream1.stop_stream()
    stream1.close()

    wf = wave.open('prueba.wav', 'wb')
    wf.setnchannels(cnls)
    wf.setframerate(fs)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.writeframes(b''.join(arreglo))
    wf.close()

    print "*fin de la grabancion"

    rate, data0 = wavfile.read("prueba.wav")
    
##  normailzación
    data0 = (preprocessing.normalize(data0[:,np.newaxis], axis=0).ravel())*100

    plt.figure(1)
    plt.subplot(2, 1, 1)
    plt.cla()
    plt.plot(data0)
    plt.xlim(0, len(data0))
    plt.show()
#Fin funcion Grabar#

def Tiempo():
    global fs, data0,dataf
        
    longitud1 = np.arange(0,len(data0))
    segundos1 = max(longitud1)/float(fs)
    tiempos_1 = np.linspace(0, segundos1, len(data0)) 
    longitud2 = np.arange(0,len(dataf))
    segundos2 = max(longitud2)/float(fs)
    tiempos_2 = np.linspace(0, segundos1, len(dataf))
    
    plt.subplot(2, 1, 1)
    plt.cla()
    plt.plot(tiempos_1,data0)
    plt.xlim(0,segundos1)

    plt.subplot(2, 1, 2)
    plt.cla()
    plt.plot(tiempos_2,dataf)
    plt.xlim(0,segundos2)

    plt.show()
#Fin Funcion Tiempo

def Frecuencia():
    global fs, data0, dataf
    N = len(data0)
    N1 = len(dataf)
    # sample spacing
    T = 1.0 / fs

    x = np.linspace(0.0, N*T, N)
    x1 = np.linspace(0.0, N1*T, N1)
    
    d0 = fft(data0)
    df = fft(dataf)
    
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
    xf1 =np.linspace(0.0, 1.0/(2.0*T), N1/2)
    
    
   # plt.grid()
    
    fig = plt.figure(1)
    plt.subplot(2, 1, 1)
    plt.cla()
    plt.plot(xf, 2.0/N * np.abs(d0[0:N/2]))
    plt.xlim(0, fs/4)
   
    plt.subplot(2, 1, 2)
    plt.cla()
    plt.plot(xf1, 2.0/N * np.abs(df[0:N1/2]))
    plt.xlim(0, fs/4)
    plt.show()
#fin funcion frecuencia
    
def Muestras():
    global fs, data0, dataf
    fig = plt.figure(1)
    plt.subplot(2, 1, 1)
    plt.cla()
    plt.plot(data0)
    plt.xlim(0, len(data0))
    
    plt.subplot(2, 1, 2)
    plt.cla()
    plt.plot(dataf)
    plt.xlim(0, len(dataf))
    plt.show()
#Fin Funcion Muestras
    
#creando la ventana
ventana=Tk()
ventana.geometry("500x300+100+200")     #Tamaño de la pantalla
ventana.title("Proyecto 1")             #Titulo del proyecto
ventana.resizable(0,0)                  #Evita que la ventana se pueda cambiar de tamaño

### receta para crear menus

# paso 1 crear la barra de menus

barramenu=Menu(ventana)

#paso 2 crear los menus

mnuArchivo=Menu(barramenu)
mnuHerramientas=Menu(barramenu)
mnuGraficas=Menu(barramenu)

#Crear Sub-Menus
#Sub-Menu Archivos
mnuArchivo.add_command(label="Grabar",command=Grabar)
mnuArchivo.add_command(label="Abrir", command=Abrir)
mnuArchivo.add_command(label="Guardar", command=Guardar)
mnuArchivo.add_separator()
mnuArchivo.add_command(label="Salir",command=ventana.destroy)

#Sub-Menu Herramientas
mnuHerramientas.add_command(label="Editar", command=Editar)
mnuHerramientas.add_command(label="Amplificar", command=Amplificar)
mnuHerramientas.add_command(label="Mezclar", command=Mezclar)
mnuHerramientas.add_command(label="Insertar", command=Insertar)

#Sub-Menu Graficas
mnuGraficas.add_command(label="Muestras", command = Muestras)
mnuGraficas.add_command(label="Tiempo", command = Tiempo)
mnuGraficas.add_command(label="Frecuencia", command = Frecuencia)

#paso 4 agergar los menus a la barra de menus
barramenu.add_cascade(label="Archivo",menu=mnuArchivo)
barramenu.add_cascade(label="Herramientas",menu=mnuHerramientas)
barramenu.add_cascade(label="Graficas",menu=mnuGraficas)
ventana.config(menu=barramenu)      #Comando para inicializar el menú

#Creacion de Botones
Img_Boton=PhotoImage(file="play.gif")

Play1 = Button(ventana,image=Img_Boton,command=play_1,font=("Agency FB",14),height=30,width=40).place(x=100,y=100)
Play2 = Button(ventana,image=Img_Boton,command=play_2,font=("Agency FB",14),height=30,width=40).place(x=300,y=100)

fig = plt.figure(1)
plt.subplot(2, 1, 1)
plt.subplot(2, 1, 2)
plt.show()

ventana.mainloop()
