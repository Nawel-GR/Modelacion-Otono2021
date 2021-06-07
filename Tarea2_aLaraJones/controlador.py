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
from grafica.assets_path import getAssetPath

import modelo as mod #se importa el modelo
import vista as vis #se importa la vista


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True


# We will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Gaussiana", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program
    pipeline = es.SimpleModelViewProjectionShaderProgram()
    texpipeline = es.SimpleTextureModelViewProjectionShaderProgram()

    # Telling OpenGL to use our shader program
    #glUseProgram(pipeline.shaderProgram)
    glUseProgram(texpipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    #Test Cueva
    Pisomesh = mod.crear_piso(vis.testcueva)

    # Obtenemos los vertices e indices
    Piso_vertices, Piso_indices = mod.get_vertexs_and_indexes_tex(Pisomesh)

    # Creamos la gpu y la inicializamos
    gpuPisoMalla = es.GPUShape().initBuffers()
    texpipeline.setupVAO(gpuPisoMalla)
    gpuPisoMalla.fillBuffers(Piso_vertices, Piso_indices, GL_STATIC_DRAW)
    gpuPisoMalla.texture = es.textureSimpleSetup(getAssetPath("textures.png"), GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)

    Techomesh = mod.crear_techo(vis.testcueva)

    # Obtenemos los vertices e indices
    Techo_vertices, Techo_indices = mod.get_vertexs_and_indexes_tex1(Techomesh)

    # Creamos la gpu y la inicializamos
    gpuTechoMalla = es.GPUShape().initBuffers()
    texpipeline.setupVAO(gpuTechoMalla)
    gpuTechoMalla.fillBuffers(Techo_vertices, Techo_indices, GL_STATIC_DRAW)
    gpuTechoMalla.texture = es.textureSimpleSetup(getAssetPath("textures.png"), GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)

    t0 = glfw.get_time()
    camera_theta = np.pi/4

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
            camera_theta -= 2 * dt

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
            camera_theta += 2* dt

        # Setting up the view transform

        camX =0.1+ np.sin(camera_theta)
        camY =0.1+  np.cos(camera_theta)

        viewPos = np.array([camX, camY, 1])

        view = tr.lookAt(
            viewPos,
            np.array([0,0,1.2]),
            np.array([0,0,1])
        )

        #glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(texpipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        # Setting up the projection transform
        projection = tr.perspective(60, float(width)/float(height), 0.1, 100)
        #glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(texpipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Drawing shapes with different model transformations
        #glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.uniformScale(1))
        #pipeline.drawCall(gpuMalla)
        
        glUniformMatrix4fv(glGetUniformLocation(texpipeline.shaderProgram, "model"), 1, GL_TRUE, tr.uniformScale(1))
        
        texpipeline.drawCall(gpuPisoMalla)
        texpipeline.drawCall(gpuTechoMalla)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()