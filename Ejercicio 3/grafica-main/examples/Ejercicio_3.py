# coding=utf-8
"""Ejercicio 3"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.gpu_shape as gs
import grafica.transformations as tr
from grafica.gpu_shape import GPUShape


# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4


# A class to store the application control
class Controller:
    fillPolygon = True


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    else:
        print('Unknown key')


def drawCall(shaderProgram, shape, mode=GL_LINES):
    # Binding the proper buffers
    glBindVertexArray(shape.vao)
    glBindBuffer(GL_ARRAY_BUFFER, shape.vbo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, shape.ebo)

    # Describing how the data is stored in the VBO
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)
    
    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    # This line tells the active shader program to render the active element buffer with the given size
    glDrawElements(GL_TRIANGLES, shape.size, GL_UNSIGNED_INT, None)


def createEarth(N):

    # Here the new shape will be stored
    gpuShape = GPUShape()

    # First vertex at the center, white color
    vertices = [0, 0, 0, 0.4, 0.4, 1.0]
    indices = []

    dtheta = 2 * np.pi / N

    for i in range(N):
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            0.5 * np.cos(theta), 0.5 * np.sin(theta), 0,

            # color generates varying between 0 and 1
                  0.0,       0.0, 0.2]

        # A triangle is created using the center, this and the next vertex
        indices += [0, i, i+1]

    # The final triangle connects back to the second vertex
    indices += [0, N, 1]

    vertices = np.array(vertices, dtype =np.float32)
    indices = np.array(indices, dtype= np.uint32)
        
    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertices) * SIZE_IN_BYTES, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * SIZE_IN_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape

def createSun(N):

    # Here the new shape will be stored
    gpuShape = GPUShape()

    # First vertex at the center, white color
    vertices = [0, 0, 0, 1.0, 1.0, 0.0]
    indices = []

    dtheta = 2 * np.pi / N

    for i in range(N):
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            0.5 * np.cos(theta), 0.5 * np.sin(theta), 0,

            # color generates varying between 0 and 1
                  0.15,       0.15, 0]

        # A triangle is created using the center, this and the next vertex
        indices += [0, i, i+1]

    # The final triangle connects back to the second vertex
    indices += [0, N, 1]

    vertices = np.array(vertices, dtype =np.float32)
    indices = np.array(indices, dtype= np.uint32)
        
    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertices) * SIZE_IN_BYTES, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * SIZE_IN_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape

def createMoon(N):

    # Here the new shape will be stored
    gpuShape = GPUShape()

    # First vertex at the center, white color
    vertices = [0, 0, 0, 1.0, 1.0, 1.0]
    indices = []

    dtheta = 2 * np.pi / N

    for i in range(N):
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            0.5 * np.cos(theta), 0.5 * np.sin(theta), 0,

            # color generates varying between 0 and 1
                  0.15,       0.15, 0.15]

        # A triangle is created using the center, this and the next vertex
        indices += [0, i, i+1]

    # The final triangle connects back to the second vertex
    indices += [0, N, 1]

    vertices = np.array(vertices, dtype =np.float32)
    indices = np.array(indices, dtype= np.uint32)
        
    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertices) * SIZE_IN_BYTES, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * SIZE_IN_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape

def createLine(N):

    # Here the new shape will be stored
    gpuShape = GPUShape()

    # First vertex at the center, white color
    vertices = [0.5* np.cos(0), 0.5 * np.sin(0), 0, 1.0, 1.0, 1.0]
    indices = []
    dtheta = 2 * np.pi / N
    

    i=0 
    while i <= N:
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            0.5 * np.cos(theta), 0.5 * np.sin(theta), 0,

            # color generates varying between 0 and 1
                  1, 1, 1]

        # A triangle is created using the center, this and the next vertex
        indices += [i, i+1]
        i+=1

    # The final triangle connects back to the second vertex
    indices += [N, 0]
    

    vertices = np.array(vertices, dtype =np.float32)
    indices = np.array(indices, dtype= np.uint32)
        
    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertices) * SIZE_IN_BYTES, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * SIZE_IN_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape

def createCirc(N):

    # Here the new shape will be stored
    gpuShape = GPUShape()

    # First vertex at the center, white color
    vertices = [0.5* np.cos(0), 0.5 * np.sin(0), 0, 1.0, 1.0, 1.0]
    indices = []
    dtheta = 2 * np.pi / N
    

    i=0 
    while i <= N:
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            0.5 * np.cos(theta), 0.5 * np.sin(theta), 0,

            # color generates varying between 0 and 1
                  1, 1, 1]

        # A triangle is created using the center, this and the next vertex
        indices += [i, i+1]
        i+=2

    # The final triangle connects back to the second vertex
    indices += [N, 0]
    

    vertices = np.array(vertices, dtype =np.float32)
    indices = np.array(indices, dtype= np.uint32)
        
    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertices) * SIZE_IN_BYTES, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * SIZE_IN_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape



if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Displaying multiple shapes - Modern OpenGL", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Defining shaders for our pipeline
    vertex_shader = """
    #version 130
    in vec3 position;
    in vec3 color;

    out vec3 fragColor;

    uniform mat4 transform;

    void main()
    {
        fragColor = color;
        gl_Position = transform * vec4(position, 1.0f);
    }
    """

    fragment_shader = """
    #version 130

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {
        outColor = vec4(fragColor, 1.0f);
    }
    """

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))
    
    # Telling OpenGL to use our shader program
    glUseProgram(shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.1, 0.1, 0.1, 1.0)

    # Creating shapes on GPU memory
    gpuEarth = createEarth(100)
    gpuSun = createSun(100)
    gpuMoon = createMoon(100)
    gpuLine = createLine(300)
    gpuCirc = createCirc(100)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Using the time as the theta parameter
        theta = glfw.get_time()/2
        alpha = (glfw.get_time())

        #Line
        lineTransform = tr.matmul([
            tr.uniformScale(1.5)
        ])
        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_TRUE, lineTransform)
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        drawCall(shaderProgram, gpuLine, mode=GL_LINES)
        

        #Line
        lineTransform2 = tr.matmul([
            tr.translate(np.cos(theta)*3/4, np.sin(theta)*3/4, 0),
            tr.uniformScale(0.5)
        ])
        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_TRUE, lineTransform2)
        
        drawCall(shaderProgram, gpuLine, mode=GL_LINES)
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        
        # Sol 
        sunTransform = tr.matmul([
            tr.translate(0.0, 0.0, 0.0),
            tr.uniformScale(0.40)
        ])

        # updating the transform attribute
        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_TRUE, sunTransform)

        # drawing function
        drawCall(shaderProgram, gpuSun)

        # Tierra 
        earthTransform = tr.matmul([
            tr.translate(np.cos(theta)*3/4, np.sin(theta)*3/4, 0),
            tr.rotationZ(theta),
            tr.uniformScale(0.20)
        ])
        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_TRUE, earthTransform)
        drawCall(shaderProgram, gpuEarth)

        #Luna
        moonTransform = tr.matmul([
            tr.translate(np.cos(theta)*3/4+np.cos(alpha)*1/4, np.sin(theta)*3/4+np.sin(alpha)*1/4, 0),
            tr.rotationZ(theta),
            tr.uniformScale(0.1)
        ])
        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_TRUE, moonTransform)
        drawCall(shaderProgram, gpuMoon)


        #Circ
        circTransform = tr.matmul([
            tr.uniformScale(0.4)
        ])
        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_TRUE, circTransform)
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        drawCall(shaderProgram, gpuLine, mode=GL_LINES)
        


        #Circ
        circTransform2 = tr.matmul([
            tr.translate(np.cos(theta)*3/4, np.sin(theta)*3/4, 0),
            tr.uniformScale(0.2)
        ])
        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_TRUE, circTransform2)
        
        drawCall(shaderProgram, gpuLine, mode=GL_LINES)
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)


        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuSun.clear()
    gpuEarth.clear()
    gpuMoon.clear()
    gpuLine.clear()
    gpuCirc.clear()

    
    glfw.terminate()