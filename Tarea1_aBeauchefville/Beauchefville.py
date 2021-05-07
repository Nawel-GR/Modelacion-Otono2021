"""Tarea 1A BeauchefVille"""

import glfw
import OpenGL.GL.shaders
import numpy as np
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.performance_monitor as pm
import grafica.scene_graph as sg
from shapes import *
from model import *

SIZE_IN_BYTES = 4

class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.is_w_pressed = False
        self.is_s_pressed = False
        self.is_a_pressed = False
        self.is_d_pressed = False


#Global COntroller
controller = Controller()

def on_key(window, key, scancode, action, mods):
    
    global controller
    
    if key == glfw.KEY_W:
        if action ==glfw.PRESS:
            controller.is_w_pressed = True
        elif action == glfw.RELEASE:
            controller.is_w_pressed = False

    if key == glfw.KEY_S:
        if action ==glfw.PRESS:
            controller.is_s_pressed = True
        elif action == glfw.RELEASE:
            controller.is_s_pressed = False

    if key == glfw.KEY_A:
        if action ==glfw.PRESS:
            controller.is_a_pressed = True
        elif action == glfw.RELEASE:
            controller.is_a_pressed = False

    if key == glfw.KEY_D:
        if action ==glfw.PRESS:
            controller.is_d_pressed = True
        elif action == glfw.RELEASE:
            controller.is_d_pressed = False

    # Caso de detecar la barra espaciadora, se cambia el metodo de dibujo  -----------------------falta modificar
    if key == glfw.KEY_SPACE and action ==glfw.PRESS:
        controller.fillPolygon = not controller.fillPolygon

    # Caso en que se cierra la ventana
    elif key == glfw.KEY_ESCAPE and action ==glfw.PRESS:
        glfw.set_window_should_close(window, True)



if __name__ == "__main__":

    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 900
    height = 900
    title = "BeauchefVille"
    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)
    glfw.set_key_callback(window, on_key)

    # Pipeline interpolacion
    pipeline = es.SimpleTransformShaderProgram()

    # Pipeline texturas
    tex_pipeline = es.SimpleTextureTransformShaderProgram()

    # Color base
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Transparencias
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    mainScene = createScene(pipeline)



# Shape con textura de la carga
    garbage = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "sprites/bag.png")

    # Se crean dos nodos de carga
    garbage1Node = sg.SceneGraphNode("garbage1")
    #garbage1Node.transform = tr.translate(0.2, 0.55, 0.1)
    garbage1Node.childs = [garbage]


    # Se crean el grafo de escena con textura y se agregan las cargas
    tex_scene = sg.SceneGraphNode("textureScene")
    tex_scene.childs = [garbage1Node]

    # Se crean los modelos de la carga, se indican su nodo y se indica lo posicion inicial
    
    carga1 = Carga(0.2, 0.55, 0.1)
    carga1.set_model(garbage1Node)
    carga1.update()

    # Lista con todas las cargas
    cargas = [carga1]
#

    saitamabase = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "sprites/Saitama.png")
    saitamaNode = sg.SceneGraphNode("saitama")
    saitamaNode.childs = [saitamabase]

    tex_scene.childs += [saitamaNode]
    

    player = Player(0.3)
    # Se indican las referencias del nodo y el controller al modelo
    player.set_model(saitamaNode)
    player.set_controller(controller)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # tiempo
    glfw.swap_interval(0)
    t0 = glfw.get_time()    


    while not glfw.window_should_close(window):
        # Variables del tiempo
        t1 = glfw.get_time()
        delta = t1 - t0
        t0 = t1

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen
        glClear(GL_COLOR_BUFFER_BIT)

        # Detectar colisiones
        player.collision(cargas)

        # Actualizacion de posiciones
        player.update(delta)


        # Grafo de escena principal
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(mainScene, pipeline, "transform")

        # Grafo de escena con texturas
        glUseProgram(tex_pipeline.shaderProgram)
        sg.drawSceneGraphNode(tex_scene, tex_pipeline, "transform")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)


    # Free GPU
    mainScene.clear()
    tex_scene.clear()
    
    glfw.terminate()