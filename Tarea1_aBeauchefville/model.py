""" Clases y objetos correspondiente al modelo"""

import glfw
import OpenGL.GL.shaders
import numpy as np
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.performance_monitor as pm
import grafica.scene_graph as sg
from shapes import *
import random as rd

class Player():
    def __init__(self, size):
        self.posx = 0.55
        self.posy = -0.85
        self.velx = 1
        self.vely = 1 
        self.model = None 
        self.controller = None 
        self.size = size 


    def set_model(self, new_model):
        self.model = new_model

    def set_controller(self, new_controller):
        self.controller = new_controller

    def update(self, delta):

        if self.controller.is_d_pressed and self.posx < 0.55:
            self.posx += self.velx * delta

        if self.controller.is_a_pressed and self.posx > -0.55:
            self.posx -= self.velx * delta

        if self.controller.is_w_pressed and self.posy < 0.9:
            self.posy += self.vely * delta

        if self.controller.is_s_pressed and self.posy > -0.9:
            self.posy -= self.vely * delta

        self.model.transform = tr.matmul([tr.translate(self.posx, self.posy, 0), tr.scale(self.size, self.size, 1)])

    def collision(self, objeto):
        for i in objeto:
            if (0.01) > ((self.posx - i.posx)**2 + (self.posy - i.posy)**2) and i.model != i.zombie:
                if  i.infected:
                    if rd.choice([1,2,3,4]) == 1: #25% de probabilidad de contagiarse y perder
                        print("PERDISTE") 

            if (0.01) > ((self.posx - i.posx)**2 + (self.posy - i.posy)**2) and i.model == i.zombie:
                print("PERDISTE")


class Market():
    def __init__(self, posx, posy, size_x,size_y):
        self.posx = posx
        self.posy = posy
        self.size_x = size_x
        self.size_y = size_y
        self.model = None
    
    def set_model(self, new_model):
        self.model = new_model
    
    def update(self):
        self.model.transform = tr.matmul([tr.translate(self.posx, self.posy, 0), tr.scale(self.size_x, self.size_y, 1),tr.rotationZ(1.570)])

    def collision(self, objeto):
        if (0.075) > ((self.posx - objeto.posx)**2 + (self.posy - objeto.posy)**2):
            print("GANASTE")


class Body():
    def __init__(self):
        self.size = 0.2
        #Se importara la imagen de Genos, la cual corresponde a la del humano
        genos_tex = createTextureGPUShape(bs.createTextureQuad(1,1), es.SimpleTextureTransformShaderProgram(), "sprites/Genos.png")
        GenosNode =sg.SceneGraphNode("GenosNode")
        GenosNode.transform =tr.scale(self.size,self.size,1)
        GenosNode.childs += [genos_tex]

        genos_c=sg.SceneGraphNode("genos_c")
        genos_c.childs += [GenosNode]

        #Se importara la imagen de Boros, la cual corresponde a la del zombie
        boros_tex = createTextureGPUShape(bs.createTextureQuad(1,1), es.SimpleTextureTransformShaderProgram(), "sprites/Boros.png") 
        BorosNode =sg.SceneGraphNode("BorosNode")
        BorosNode.transform =tr.scale(self.size,self.size,1)
        BorosNode.childs += [boros_tex]
        
        boros_c=sg.SceneGraphNode("boros_c")
        boros_c.childs += [BorosNode]

        boros2_tex = createTextureGPUShape(bs.createTextureQuad(1,1), es.SimpleTextureTransformShaderProgram(), "sprites/Genos2.png") 
        Boros2Node =sg.SceneGraphNode("Boros2Node")
        Boros2Node.transform =tr.scale(self.size,self.size,1)
        Boros2Node.childs += [boros2_tex]
        
        boros2_c=sg.SceneGraphNode("boros2_c")
        boros2_c.childs += [Boros2Node]

        self.human=genos_c
        self.zombie=boros_c
        self.zombie2=boros2_c

        self.alive = True #True si aun es humano
        self.posx = (np.random.randint(-5,5)+0.5)/10.0
        self.posy = 1.0
        self.vely = rd.uniform(0.0009,0.005)
        self.theta = rd.uniform(-0.001,0.001)
        self.offset = np.random.randint(0,10)
        self.infected = False #Ojo que pueden haber boros que no estén infectados, pero el estar vivos es mas importante
        if rd.choice([-1,1]) == -1: #Me crea aleatoriedad en los npc infectados
            self.infected = True
        
        self.model =self.human

    def boroizacion(self): #es tranformado en Boros
        self.alive=False
        self.model = self.zombie

    def is_infected(self,probability):
        if self.infected: 
            num = np.random.rand()
            if num < probability:
                self.boroizacion()
        
    def collision(self, objects):
        if not self.alive: #Genos se transforma
            for i in objects:
                if (0.01) > ((self.posx-i.posx)**2+(self.posy-i.posy)**2) and i.model != i.zombie:
                    i.boroizacion()

        if self.infected: #Boros se infecta
            for i in objects:
                if (0.01) > ((self.posx-i.posx)**2+(self.posy-i.posy)**2) and i.model != i.zombie:
                    i.infected = True
        
    def movement(self,time):
        self.posy-=self.vely
        if not self.alive:
            n=np.cos(time-self.offset)*self.theta
            if not (self.posx+n>0.5 or self.posx+n<-0.5):
                self.posx+=n    
        else:
            n=np.sin(time-self.offset)*self.theta
            if not (self.posx+n>0.5 or self.posx+n<-0.5):
                self.posx+=n  

    def spacechange1(self):
        if self.infected:    
            self.model = self.zombie2
            

    def spacechange2(self):
        if self.infected:    
            self.model = self.human 
    
        

    def draw(self,pipeline):
        self.model.transform = tr.translate(self.posx,self.posy,0)
        sg.drawSceneGraphNode(self.model,pipeline,"transform")