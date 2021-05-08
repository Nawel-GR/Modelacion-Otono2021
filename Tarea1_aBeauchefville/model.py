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
        self.pos = [0,-0.65] 
        self.vel = [1,1] 
        self.model = None 
        self.controller = None 
        self.size = size 
        self.radio = 0.1 

    def set_model(self, new_model):
        self.model = new_model

    def set_controller(self, new_controller):
        self.controller = new_controller

    def update(self, delta):

        if self.controller.is_d_pressed and self.pos[0] < 0.6:
            self.pos[0] += self.vel[0] * delta

        if self.controller.is_a_pressed and self.pos[0] > -0.6:
            self.pos[0] -= self.vel[0] * delta

        if self.controller.is_w_pressed:
            self.pos[1] += self.vel[1] * delta

        if self.controller.is_s_pressed:
            self.pos[1] -= self.vel[1] * delta

        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1)])

    def collision(self, objeto):
        
        for i in objeto:
            if (self.radio + i.radio)**2 > ((self.pos[0] - i.pos[0])**2 + (self.pos[1] - i.pos[1])**2):
                print("CHOQUE")
                return

class Market():
    def __init__(self, posx, posy, size_x,size_y):
        self.pos = [posx, posy]
        self.radio = 0.1
        self.size_x = size_x
        self.size_y = size_y
        self.model = None
    
    def set_model(self, new_model):
        self.model = new_model
    
    def update(self):
        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size_x, self.size_y, 1),tr.rotationZ(1.570)])

class Zombie():
    def __init__(self, size):
        zombietex = createTextureGPUShape(bs.createTextureQuad(1,1), es.SimpleTextureTransformShaderProgram(), "sprites/Boros.png")

        self.x = (np.random.randint(-5,5)+0.5)/10.0
        self.y = 1.1
        self.radio = 0.05
        self.size = size
        self.theta = self.x
        self.offset = np.random.randint(10)
        self.vel = rd.uniform(0.0006,0.001)
        self.pos = [self.x, self.y]
        
        zombieNode =sg.SceneGraphNode("zombie")
        zombieNode.transform =tr.scale(self.size,self.size,1)
        zombieNode.childs += [zombietex]
        zombie_tr=sg.SceneGraphNode("zombie_tr")
        zombie_tr.childs += [zombieNode]
        self.model = zombie_tr
    
    def set_model(self, new_model):
        self.model = new_model

    def movement(self,time):
        
        self.y -= self.vel
        
        if (self.x > 0.55):
            self.x -= 0.01

        elif (self.x < -0.5):
            self.x += 0.01

        else:
            self.x = np.sin(time-self.offset)*self.theta
        self.pos = [self.x, self.y]

    def draw(self,pipeline):
        x=self.x
        y=self.y
        self.model.transform = tr.translate(x,y,0)
        sg.drawSceneGraphNode(self.model,pipeline,"transform")

    def copy(self, personcopy):
        self.x = personcopy.x
        self.y = personcopy.y
        self.offset = personcopy.offset
        self.vel = personcopy.vel
        self.pos = personcopy.pos



class Person():
    def __init__(self, size):
        persontex = createTextureGPUShape(bs.createTextureQuad(1,1), es.SimpleTextureTransformShaderProgram(), "sprites/Genos.png")

        self.x = (np.random.randint(-5,5)+0.5)/10.0
        self.y = 1.0
        self.radio = 0.05
        self.size = size
        self.theta = self.x
        self.offset = np.random.randint(10)
        self.vel = rd.uniform(0.0006,0.001)
        self.pos = [self.x, self.y]
        self.flag = False

        personNode =sg.SceneGraphNode("person")
        personNode.transform =tr.scale(self.size,self.size,1)
        personNode.childs += [persontex]
        person1=sg.SceneGraphNode("person1")
        person1.childs += [personNode]
        self.model = person1
    
    def set_model(self, new_model):
        self.model = new_model

    def movement(self,time):
        self.y -= self.vel
        
        if (self.x > 0.55):
            self.x -= 0.01

        elif (self.x < -0.5):
            self.x += 0.01

        else:
            self.x = np.sin(time-self.offset)*self.theta
        self.pos = [self.x, self.y]
        
    def draw(self,pipeline):
        x=self.x
        y=self.y
        self.model.transform = tr.translate(x,y,0)
        sg.drawSceneGraphNode(self.model,pipeline,"transform")
    
    def collision(self, objeto):
        for i in objeto:
            if (self.radio + i.radio)**2 > ((self.pos[0] - i.pos[0])**2 + (self.pos[1] - i.pos[1])**2):
                print("CONTAGIO!!!!!!!!!")
                self.flag = True
                ###queremos crear un zombie
                return

    
