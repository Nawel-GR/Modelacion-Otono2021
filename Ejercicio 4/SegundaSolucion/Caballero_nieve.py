# coding=utf-8
"""Textures and transformations in 2D"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys, os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grafica.gpu_shape import GPUShape, SIZE_IN_BYTES
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
from PIL import Image

__author__ = "Daniel Calderon"
__license__ = "MIT"


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.actual_sprite = 1
        self.x = 0.0

# global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    # Agregamos dos nuevas teclas para interactuar
    elif key == glfw.KEY_RIGHT:
        controller.x += 0.05
        controller.actual_sprite = (controller.actual_sprite + 1)%10
    
    elif key == glfw.KEY_LEFT:
        controller.x -= 0.05
        controller.actual_sprite = (controller.actual_sprite - 1)%10

    else:
        print('Unknown key')


if __name__ == "__main__":
    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Knight and snow", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # A simple shader program with position and texture coordinates as inputs.
    pipeline = es.SimpleTextureTransformShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.765, 0.765, 0.765, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    
    # Creamos una lista para guardar todas las gpu shapes necesarias
    gpus_K = [] #Knight
    gpus_B = [] #Background
    gpus_S = [] #Snow

    # Definimos donde se encuentra la textura
    thisFilePath = os.path.abspath(__file__)
    thisFolderPath = os.path.dirname(thisFilePath)
    spritesDirectory = os.path.join(thisFolderPath, "Sprites")
    spritePath = os.path.join(spritesDirectory, "sprites.png")
    backPath = os.path.join(spritesDirectory, "Fotofinal.png")
    snowPath = os.path.join(spritesDirectory, "Copitos.png")

    texture_K = es.textureSimpleSetup(
            spritePath, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)

    texture_B = es.textureSimpleSetup(
            backPath, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)

    texture_S = es.textureSimpleSetup(
            snowPath, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)


    # Creamos nieve en el fondo
    for i in range(10):
        shapeSnow = bs.createTextureQuad(0, 1,0,1)
        gpuSnow = GPUShape().initBuffers()
        pipeline.setupVAO(gpuSnow)

        gpuSnow.texture = texture_S

        gpuSnow.fillBuffers(shapeSnow.vertices, shapeSnow.indices, GL_STATIC_DRAW)

        gpus_S.append(gpuSnow)


    # Creamos una gpushape por cada frame de textura
    for i in range(10):
        gpuKnight = GPUShape().initBuffers()
        pipeline.setupVAO(gpuKnight)

        shapeKnight = bs.createTextureQuad(i/10,(i + 1)/10,0,1)

        gpuKnight.texture = texture_K

        gpuKnight.fillBuffers(shapeKnight.vertices, shapeKnight.indices, GL_STATIC_DRAW)

        gpus_K.append(gpuKnight)

    # Creamos una gpushape por cada frame del fondo
    for i in range(10):
        gpuBack = GPUShape().initBuffers()
        pipeline.setupVAO(gpuBack)

        shapeBack = bs.createTextureQuad(i/10,(i + 1)/10,0,1)

        gpuBack.texture = texture_B

        gpuBack.fillBuffers(shapeBack.vertices, shapeBack.indices, GL_STATIC_DRAW)

        gpus_B.append(gpuBack)

    ##time
    time1 = 0
    time2 = 0

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Drawing the shapes

        #trabajamos con la snow
        cont1= (glfw.get_time()/20)-time1
        cont2=(glfw.get_time()/20)-time2

        SnowTransform = tr.matmul([
        tr.translate(0.0-controller.x, 0.7-cont1, 0),
        tr.scale(10.0,4,0.0)
        ])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, SnowTransform)
        
        pipeline.drawCall(gpus_S[controller.actual_sprite])

        SnowTransform2 = tr.matmul([
        tr.translate(0.0-controller.x, 3-cont2, 0),
        tr.scale(10.0,4,0.0)
        ])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, SnowTransform2)
        
        pipeline.drawCall(gpus_S[controller.actual_sprite])

        if cont1>=3:
            time1=glfw.get_time()/20
        if cont2>=5:
            time2=glfw.get_time()/20 

        #Fondo
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.scale(2,1.5,0),
            tr.translate(0, -0.18, 0)
        ]))
        pipeline.drawCall(gpus_B[controller.actual_sprite])


        # Le entregamos al vertex shader la matriz de transformación Knight
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.uniformScale(0.5),
            tr.translate(0, -0.9, 0)
        ]))
        pipeline.drawCall(gpus_K[controller.actual_sprite])


        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuKnight.clear()
    gpuBack.clear()

    glfw.terminate()