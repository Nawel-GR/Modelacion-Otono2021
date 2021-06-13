"""
Nahuel Gómez, CC3501, 2020-1
Tarea 2_a
Vista
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import grafica.lighting_shaders as ls
import grafica.transformations as tr
import grafica.easy_shaders as es
from grafica.assets_path import getAssetPath
import modelo as pr
import controlador as crt

#test-------------------------
testcueva =  [
 [[2., 1., 0., 1.], #HPiso,HTecho,TPiso,TTecho
  [2., 1., 0., 1.],
  [2., 1., 0., 1.],
  [1., 1., 0., 1.],
  [1., 1., 0., 1.],
  [1., 1., 0., 1.],
  [1., 1., 0., 1.],
  [1., 1., 0., 1.],
  [1., 1., 0., 1.],
  [1., 1., 0., 1.]], # Hasta aquí llega x=0
 [[2., 1., 0., 1.],
  [0.1, 5., 0., 1.],
  [0.2, 5., 0., 1.],
  [0.2, 5., 0., 1.],
  [0.3, 5., 0., 1.],
  [0.4, 5., 0., 1.],
  [0.5, 5., 0., 1.],
  [0.6, 5., 0., 1.],
  [0.7, 5., 0., 1.],
  [1., 1., 0., 1.]], # Hasta aquí llega x=1
 [[0., 0., 1., 1.],
  [0.1, 0., 1., 1.],
  [0.2, 5., 1., 1.],
  [0.2, 5., 1., 1.],
  [0.3, 5., 1., 1.],
  [0.4, 5., 1., 1.],
  [0.5, 5., 1., 1.],
  [0.6, 5., 1., 1.],
  [0.7, 5., 1., 1.],
  [1., 1., 1., 1.]], # Hasta aquí llega x=2
 [[1., 1., 1., 1.],
  [0.1, 5., 1., 1.],
  [0.2, 5., 1., 1.],
  [0.2, 5., 1., 1.],
  [0.3, 5., 1., 1.],
  [0.4, 5., 1., 1.],
  [0.5, 5., 1., 1.],
  [0.6, 5., 1., 1.],
  [0.7, 5., 1., 1.],
  [1., 1., 1., 1.]], # Hasta aquí llega x=3
 [[1., 1., 1., 1.],
  [1., 1., 1., 1.],
  [1., 1., 1., 1.],
  [1., 1., 1., 1.],
  [1., 1., 1., 1.],
  [1., 1., 1., 1.],
  [1., 1., 5., 1.],
  [1., 1., 1., 1.],
  [1., 1., 1., 1.],
  [1., 1., 1., 1.]] # Hasta aquí llega x=4
  ]# Y = 10

cave = np.load("cave.npy")
cave = cave.tolist()

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 700
    height = 700

    window = glfw.create_window(width, height, "Gaussiana", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, crt.on_key)

    #Haciendo el callback para el mouse
    glfw.set_input_mode(window,glfw.CURSOR,glfw.CURSOR_DISABLED)
    glfw.set_cursor_pos_callback(window, crt.cursor_pos_callback)
    glfw.set_mouse_button_callback(window, crt.mouse_button_callback)

    # Assembling the shader program
    pipeline = es.SimpleModelViewProjectionShaderProgram()
    texpipeline = ls.SpotlightTexturePhongShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(texpipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.5, 0.5, 0.5, 1.0)

    # As we work in 3D, we need to check which part is in front, and which one is at the back
    glEnable(GL_DEPTH_TEST)
    
    # Gpu Techo
    Techo_mesh = pr._create(testcueva,1)
    shapeTecho = pr.toShape(Techo_mesh)

    gpuTecho_malla = es.GPUShape().initBuffers()
    texpipeline.setupVAO(gpuTecho_malla)
    gpuTecho_malla.fillBuffers(shapeTecho.vertices, shapeTecho.indices, GL_STATIC_DRAW)
    gpuTecho_malla.texture = es.textureSimpleSetup(getAssetPath("texturestest.png"), GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)

    # Gpu Piso
    Piso_mesh = pr._create(testcueva,0)
    shapePiso = pr.toShape(Piso_mesh)

    gpuPiso_malla = es.GPUShape().initBuffers()
    texpipeline.setupVAO(gpuPiso_malla)
    gpuPiso_malla.fillBuffers(shapePiso.vertices, shapePiso.indices, GL_STATIC_DRAW)
    gpuPiso_malla.texture = es.textureSimpleSetup(getAssetPath("texturestest.png"), GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)

    #Se incorpora personaje
    joven = crt.Principal_dibujo()

    #variables a utilizar
    t_0 = glfw.get_time()
    t2 = glfw.get_time()
    z_0,x_0 = 0. , 0.
    up = np.array((0., 0., 1.))
    viewPos = np.zeros(3)
    viewPos[2] = 2.0
    i=0
    personaje_pos = np.zeros(3)
    camera_theta = np.pi/4

    while not glfw.window_should_close(window):
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (crt.Controlador.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Getting the time difference from the previous iteration
        t_1 = glfw.get_time()
        dt = t_1 - t_0
        t_0 = t_1

        x_1, z_1 = glfw.get_cursor_pos(window)

        dz = z_1 - z_0
        z_0 = z_1

        dx = x_1 - x_0
        x_0 = x_1

        #Angulos de vision
        phi, theta = crt.Movimiento.angulo(dx, dz, dt)
        new_pi = phi + np.pi * 0.5 # Simple correction

        #Vector at
        at = np.array([np.cos(phi) * np.sin(theta), np.sin(phi) * np.sin(theta), np.cos(theta)])
        # We have to redefine our at and forward vectors now considering our character's position.
        new_at = at + viewPos
        forward = new_at - viewPos

        # Side vector, this helps us define our sideway movement
        new_side = np.array([np.cos(new_pi) * np.sin(theta), np.sin(new_pi) * np.sin(theta), 0])

        # Move character 
        crt.Movimiento.move(window, viewPos, forward, new_side, dt)

        # Setting camera (eye, at, up)
        update_at= at + viewPos
        view = tr.lookAt(viewPos,update_at,up)

        # Setting up the projection transform
        projection = tr.perspective(60, float(width)/float(height), 0.1, 100)

        glUniformMatrix4fv(glGetUniformLocation(texpipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

        glUniform3f(glGetUniformLocation(texpipeline.shaderProgram, "La"), 0.4, 0.4, 0.4)
        glUniform3f(glGetUniformLocation(texpipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(texpipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(texpipeline.shaderProgram, "Ka"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(texpipeline.shaderProgram, "Kd"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(texpipeline.shaderProgram, "Ks"), 0.0, 0.0, 0.0)

        glUniform3f(glGetUniformLocation(texpipeline.shaderProgram, "lightposition"),*crt.Movimiento.plinterna)
        glUniform3f(glGetUniformLocation(texpipeline.shaderProgram, "lightDirection"), *update_at)
        glUniform3f(glGetUniformLocation(texpipeline.shaderProgram, "viewPosition"), *viewPos)
        glUniform1ui(glGetUniformLocation(texpipeline.shaderProgram, "focused"),10)
        glUniform1ui(glGetUniformLocation(texpipeline.shaderProgram, "shininess"),2)       
        glUniform1f(glGetUniformLocation(texpipeline.shaderProgram, "constantAttenuation"), 1.0)
        glUniform1f(glGetUniformLocation(texpipeline.shaderProgram, "linearAttenuation"), 0.0)
        glUniform1f(glGetUniformLocation(texpipeline.shaderProgram, "quadraticAttenuation"), 0.0)        

        glUniformMatrix4fv(glGetUniformLocation(texpipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glUniformMatrix4fv(glGetUniformLocation(texpipeline.shaderProgram, "model"), 1, GL_TRUE, tr.uniformScale(1))
        
        #Drawcall
        texpipeline.drawCall(gpuPiso_malla)
        texpipeline.drawCall(gpuTecho_malla)
        
        t3 = glfw.get_time()
        dt1 = t2-t3
        t2 = t3

        personaje_pos[0]=new_at[0]
        personaje_pos[1]=new_at[1]

        if pr.up_z(Piso_mesh,personaje_pos) != None:
            personaje_pos[2]=pr.up_z(Piso_mesh,personaje_pos)+ 0.5
            viewPos[2]= personaje_pos[2]
        joven.update(personaje_pos,phi)

        if  (crt.Controlador.leftClickOn ):
            if i == 12 or i == -1 :                
                i =0
            joven.draw(texpipeline,i)
            i +=1

        elif crt.Controlador.rightClickOn:
            if i == -1 or i == 12:
                i = 11
            joven.draw(texpipeline,i)
            i -=1
        else:
            joven.draw(texpipeline,0)

        glfw.swap_buffers(window)

    glfw.terminate()
