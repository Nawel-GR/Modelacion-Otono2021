import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
from gpu_shape import GPUShape, SIZE_IN_BYTES

class Controller:
    """
    Clase controlador que guardar las variables a modificar en la funcion on_key
    """
    fillPolygon = True # Variable que indica si se debe dibujar en modo lineas o rellenar los triangulos
    effect1 = False # Variable que guarda el estado del efecto 1 : verde (activado o desactivado)
    effect2 = False # Variable que guarda el estado del efecto 1 : atardecer (activado o desactivado)


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):
    """
    Funcion que recibe el input del teclado.
    Si no se detecta una tecla presionada, la funcion retorna
    """
    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    # Si detecta la tecla [Q] cambia el estado del efecto 1 : verde
    elif key == glfw.KEY_Q:
        controller.effect1 = not controller.effect1

    # Si detecta la tecla [W] cambia el estado del efecto 2 : atardecer
    elif key == glfw.KEY_W:
        controller.effect2 = not controller.effect2

    else:
        print('Unknown key')
    
class Shape:
    """
    Clase simple para guardar los vertices e indices
    """
    def __init__(self, vertices, indices):
        self.vertices = vertices
        self.indices = indices

class SimpleShaderProgram:
    """
    Clase para guardar el los shaders compilados
    Contiene los shaders basicos (sin efectos)
    """
    def __init__(self):

        vertex_shader = """
            #version 130

            in vec3 position;
            in vec3 color;

            out vec3 newColor;
            void main()
            {
                gl_Position = vec4(position, 1.0f);
                newColor = color;
            }
            """

        fragment_shader = """
            #version 130
            in vec3 newColor;

            out vec4 outColor;
            void main()
            {
                outColor = vec4(newColor, 1.0f);
            }
            """

        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))


    def setupVAO(self, gpuShape):
        """
        Se le "dice" al shader como leer los bytes de la gpuShape asignada
        """

        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        # 3d vertices + rgb color specification => 3*4 + 3*4 = 24 bytes
        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        color = glGetAttribLocation(self.shaderProgram, "color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        # Unbinding current vao
        glBindVertexArray(0)


    def drawCall(self, gpuShape, mode=GL_TRIANGLES):
        """
        Se dibuja la gpuShape
        """
        assert isinstance(gpuShape, GPUShape)

        # Binding the VAO and executing the draw call
        glBindVertexArray(gpuShape.vao)
        glDrawElements(mode, gpuShape.size, GL_UNSIGNED_INT, None)

        # Unbind the current VAO
        glBindVertexArray(0)

class GreenShaderProgram:
    """
    Clase para guardar el los shaders compilados
    Contiene los shaders para el efecto de solamente dibujar los pixeles con más componente verde
    """

    def __init__(self):

        # Vertex shader no de modifica
        vertex_shader = """
            #version 130

            in vec3 position;
            in vec3 color;

            out vec3 newColor;
            void main()
            {
                gl_Position = vec4(position, 1.0f);
                newColor = color;
            }
            """
        # Se modifica el fragment shader para descartar los fragmentos que tienen un componente verde bajo
        fragment_shader = """
            #version 130
            in vec3 newColor;

            out vec4 outColor;
            void main()
            {
                // Se guarda el promedio para tener un color gris del fragmento
                float grayColor = (newColor.r + newColor.g + newColor.b) / 3.0;

                // Se crea una nuevo vector para contener el color final
                vec3 finalColor = newColor;

                // Si la componente verde es menos que una de las otras dos componentes
                // Se descarta, asignando el color gris al color final
                if (newColor.g < newColor.r +0.1|| newColor.g < newColor.b +0.1)
                {
                    finalColor = vec3(grayColor, grayColor, grayColor);
                }

                // Si no cumple la condicion, el color final se manetiene igual al color original
                // Se asigna el color final al fragmento
                outColor = vec4(finalColor, 1.0f);
            }
            """

        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))


    def setupVAO(self, gpuShape):
        """
        Se le "dice" al shader como leer los bytes de la gpuShape asignada
        """

        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        # 3d vertices + rgb color specification => 3*4 + 3*4 = 24 bytes
        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        color = glGetAttribLocation(self.shaderProgram, "color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        # Unbinding current vao
        glBindVertexArray(0)


    def drawCall(self, gpuShape, mode=GL_TRIANGLES):
        """
        Se dibuja la gpuShape
        """
        assert isinstance(gpuShape, GPUShape)

        # Binding the VAO and executing the draw call
        glBindVertexArray(gpuShape.vao)
        glDrawElements(mode, gpuShape.size, GL_UNSIGNED_INT, None)

        # Unbind the current VAO
        glBindVertexArray(0)

class SunsetShaderProgram:
    """
    Clase para guardar el los shaders compilados
    Contiene los shaders para generar el efecto atardecer alterando las componentes del rgb
    """
    def __init__(self):
        # Vertex shader no de modifica
        vertex_shader = """
            #version 130

            in vec3 position;
            in vec3 color;

            out vec3 newColor;
            void main()
            {
                gl_Position = vec4(position, 1.0f);
                newColor = color;
            }
            """
         # Se modifica el fragment shader para alterar los comoponentes rgb del color original
        fragment_shader = """
            #version 130
            in vec3 newColor;

            out vec4 outColor;
            void main()
            {   
                float newRed = newColor.r + 0.4; // Se modifica la componente roja
                float newGreen = newColor.g + 0.2; // Se modifica la componente verde
                float newBlue = newColor.b * 0.1; // Se modifica la componente azul
                vec3 finalColor = vec3(newRed, newGreen, newBlue); // Se crea el nuevo vector rgb
                outColor = vec4(finalColor, 1.0f); // Se asigna el color final
            }
            """

        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))


    def setupVAO(self, gpuShape):
        """
        Se le "dice" al shader como leer los bytes de la gpuShape asignada
        """
        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        # 3d vertices + rgb color specification => 3*4 + 3*4 = 24 bytes
        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        color = glGetAttribLocation(self.shaderProgram, "color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        # Unbinding current vao
        glBindVertexArray(0)


    def drawCall(self, gpuShape, mode=GL_TRIANGLES):
        """
        Se dibuja la gpuShape
        """
        assert isinstance(gpuShape, GPUShape)

        # Binding the VAO and executing the draw call
        glBindVertexArray(gpuShape.vao)
        glDrawElements(mode, gpuShape.size, GL_UNSIGNED_INT, None)

        # Unbind the current VAO
        glBindVertexArray(0)

def create_sky(y0, y1):
    """
    Funcion para crear rectangulo que represente el cielo

    Parameters:
    y_0 (float): altura inferior donde empezara el rectangulo
    y_1 (float): altura superior donde termina el rectangulo
    """
    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -1.0, y0, 0.0,  0.0, 1.0, 1.0,
         1.0, y0, 0.0,  0.0, 1.0, 1.0,
         1.0, y1, 0.0,  0.8, 1.0, 1.0,
        -1.0, y1, 0.0,  0.8, 1.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,
                2, 3, 0]

    return Shape(vertices, indices)


