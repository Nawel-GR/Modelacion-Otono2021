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

# A class to store the application control
class Controller:
    def __init__(self):
        self.leftClickOn = False
        self.theta = 0.0
        self.mousePos = (0.0, 0.0)
        self.fillPolygon = True

controller = Controller()

def cursor_pos_callback(window, x, y):
    global _controller
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

class Principal:

    def __init__(self):
        self.position = np.zeros(3)
        self.old_pos = 0, 0
        self.theta = np.pi * 0.5
        self.phi = 0.0
        self.mouse_sensitivity = 0.5

    def angulo(self, dx, dz, dt):

        self.phi -= dx * dt * self.mouse_sensitivity
        theta_0 = self.theta

        dtheta = dz * dt * self.mouse_sensitivity
        self.theta += dtheta

        if self.theta < 0:
            self.theta = 0.01

        elif self.theta > np.pi:
            self.theta = 3.14159

        else:
            pass

        # if (self.theta + dtheta) // np.pi == multiplo_inicial:
        #     self.theta += dtheta

        return self.phi, self.theta

    def move(self, window, viewPos, forward, new_side, dt):

        #if (glfw.get_key(window, glfw.KEY_A) == glfw.PRESS):
        #    self.position[0] -= 2 * dt
        #    viewPos += new_side * dt * 10

        #elif (glfw.get_key(window, glfw.KEY_D) == glfw.PRESS):
        #    self.position[0] += 2* dt
        #    viewPos -= new_side * dt * 10

        if (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS):
            self.position[1] += 2* dt
            viewPos += forward * dt * 10

        elif (glfw.get_key(window, glfw.KEY_S) == glfw.PRESS):
            self.position[1] -= 2* dt
            viewPos -= forward * dt * 10

        #elif (glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS):
        #    self.position[2] += 2* dt
        #    viewPos[2] += 2*dt 

        return self.position

# We will use the global controller as communication with the callback function
Controlador = Controller()
Lara = Principal()



