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
import sys

SIZE_IN_BYTES = 4

class Controller:
    def __init__(self):
        self.superglasses = True
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

    if key == glfw.KEY_SPACE and action ==glfw.PRESS:
        controller.superglasses = not controller.superglasses
    
    elif key == glfw.KEY_ESCAPE and action ==glfw.PRESS:
        glfw.set_window_should_close(window, True)


if __name__ == "__main__":
    if len(sys.argv)!=5:
        print("input incorrecto: distinta cantidad de inputs")
        exit()
    elif (int(sys.argv[1]))<0:
        print("input incorrecto: los zombies tiene un valor negativo")
        exit()
    elif (int(sys.argv[2]))<0:
        print("input incorrecto: los humanos tiene un valor negativo")
        exit()
    elif (int(sys.argv[3]))<0:
        print("input incorrecto: el tiempo debe ser positivo")
        exit()
    elif (float(sys.argv[4]))<0 or (float(sys.argv[4]))>1:
        print("input incorrecto: probabilidades fuera de rango")
        exit()
    Z=(int(sys.argv[1])) #Cantidad de Zombies por ronda
    H= (int(sys.argv[2])) #cantidad de Humanos por ronda
    T=(int(sys.argv[3])) #tiempo entre cada ronda
    P=(float(sys.argv[4])) #Probabilidad

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
    
    # Connecting the callback function 'on_key' to handle keyboard events
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

    #Pantallas de inicio y termino
    victoryScreentex =  createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "sprites/Win.png") ###falta

    loseScreentex =  createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "sprites/Lose.png") ##falta


    victoryScreenNode  = sg.SceneGraphNode("victoryScreen")
    victoryScreenNode.childs = [victoryScreentex]

    loseScreenNode = sg.SceneGraphNode("loseScreen")
    loseScreenNode.childs = [loseScreentex]

    #Se crea la lista que irá guardando los personajes
    body_list=[]

    #Se asigna el player
    player = Player(0.2)
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

        if t1-dt > T:
            dt=t1
            for i in range(Z):
                NewBoros=Body()
                NewBoros.boroizacion()
                body_list.append(NewBoros)

        if t1-dt1 > T:
            dt1=t1
            for i in range(H):
                body_list.append(Body())

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller statea
        if (controller.superglasses):
            for i in body_list:
                i.spacechange2()
                player.spacechange2()
        else:
            for i in body_list:
                i.spacechange1()
                player.spacechange1()
                

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

        for i in body_list:
            i.is_infected(P)
            i.movement(t1)
            i.collision(body_list)
            i.draw(tex_pipeline)
        
        #Interacciones
        if not store1.victory and not player.notalive:
            store1.collision(player)
            player.collision(body_list)
            player.is_infected(P)
            player.draw(tex_pipeline)

        elif store1.victory:
            sg.drawSceneGraphNode(victoryScreenNode,tex_pipeline,"transform")

        elif player.notalive:
            sg.drawSceneGraphNode(loseScreenNode,tex_pipeline,"transform")

        glfw.swap_buffers(window)

    #Freeing GPU memory
    mainScene.clear()
    tex_scene.clear()
    
    glfw.terminate()