def create_ocean(y0, y1):
    """
    Funcion para crear rectangulo que represente el oceano

    Parameters:
    y_0 (float): altura inferior donde empezara el rectangulo
    y_1 (float): altura superior donde termina el rectangulo
    """
    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -0.20, y0, 0.0,  0.0, 0.0, 0.5,
         0.20, y0, 0.0,  0.0, 0.0, 0.5,
         0.20, y1, 0.0,  0.2, 0.4, 1.0,
        -0.20, y1, 0.0,  0.2, 0.4, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,
                2, 3, 0]

    return Shape(vertices, indices)
    

def create_island(y0, y1):
    """
    Funcion para crear rectangulo que represente el oceano

    """
    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -0.25, y0, 0.0,  0.0, 0.0, 0.5,
         0.25, y0, 0.0,  0.0, 0.0, 0.5,
         0.2, y1, 0.0,  0.2, 0.4, 1.0,
        -0.2, y1, 0.0,  0.2, 0.4, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,
                2, 3, 0]

    return Shape(vertices, indices)


def create_volcano(y0, y1):
    """
    Funcion para crear rectangulo que represente el oceano

    """
    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -0.25, y0, 0.0,  0.0, 0.0, 0.5,
         0.25, y0, 0.0,  0.0, 0.0, 0.5,
         0.2, y1, 0.0,  0.2, 0.4, 1.0,
        -0.2, y1, 0.0,  0.2, 0.4, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,
                2, 3, 0]

    return Shape(vertices, indices)

