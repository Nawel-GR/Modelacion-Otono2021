# coding=utf-8
"""
Nahuel Gómez, CC3501, 2020-1
Tarea 2_a
Controlador
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import grafica.transformations as tr
import grafica.easy_shaders as es
import grafica.scene_graph as sg
from grafica.assets_path import getAssetPath

class Shape:
    def __init__(self, vertices, indices, textureFileName=None):
        self.vertices = vertices
        self.indices = indices
        self.textureFileName = textureFileName

def createNewTextureQuad(xi,xf,yi, yf):
    vertices = [
    #   positions        texture
         0, -0.5,-0.5, xi, yf,
         0, -0.5, 0.5, xf, yf,
         0,  0.5, 0.5, xf, yi,
         0,  0.5,-0.5, xi, yi]

    indices = [
         0, 1, 2,
         2, 3, 0]

    return Shape(vertices, indices)

def createTextureGPUShape(shape, pipeline, img_name):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    gpuShape.texture = es.textureSimpleSetup(
        getAssetPath(img_name), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    return gpuShape

class Controller:
    def __init__(self):
        self.leftClickOn = False
        self.rightClickOn = False
        self.mousePos = (0.0, 0.0)
        self.fillPolygon = True

def cursor_pos_callback(window, x, y):
    global Controlador
    Controlador.mouse_pos = (x, y)

def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        Controlador.fillPolygon = not Controlador.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    elif key == glfw.KEY_O:
        Controlador.size -= 0.01

    elif key == glfw.KEY_P:
        Controlador.size += 0.01

def mouse_button_callback(window, button, action, mods):

    global controller

    if (action == glfw.PRESS or action == glfw.REPEAT):
        if (button == glfw.MOUSE_BUTTON_1):
            Controlador.leftClickOn = True

        if (button == glfw.MOUSE_BUTTON_2):
            Controlador.rightClickOn = True

    elif (action ==glfw.RELEASE):
        if (button == glfw.MOUSE_BUTTON_1):
            Controlador.leftClickOn = False
        if (button == glfw.MOUSE_BUTTON_2):
            Controlador.rightClickOn = False

class Principal_move: #movimiento del personaje

    def __init__(self):
        self.position = np.zeros(3)
        self.plinterna = np.zeros(3)
        self.angle = np.pi * 0.5
        self.phi = 0.0

    def move(self, window, viewPos, forward, new_side, dt):

        if (Controlador.leftClickOn):
            self.position[1] += 2.5* dt
            self.plinterna[1] += 3*dt
            viewPos += forward * dt * 10

        elif (Controlador.rightClickOn):
            self.position[1] -= 2.5* dt
            self.plinterna[1] -= 3*dt
            viewPos -= forward * dt * 10

        return self.position

    def angulo(self, dx, dz, dt):

        self.phi -= dx * dt * 0.5
        angle_0 = self.angle

        dangle = dz * dt * 0.5
        self.angle += dangle

        if self.angle < 0:
            self.angle = 0.01

        elif self.angle > np.pi:
            self.angle = 3.14159

        return self.phi, self.angle

class Principal_dibujo: #dibujo del personaje
    def __init__(self):
        gpus=[]
        for i in range(12):
            gpuChar = es.GPUShape().initBuffers()
            es.SimpleTextureModelViewProjectionShaderProgram().setupVAO(gpuChar)

            shapeChar = createNewTextureQuad(i/12,(i + 1)/12,3/4,1)
            gpuChar.fillBuffers(shapeChar.vertices, shapeChar.indices, GL_STATIC_DRAW)
            gpuChar.texture = es.textureSimpleSetup(
                getAssetPath("spritet2v2.png"), GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)
            gpus.append(gpuChar)

        self.position = np.zeros(3)
        self.angle = 0

        self.sprite = gpus

    def update(self,new_pos,angle):
        self.position[0] = new_pos[0]
        self.position[1] = new_pos[1]
        self.position[2] = new_pos[2]
        self.angle = angle

    
    def position_in_matrix(self,matriz):
        for i in range(len(matriz)):
            for i in range(len(matriz[i])):
                return


    def draw(self,pipeline,actual_sprite):
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        phi = self.angle
        tex = self.sprite[actual_sprite]

        charNode =sg.SceneGraphNode("ctexture")
        charNode.transform =tr.matmul([tr.rotationX(np.pi/2),tr.scale(0,0.8,0.3)])
        charNode.childs += [tex]
        char_tr=sg.SceneGraphNode("char_tr")
        char_tr.childs += [charNode]

        char_tr.transform = tr.matmul([tr.translate(x,y,z),tr.rotationZ(phi)])

        sg.drawSceneGraphNode(char_tr,pipeline,"model")


Movimiento = Principal_move() 
Controlador = Controller() 