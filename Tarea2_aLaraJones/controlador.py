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
import modelo as pr

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

    """
    glfw.MOUSE_BUTTON_1: left click
    glfw.MOUSE_BUTTON_2: right click
    glfw.MOUSE_BUTTON_3: scroll click
    """

    if (action == glfw.PRESS or action == glfw.REPEAT):
        if (button == glfw.MOUSE_BUTTON_1):
            Controlador.leftClickOn = True
            print("Mouse click - button 1")

        if (button == glfw.MOUSE_BUTTON_2):
            Controlador.rightClickOn = True
            print("Mouse click - button 2:", glfw.get_cursor_pos(window))

    elif (action ==glfw.RELEASE):
        if (button == glfw.MOUSE_BUTTON_1):
            Controlador.leftClickOn = False
        if (button == glfw.MOUSE_BUTTON_2):
            Controlador.rightClickOn = False

class Principal_move: #movimiento del personaje

    def __init__(self):
        self.position = np.zeros(3)
        self.poslinterna = np.zeros(3)
        self.angle = np.pi * 0.5
        self.phi = 0.0

    def move(self, window, viewPos, forward, new_side, dt):

        if (Controlador.leftClickOn):
            self.position[1] += 2.1* dt
            self.poslinterna[1] += 2.6*dt
            viewPos += forward * dt * 10

        elif (Controlador.rightClickOn):
            self.position[1] -= 2.1* dt
            self.poslinterna[1] -= 2.6*dt
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
            es.SimpleTextureTransformShaderProgram().setupVAO(gpuChar)

            shapeChar = createNewTextureQuad(i/12,(i + 1)/12,3/4,1)
            gpuChar.fillBuffers(shapeChar.vertices, shapeChar.indices, GL_STATIC_DRAW)
            gpuChar.texture = es.textureSimpleSetup(
                getAssetPath("Principal.png"), GL_CLAMP_TO_BORDER, GL_CLAMP_TO_BORDER, GL_NEAREST, GL_NEAREST)
            gpus.append(gpuChar)
        
        self.Personaje = gpus

        # Cuando ganamos se cambia el personaje por win
        WinCharGpu = es.GPUShape().initBuffers()
        es.SimpleTextureTransformShaderProgram().setupVAO(WinCharGpu)
        shapeWinChar = createNewTextureQuad(0,1,0,1)
        WinCharGpu.fillBuffers(shapeWinChar.vertices, shapeWinChar.indices, GL_STATIC_DRAW)
        WinCharGpu.texture = es.textureSimpleSetup(
            getAssetPath("Win.png"), GL_CLAMP_TO_BORDER, GL_CLAMP_TO_BORDER, GL_NEAREST, GL_NEAREST)

        winNode =sg.SceneGraphNode("winNode")
        winNode.transform =tr.matmul([tr.rotationX(np.pi/2),tr.scale(0,0.8,0.8)])
        winNode.childs += [WinCharGpu]
        Win_tr=sg.SceneGraphNode("winChar_tr")
        Win_tr.childs += [winNode]

        self.Win = Win_tr

        self.position = np.zeros(3)
        self.angle = 0

    def update(self,new_pos,angle):
        self.position[0] = new_pos[0]
        self.position[1] = new_pos[1]
        self.position[2] = new_pos[2]
        self.angle = angle

    def draw(self,pipeline,actual_Personaje):
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        phi = self.angle
        tex = self.Personaje[actual_Personaje]

        charNode =sg.SceneGraphNode("ctexture")
        charNode.transform =tr.matmul([tr.rotationX(np.pi/2),tr.scale(0,0.6,0.3)])
        charNode.childs += [tex]
        char_tr=sg.SceneGraphNode("char_tr")
        char_tr.childs += [charNode]

        char_tr.transform = tr.matmul([tr.translate(x,y,z),tr.rotationZ(phi)])

        sg.drawSceneGraphNode(char_tr,pipeline,"model")
    
    def win_draw(self,pipeline):
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        phi = self.angle

        self.Win.transform = tr.matmul([tr.translate(x,y,z),tr.rotationZ(phi)])

        sg.drawSceneGraphNode(self.Win,pipeline,"model")


class objeto:
    def __init__(self,x,y):

        pieza = sg.SceneGraphNode("Pieza")
        pieza.transform = tr.matmul([tr.rotationX(np.pi/2),tr.scale(0.5,0.5,1)])
        pieza.childs = [pr.createPiece(es.SimpleTransformShaderProgram())]

        piece_tr = sg.SceneGraphNode("pieza_tr")
        piece_tr.childs = [pieza]

        self.posicion = np.zeros(3)
        self.posicion[0] = np.random.randint(x-3)
        self.posicion[1] = np.random.randint(y-3)            
        self.object = piece_tr
        self.angle = 0

    def update_z(self,pos_z):
        self.posicion[2]  = pos_z

    def update_angle(self,newangle):
        self.angle = newangle    

    def take(self, pj_pos):
        if (abs(self.posicion[0]-pj_pos[0])<=0.2) and (abs(self.posicion[1]-pj_pos[1])<=0.2):
            return True
        else:
            return False

    def draw(self,pipeline):
        x=self.posicion[0]
        y=self.posicion[1]
        if self.posicion[2] == None:
            z=0.8
        z=self.posicion[2]+0.7
        phi = self.angle
        self.object.transform = tr.matmul([tr.translate(x,y,z),tr.rotationZ(phi+np.pi/2)])
        sg.drawSceneGraphNode(self.object, pipeline, "model")


Movimiento = Principal_move() 
Controlador = Controller() 