if __name__ == "__main__":
    """
    Funcion o bloque que se ejecuta al correr el codigo
    """

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    # Dimensiones de la ventana de la aplicacion
    width = 800
    height = 800

    # Se crea la ventana con el titulo asignado
    window = glfw.create_window(width, height, "P5: Efectos con shaders", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)
    
    # Creamos las instancias de los ShaderProgram, que compila los shaders creados
    simplePipeline = SimpleShaderProgram() # Shaders normales
    greenPipeline = GreenShaderProgram() # Shaders para efecto verde
    sunsetPipeline = SunsetShaderProgram() #Shaders para efecto atardecer

    """
    Se crea cada figura en la memoria de la GPU.
    Es importante recordar que se debe hacer setupVAO a cada shaderProgram con cada figura 
    que desea dibujar
    """

    # 1- Creamos la Figura del cielo en la GPU
    sky_shape = create_sky(y0=-1, y1=1.0) # Creamos los vertices e indices (guardandolos en un objeto shape)
    gpu_sky = GPUShape().initBuffers() # Se le pide memoria a la GPU para guardar la figura
    simplePipeline.setupVAO(gpu_sky) # Se le dice al ShaderProgram NORMAL como leer esta parte de la memoria 
    greenPipeline.setupVAO(gpu_sky) # Se le dice al ShaderProgram del EFECTO 1 (VERDE) como leer esta parte de la memoria 
    sunsetPipeline.setupVAO(gpu_sky) # Se le dice al ShaderProgram del EFECTO 2 (ATARDECER) como leer esta parte de la memoria 
    gpu_sky.fillBuffers(sky_shape.vertices, sky_shape.indices, GL_STATIC_DRAW) # Llenamos esta memoria de la GPU con los vertices e indices

    # 2- Creamos la Figura del oceano en la GPU
    ocean_shape = create_ocean(y0=-1, y1=0.0) # Creamos los vertices e indices (guardandolos en un objeto shape)
    gpu_ocean = GPUShape().initBuffers() # Se le pide memoria a la GPU para guardar la figura
    simplePipeline.setupVAO(gpu_ocean) # Se le dice al ShaderProgram NORMAL como leer esta parte de la memoria 
    greenPipeline.setupVAO(gpu_ocean) # Se le dice al ShaderProgram del EFECTO 1 (VERDE) como leer esta parte de la memoria 
    sunsetPipeline.setupVAO(gpu_ocean) # Se le dice al ShaderProgram del EFECTO 2 (ATARDECER) como leer esta parte de la memoria 
    gpu_ocean.fillBuffers(ocean_shape.vertices, ocean_shape.indices, GL_STATIC_DRAW) # Llenamos esta memoria de la GPU con los vertices e indices

     # 3- Creamos la Figura de la isla en la GPU
    island_shape = create_island(y0=0.2, y1=0.3) # Creamos los vertices e indices (guardandolos en un objeto shape)
    gpu_island = GPUShape().initBuffers() # Se le pide memoria a la GPU para guardar la figura
    simplePipeline.setupVAO(gpu_island) # Se le dice al ShaderProgram NORMAL como leer esta parte de la memoria 
    greenPipeline.setupVAO(gpu_island) # Se le dice al ShaderProgram del EFECTO 1 (VERDE) como leer esta parte de la memoria 
    sunsetPipeline.setupVAO(gpu_island) # Se le dice al ShaderProgram del EFECTO 2 (ATARDECER) como leer esta parte de la memoria 
    gpu_island.fillBuffers(island_shape.vertices, island_shape.indices, GL_STATIC_DRAW) # Llenamos esta memoria de la GPU con los vertices e indices

    # 4- Creamos la Figura del volcan en la GPU 
    volcano_shape = create_volcano(y0=0.0, y1=0.055) # Creamos los vertices e indices (guardandolos en un objeto shape)
    gpu_volcano = GPUShape().initBuffers() # Se le pide memoria a la GPU para guardar la figura
    simplePipeline.setupVAO(gpu_volcano) # Se le dice al ShaderProgram NORMAL como leer esta parte de la memoria 
    greenPipeline.setupVAO(gpu_volcano) # Se le dice al ShaderProgram del EFECTO 1 (VERDE) como leer esta parte de la memoria 
    sunsetPipeline.setupVAO(gpu_volcano) # Se le dice al ShaderProgram del EFECTO 2 (ATARDECER) como leer esta parte de la memoria 
    gpu_volcano.fillBuffers(volcano_shape.vertices, volcano_shape.indices, GL_STATIC_DRAW) # Llenamos esta memoria de la GPU con los vertices e indices


    # Color de fondo de la visualizacion
    glClearColor(0.2, 0.2, 0.2, 1.0)

    # Loop principal que muestra las figuras
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

        """
        Si esta el efecto 1 activado (se activa o desactiva con la tecla [T]
        Se usa el shaderProgram del efecto 1: verde
        """
        if (controller.effect1):
            # Se le dice a OpenGL que use el shaderProgram del efecto 1: verde
            glUseProgram(greenPipeline.shaderProgram)
            greenPipeline.drawCall(gpu_sky) # Se dibuja el cielo
            greenPipeline.drawCall(gpu_ocean) # Se dibuja el oceano
            greenPipeline.drawCall(gpu_island) # Se dibuja la isla
            greenPipeline.drawCall(gpu_volcano) # Se dibuja el volcan
        # Si esta el efecto 2 activado (se activa o desactiva con la tecla [W]
        # Se usa el shaderProgram del efecto 2: atardecer
        elif (controller.effect2):
            # Se le dice a OpenGL que use el shaderProgram del efecto 2: atardecer
            glUseProgram(sunsetPipeline.shaderProgram)
            sunsetPipeline.drawCall(gpu_sky) # Se dibuja el cielo
            sunsetPipeline.drawCall(gpu_ocean) # Se dibuja el oceano
            sunsetPipeline.drawCall(gpu_island) # Se dibuja la isla
            sunsetPipeline.drawCall(gpu_volcano) # Se dibuja el volcan
        # Si no hay un efecto activado
        # Se usa el shaderProgram normal
        else:
            # Se le dice a OpenGL que use el shaderProgram normal
            glUseProgram(simplePipeline.shaderProgram)
            simplePipeline.drawCall(gpu_sky) # Se dibuja el cielo
            simplePipeline.drawCall(gpu_ocean) # Se dibuja el oceano
            simplePipeline.drawCall(gpu_island) # Se dibuja la isla
            simplePipeline.drawCall(gpu_volcano) # Se dibuja el volcan

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpu_sky.clear()
    gpu_ocean.clear()
    gpu_island.clear()
    gpu_volcano.clear()

    glfw.terminate()