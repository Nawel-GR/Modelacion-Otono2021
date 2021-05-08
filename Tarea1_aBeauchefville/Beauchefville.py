""" Beauchef Ville """

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

    


if __name__ == "__main__":

    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 700
    height = 700
    title = "BeauchefVille"
    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)
    glfw.set_key_callback(window, on_key)

    # Pipeline interpolacion y textura
    pipeline = es.SimpleTransformShaderProgram()
    tex_pipeline = es.SimpleTextureTransformShaderProgram()

    # Color base
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Transparencias
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    #Mainscene y tex_scene
    mainScene = createScene(pipeline)
    tex_scene = sg.SceneGraphNode("textureScene")

    #Tienda
    store = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "sprites/Supermarket.png")
    
    storeNode = sg.SceneGraphNode("store")
    storeNode.childs = [store]
    tex_scene.childs += [storeNode]

    store1 = Market(-0.8,0.7,0.4,0.5)
    store1.set_model(storeNode)
    store1.update()

    #Se crea la lista que irá guardando los personajes
    body_list=[]

    #Saitama (player)
    saitamabase = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "sprites/Saitama.png")
    
    saitamaNode = sg.SceneGraphNode("saitama")
    saitamaNode.childs = [saitamabase]
    tex_scene.childs += [saitamaNode]

    player = Player(0.2)
    player.set_model(saitamaNode)
    player.set_controller(controller)

   
    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    t0 = glfw.get_time()
    dt=0
    dt1=0

    while not glfw.window_should_close(window):
        # Variables del tiempo
        t1 = glfw.get_time()
        delta = t1 - t0
        t0 = t1

        if t1-dt > 8:
            dt=t1
            for i in range(3):
                NewBoros=Body()
                NewBoros.boroizacion()
                body_list.append(NewBoros)

        if t1-dt1 >6:
            dt1=t1
            for i in range(3):
                body_list.append(Body())

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller statea
        if (controller.fillPolygon):
            for i in body_list:
                i.spacechange2()
        else:
            for i in body_list:
                i.spacechange1()
                

        # Clearing the screen
        glClear(GL_COLOR_BUFFER_BIT)

        # Actualizacion de posiciones
        player.update(delta)

        # Grafo de escena principal
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(mainScene, pipeline, "transform")

        # texture escene
        glUseProgram(tex_pipeline.shaderProgram)
        sg.drawSceneGraphNode(tex_scene, tex_pipeline, "transform")

        #Interacciones
        store1.collision(player)
        player.collision(body_list)

        for i in body_list:
            i.is_infected(0.0001)
            i.movement(t1)
            i.collision(body_list)
            i.draw(tex_pipeline)

        glfw.swap_buffers(window)

    mainScene.clear()
    tex_scene.clear()
    
    glfw.terminate()
