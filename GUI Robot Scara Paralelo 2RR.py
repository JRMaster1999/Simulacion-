# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 13:24:40 2020

@author: Gonzalez Bañez, Ricardo Danfer
Segura Mendez, Roger Junior
Tello Chavez, Norbil Ever

"""

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import Frame, Label, Button, Spinbox, Radiobutton
from tkinter.ttk import Combobox
import math 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.misc import derivative

class Interfaz(Frame):
    
    a = 1
    L = 20
    L5 = 15
    Cx= np.arange(0,20,0.2)
    Vc= 1 #cm/s 
    t_pulsIn = 1000
    t_pulsFin = 2000
    D_CInt_1 = []
    D_CInt_2 = []
    x5=[-2.5,2.5]
    y5=[-2,-2]
    x6=[12.5,17.5]
    y6=[-2,-2]
    salir = 0 
    pausa = True
    b = 0
    
    def __init__(self, master=None): #Constructor
        super().__init__(master, bg = "dark turquoise", width = 350, height = 700)
        
        self.master = master
        self.pack(side = "left",fill = "both", expand="True")
        self.crearWidgets()
        
        self.fig = Figure()
        self.ax1=self.fig.add_subplot(221)
        self.ax2=self.fig.add_subplot(222)
        self.ax3=self.fig.add_subplot(223)
        self.ax4=self.fig.add_subplot(224)
        
        self.fig.patch.set_facecolor('blue')
        self.fig.patch.set_alpha(0.3)
        
        self.canvas = FigureCanvasTkAgg(self.fig, root)
        self.canvas.get_tk_widget().config(width=760)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side = tk.RIGHT,fill = tk.BOTH, expand = 1)
        
        self.funcAnim()
            
        
    def funcAnim(self): 
        def animacion(i):
            
            self.ax1.clear()
            self.ax2.clear()
            self.ax3.clear()
            self.ax4.clear()
            
            #len(self.Cx)-i-1
            if i>=1:
                self.ax1.plot(self.Cx,self.crearDatos(0,0),linestyle='--',linewidth=2.0)
            self.ax1.plot((self.crearDatos(5,1))[i],(self.crearDatos(5,2))[i],linewidth=5.0,color = "red")
            self.ax1.plot((self.crearDatos(5,3))[i],(self.crearDatos(5,4))[i],linewidth=5.0,color = "orange")
            self.ax1.plot((self.crearDatos(5,5))[i],(self.crearDatos(5,6))[i],linewidth=5.0,color = "blue")
            self.ax1.plot((self.crearDatos(5,7))[i],(self.crearDatos(5,8))[i],linewidth=5.0,color = "green")
            self.ax1.plot(self.x5,self.y5,'b',linewidth=18)
            self.ax1.plot(self.x6,self.y6,'b',linewidth=18)
            self.ax1.set_xlabel('x')
            self.ax1.set_ylabel('y')
            self.ax1.set_xlim(-20,35)
            self.ax1.set_ylim(-10,40)
            self.ax1.grid()
            
            #Graficando Angulos vs Tiempo
            self.ax2.plot((self.crearDatos(1,1))[:i],(self.crearDatos(2,1))[:i],linewidth=2.0, label="Angulo 1",color = "red")
            self.ax2.plot((self.crearDatos(1,1))[:i],(self.crearDatos(2,2))[:i],linewidth=2.0, label="Angulo 2",color = "blue")
            self.ax2.plot((self.crearDatos(1,1))[:i],(self.crearDatos(2,3))[:i],linewidth=2.0, label="Angulo 3",color = "goldenrod")
            self.ax2.plot((self.crearDatos(1,1))[:i],(self.crearDatos(2,4))[:i],linewidth=2.0, label="Angulo 4",color = "brown")
            self.ax2.set_xlabel('Tiempo (s)')
            self.ax2.set_ylabel('Angulo (rad)')
            self.ax2.set_xlim(-1,self.crearDatos(1,2)+15)
            self.ax2.set_ylim(0,4)
            self.ax2.legend(loc = "lower right", frameon = "False")
            self.ax2.grid()
            
            #Graficando Velocidades angulares vs Tiempo
            self.ax3.plot((self.crearDatos(1,1))[:i],(self.crearDatos(3,1))[:i],linewidth=2.0,label="w_1",color = "orange")
            self.ax3.plot((self.crearDatos(1,1))[:i],(self.crearDatos(3,2))[:i],linewidth=2.0,label="w_2",color = "green")
            self.ax3.plot((self.crearDatos(1,1))[:i],(self.crearDatos(3,3))[:i],linewidth=2.0,label="w_3",color = "purple")
            self.ax3.plot((self.crearDatos(1,1))[:i],(self.crearDatos(3,4))[:i],linewidth=2.0,label="w_4",color = "navy")
            self.ax3.set_xlabel('Tiempo (s)')
            self.ax3.set_ylabel('Velocidad Angular (rad/s)')
            self.ax3.set_xlim(-1,self.crearDatos(1,2)+13)
            self.ax3.set_ylim(-0.1,0.075)
            self.ax3.legend(loc = "lower right", frameon = "False")
            self.ax3.grid()
            
            #Graficando Tiempo de pulso vs Tiempo
            self.ax4.plot((self.crearDatos(1,1))[:i],(self.crearDatos(4,1))[:i],linewidth=2.0,label="Ancho de pulso 1",color = "red")
            self.ax4.plot((self.crearDatos(1,1))[:i],(self.crearDatos(4,2))[:i],linewidth=2.0,label="Ancho de pulso 2",color = "blue")
            self.ax4.set_xlabel('Tiempo (s)')
            self.ax4.set_ylabel('Ancho de pulso (us)')
            self.ax4.set_xlim(-1,self.crearDatos(1,2)+15)
            self.ax4.set_ylim(1000,2000)
            self.ax4.legend(loc = "lower right", frameon = "False")
            self.ax4.grid()
            
            if i==0:
                self.ani1.event_source.stop()
                self.boton1['state'] = tk.NORMAL
                self.boton2['state'] = tk.DISABLED
                self.boton3['state'] = tk.DISABLED
                self.barraFunciones['state'] = tk.NORMAL
                self.boton5['state'] = tk.DISABLED
                self.pausa = True
                
            if i==(len(self.Cx)-1):
                self.ani1.event_source.stop()
                self.boton2['state'] = tk.DISABLED
                self.boton3['state'] = tk.DISABLED
                self.boton5['state'] = tk.NORMAL
                self.pausa = True
                
            plt.tight_layout()
            plt.show   
            
        self.ani1 = animation.FuncAnimation(self.fig,animacion,range(len(self.Cx)),interval=1,repeat=True)

    def crearWidgets(self):
        
        self.miLabel1 = Label(self, text = "INTERFAZ GRÁFICA DEL ROBOT",fg = "blue", bg = "dark turquoise",
                font = ("Helvetica",13,"bold"))
        self.miLabel1.place(x = 30, y = 10)
        
        self.miLabel2 = Label(self, text = "SCARA PARALELO 2RR",fg = "blue", bg = "dark turquoise",
                        font = ("Helvetica",13,"bold"))
        self.miLabel2.place(x = 65, y = 30)
        
        self.boton1 = Button(self, text = "INICIAR", width = 10, height = 1,bg = "gold",font = ("Helvetica",11),command=lambda:self.activador1(1))
        self.boton1.place(x = 105, y = 80)
        
        self.boton2 = Button(self, text = "PAUSAR", width = 10, height = 1,bg = "gold",font = ("Helvetica",11),command=lambda:self.activador1(2))
        self.boton2.place(x = 105, y = 130)
        
        self.boton3 = Button(self, text = "REANUDAR", width = 10, height = 1,bg = "gold",font = ("Helvetica",11),command=lambda:self.activador1(3))
        self.boton3.place(x = 105, y = 180)
        
        self.activarCom = Radiobutton(self, text="Activar Comunicación Serial", value=1, bg = "dark turquoise", font = ("Helvetica",10,"bold"), command=lambda:self.activarComSerial())
        self.activarCom.place(x = 75, y = 290)
        
        self.desactivarCom = Radiobutton(self, text="Desactivar Comunicación Serial", value=2, bg = "dark turquoise", font = ("Helvetica",10,"bold"), command=lambda:self.desactivarComSerial())
        self.desactivarCom.place(x = 75, y = 320)
        
        self.miLabel4 = Label(self, text = "Longitud de", bg = "dark turquoise", font = ("Helvetica",12,"bold"))
        self.miLabel4.place(x = 15, y = 360)
        
        self.miLabel5 = Label(self, text = "barra:", bg = "dark turquoise", font = ("Helvetica",12,"bold"))
        self.miLabel5.place(x = 15, y = 382)
        
        self.TamanoBarra =Spinbox(self, from_ = 10, to =20, width = 10)
        self.TamanoBarra.place(x = 120, y = 375)
        
        self.barraFunciones = Combobox(self,values = ["Recta Horizontal","Recta Inclinada","Parábola","Onda Senoidal","Circunferencia","Lemniscata"],
                                       state="readonly") #postcommand=lambda:self.seleccion()
        self.barraFunciones.bind("<<ComboboxSelected>>", self.activador2)
        self.barraFunciones.current(0)
        self.barraFunciones.place(x = 120, y = 435)
        
        self.miLabel6 = Label(self, text = "Seleccionar:", bg = "dark turquoise", font = ("Helvetica",12,"bold"))
        self.miLabel6.place(x = 15, y = 432)
        
        self.boton5 = Button(self, text = "NUEVA TRAYECTORIA", width = 18, height = 1,bg = "gold",font = ("Helvetica",11),command=lambda:self.activador1(4))
        self.boton5.place(x = 70, y = 230)
        
    def setA(self,a):
        self.a=a
        
    def activador1(self,i):
        if i==1:
            self.ani1.event_source.start()
            self.boton1['state'] = tk.DISABLED
            self.boton2['state'] = tk.NORMAL
            self.barraFunciones['state'] = tk.DISABLED
            self.pausa = False
        
        elif i==2:
            self.ani1.event_source.stop()
            self.boton2['state'] = tk.DISABLED
            self.boton3['state'] = tk.NORMAL
            self.pausa = True
            
        elif i==3: 
            self.ani1.event_source.start()
            self.boton2['state'] = tk.NORMAL
            self.boton3['state'] = tk.DISABLED
            self.pausa = False
            
        elif i==4:
            self.ani1.event_source.start()
            self.boton5['state'] = tk.DISABLED
            self.b = 0
            
    def activarComSerial(self):
        self.salir = 0
        
    def desactivarComSerial(self):
        self.salir = 1
        
    def activador2(self,event):
        if self.barraFunciones.get()=="Recta Horizontal":
            self.setA(1)
            
        elif self.barraFunciones.get()=="Recta Inclinada":
            self.setA(2)
            
        elif self.barraFunciones.get()=="Parábola":
            self.setA(3)
            
        elif self.barraFunciones.get()=="Onda Senoidal":
            self.setA(4)
            
        elif self.barraFunciones.get()=="Circunferencia":
            self.setA(5)
            
        elif self.barraFunciones.get()=="Lemniscata":
            self.setA(6)
                 
    def longCurv(self,x,y):
        self.long = 0
        for k in range(1,len(x),1):
            self.long = self.long + np.sqrt((x[k]-x[k-1])**2+(y[k]-y[k-1])**2)
                
        return self.long
            
    def crearDatos(self,i,j):
        #self.Cx = self.Cx[::-1]
        #funciones Cy
        if self.a==1:
            xx = np.ones(len(self.Cx))
            self.Cy = 25*xx
            Fy = lambda x: 25
        
        elif self.a==2:
            self.Cx= np.arange(0,20,0.2)
            self.Cy = self.Cx/2+20
            Fy = lambda x: x/2+20
            
        elif self.a==3: 
            self.Cx= np.arange(0,20,0.2)
            self.Cy = (-1/8)*(self.Cx)**2+2.5*(self.Cx)+21.5
            Fy = lambda x: -(1/8)*x**2+2.5*x+21.5  
            
        elif self.a==4:
            self.Cx= np.arange(0,20,0.2)
            self.Cy = 6*np.sin(self.Cx/2)+27
            Fy = lambda x: 6*np.sin(x/2)+27
        
        elif self.a==5: 
            ang = np.arange(0,2*math.pi,2*math.pi/100)
            self.Cx = 6*np.cos(ang)+10
            self.Cy = 6*np.sin(ang)+27
            Fx = lambda x: 6*np.cos(x)+10
            Fy = lambda x: 6*np.sin(x)+27
            
        elif self.a==6: 
            ang = np.arange(0,2*math.pi,2*math.pi/100)
            self.Cx = 8*np.cos(ang)/(1+(np.sin(ang))**2)+10
            self.Cy = 8*np.sin(ang)*np.cos(ang)/(1+(np.sin(ang))**2)+27
            Fx = lambda x: 8*np.cos(x)/(1+(np.sin(x))**2)+10
            Fy = lambda x: 8*np.sin(x)*np.cos(x)/(1+(np.sin(x))**2)+27
            
        #Seleccionar Función Cy
        if i==0:
            if j==0:
                return self.Cy
        
        #Componentes de la velocidad
        if self.a <=4:
            f = Fy
            der = derivative(f,self.Cx,dx=1e-6)
            alpha = np.arctan(der) #angulo del vector velocidad
            Vcx = (self.Vc)*np.cos(alpha)
            Vcy = (self.Vc)*np.sin(alpha)
            
        if self.a>=5:
            f1 = Fx
            f2 = Fy
            der1 = derivative(f1,ang,dx=1e-6)
            der2 = derivative(f2,ang,dx=1e-6)
            alpha1 = np.arctan(der1) #angulo1 del vector velocidad
            alpha2 = np.arctan(der2) #angulo2 del vector velocidad
            Vcx = (self.Vc)*np.cos(alpha1)
            Vcy = (self.Vc)*np.sin(alpha2)
        
        #Valores para las formulas
        A1 = self.Cx
        B1 = self.Cy  
        C1 = ((self.Cx)**2+(self.Cy)**2)/(2*self.L)       
        A4 = (self.Cx)-(self.L5)
        B4 = self.Cy
        C4 = ((self.L5)**2-2*(self.L5)*(self.Cx)+(self.Cx)**2+(self.Cy)**2)/(2*self.L)
        
        #Tiempo Final
        longitud = self.longCurv(self.Cx,self.Cy)
        timFin = longitud/(self.Vc)
        
        #Formula de Tiempo
        t = np.arange(0,timFin,timFin/len(self.Cx))
        
        #Selecionar Tiempo
        if i==1:
            if j==1:
                return t
            elif j==2:
                return timFin
        
        #Formulas de los Angulos
        theta1 = 2*np.arctan((-B1-np.sqrt(A1**2+B1**2-C1**2))/(-A1-C1))
        theta2 = np.arccos((self.Cx)/(self.L)-np.cos(theta1))
        theta4 = 2*np.arctan((-B4+np.sqrt(A4**2+B4**2-C4**2))/(-A4-C4)) 
        theta3 = np.arccos(A4/(self.L)-np.cos(theta4))

        #Selecionar Angulos
        if i==2:
            if j==1:
                return theta1
            
            elif j==2:
                return theta2
                
            elif j==3:
                return theta3
                
            elif j==4:
                return theta4
        
        #Fomulas de las Velocidades angulares
        w1 = -Vcx*(np.cos(theta2)/((self.L)*np.sin(theta1-theta2)))-Vcy*(np.sin(theta2)/((self.L)*np.sin(theta1-theta2)))
        w2 = Vcx*(np.cos(theta1)/((self.L)*np.sin(theta1-theta2)))+Vcy*(np.sin(theta1)/((self.L)*np.sin(theta1-theta2)))
        w3 = Vcx*(np.cos(theta4)/((self.L)*np.sin(theta4-theta3)))+Vcy*(np.sin(theta4)/((self.L)*np.sin(theta4-theta3)))
        w4 = -Vcx*(np.cos(theta3)/((self.L)*np.sin(theta4-theta3)))-Vcy*(np.sin(theta3)/((self.L)*np.sin(theta4-theta3)))
        
        #Selecionar Velocidades angulares
        if i==3:
            if j==1:
                return w1
            
            elif j==2:
                return w2
                
            elif j==3:
                return w3
                
            elif j==4:
                return w4
            
        #Fomulas de los Tiempos de pulso
        t_puls1 = (((self.t_pulsFin)-(self.t_pulsIn))/math.pi)*(math.pi-theta1)+1000
        t_puls2 = (((self.t_pulsFin)-(self.t_pulsIn))/math.pi)*(math.pi-theta4)+1000
        #Selecionar Tiempos de pulso
        if i==4:
            if j==1:
                return t_puls1
            
            elif j==2:
                return t_puls2
            
        x1=[] 
        y1=[] 
        x2=[] 
        y2=[] 
        x3=[] 
        y3=[] 
        x4=[] 
        y4=[]
        
        #Construción de los eslabones        
        #Seleccionar eslabones
        if i==5:
            if j==1:
                for k in range(len(self.Cx)):
                    x1.append([0,(self.L)*np.cos(theta1[k])])
                return x1
    
            elif j==2:
                for k in range(len(self.Cx)):
                    y1.append([0,(self.L)*np.sin(theta1[k])])
                return y1
            
            elif j==3:
                for k in range(len(self.Cx)):
                    x2.append([(self.L)*np.cos(theta1[k]),(self.L)*np.cos(theta1[k])+(self.L)*np.cos(theta2[k])])
                return x2
    
            elif j==4:
                for k in range(len(self.Cx)):
                    y2.append([(self.L)*np.sin(theta1[k]),(self.L)*np.sin(theta1[k])+(self.L)*np.sin(theta2[k])])
                return y2
    
            elif j==5:
                for k in range(len(self.Cx)):
                    x3.append([15+(self.L)*np.cos(theta4[k]),15+(self.L)*np.cos(theta4[k])+(self.L)*np.cos(theta3[k])])
                return x3
    
            elif j==6:
                for k in range(len(self.Cx)):
                    y3.append([(self.L)*np.sin(theta4[k]),(self.L)*np.sin(theta3[k])+(self.L)*np.sin(theta4[k])])
                return y3
    
            elif j==7:
                for k in range(len(self.Cx)):
                    x4.append([15,15+(self.L)*np.cos(theta4[k])])
                return x4
            
            elif j==8:
                for k in range(len(self.Cx)):
                    y4.append([0,(self.L)*np.sin(theta4[k])])
                return y4  
      
        
root = tk.Tk()
root.wm_title("Interfaz Gráfica")
app = Interfaz(root)
app.mainloop()