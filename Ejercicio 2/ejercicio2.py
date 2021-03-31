import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
from gpu_shape import GPUShape, SIZE_IN_BYTES

class Controller:
    """
    Clase controlador que guardar las variables a modificar en la funcion on_key
    """
    fillPolygon = True 
    effect1 = False 
    effect2 = False 


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

    # Si detecta la tecla [Q] cambia el estado del efecto 1 : Achicar
    elif key == glfw.KEY_Q:
        controller.effect1 = not controller.effect1

    # Si detecta la tecla [W] cambia el estado del efecto 2 : Anochecer
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

class NocheShaderProgram:
    """
    Clase para guardar el los shaders compilados
    Contiene los shaders para el efecto de achicar
    """

    def __init__(self):

        # Vertex shader no se modifica
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
        # Se modifica el fragment shader para cambiar los colores a una tonalidad oscura
        fragment_shader = """
            #version 130
            in vec3 newColor;

            out vec4 outColor;
            void main()
            {   
                float newRed = newColor.r - 0.6; // Se modifica la componente roja
                float newGreen = newColor.g - 0.6; // Se modifica la componente Achicar
                float newBlue = newColor.b - 0.5; // Se modifica la componente azul
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

class ChicoShaderProgram:
    """
    Clase para guardar el los shaders compilados
    Contiene los shaders basicos (sin efectos)
    """
    def __init__(self):
        
        #Se modifican el vertex shader para achicar la imagen
        vertex_shader = """
            #version 130

            in vec3 position;
            in vec3 color;

            out vec3 newColor;
            void main()
            {
                vec3 newpos = vec3(position[0]/3, position[1]/3,position[2]/3);
                gl_Position = vec4(newpos, 1.0f);
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

    """
    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -1.0, y0, 0.0,  0.3, 1.0, 1.0,
         1.0, y0, 0.0,  0.3, 1.0, 1.0,
         1.0, y1, 0.0,  0.8, 1.0, 1.0,
        -1.0, y1, 0.0,  0.8, 1.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,
                2, 3, 0]

    return Shape(vertices, indices)


def create_pilar(y0, y1):
    """
    Funcion para crear rectangulo que represente el pilar de la corona


    """
    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -0.20, y0, 0.0,  0.64, 0.64, 0.75,
         0.20, y0, 0.0,  0.64, 0.64, 0.75,
         0.20, y1, 0.0,  0.50, 0.50, 0.75,
        -0.20, y1, 0.0,  0.50, 0.50, 0.75]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,
                2, 3, 0]

    return Shape(vertices, indices)
    

def create_corsup(y0, y1):
    """
    Funcion para crear rectangulo que represente la parte superior de la corona

    """
    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -0.3, y0, 0.0,  1.0, 0.85, 0.1,
         0.3, y0, 0.0,  1.0, 0.85, 0.1,
         0.4, y1, 0.0,  1.0, 1.0, 0.3,
        -0.4, y1, 0.0,  1.0, 1.0, 0.3]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,
                2, 3, 0]

    return Shape(vertices, indices)


def create_corinf(y0, y1):
    """
    Funcion para crear rectangulo que represente la parte inferior de la corona

    """
    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -0.35, y0, 0.0,  1.0, 0.8, 0.0,
         0.35, y0, 0.0,  1.0, 0.8, 0.0,
         0.3, y1, 0.0,   1.0, 0.85, 0.1,
        -0.3, y1, 0.0,   1.0, 0.85, 0.1]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,
                2, 3, 0]

    return Shape(vertices, indices)

def create_triangulo(y0,y1):
    """
    Funcion para crear rectangulo que represente los triangulos de la corona

    """
    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions                           colors
         -0.4, y1 ,               0.0,  0.64, 1.0, 1.0,
         -0.14, y1 ,              0.0,  0.64, 1.0, 1.0,
         -0.27, y0 ,              0.0,  0.4, 1.0, 1.0,

         -0.14 , y1 ,             0.0,  0.64, 1.0, 1.0,
         0.12, y1 ,               0.0,  0.64, 1.0, 1.0,
         -0.01, y0 ,              0.0,  0.4, 1.0, 1.0,

         0.12, y1 ,               0.0,  0.64, 1.0, 1.0,
         0.4, y1 ,                0.0,  0.64, 1.0, 1.0,
         0.25, y0,                0.0,  0.4, 1.0, 1.0]
        

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,
               3 , 4, 5,
               6, 7, 8]

    return Shape(vertices, indices)

def create_franja(y0, y1):
    """
    Funcion para crear rectangulo que representa una franja

    """
    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -0.31, y0, 0.0,  1.0, 0.0, 0.0,
         0.31, y0, 0.0,  1.0, 0.0, 0.0,
         0.3, y1, 0.0,   1.0, 0.5, 0.5,
        -0.3, y1, 0.0,   1.0, 0.5, 0.5]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,
                2, 3, 0]

    return Shape(vertices, indices)

def create_rubi(y0, y1,y2):
    """
    Funcion para crear rectangulo que representa un rubi

    """
    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        0.0, y0, 0.0,   1.0, 0.4, 0.4,
        0.03, y1, 0.0,  1.0, 0.2, 0.2,
        0, y2, 0.0,     1.0, 0.0, 0.0,
        -0.03, y1, 0.0,  1.0, 0.2, 0.2]

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
    window = glfw.create_window(width, height, "Ejercicio 2", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)
    
    # Creamos las instancias de los ShaderProgram, que compila los shaders creados
    simplePipeline = SimpleShaderProgram() # Shaders normales
    ChicoPipeline = ChicoShaderProgram() # Shaders para efecto achicar
    NochePipeline = NocheShaderProgram() #Shaders para efecto anochecer

    """
    Se crea cada figura en la memoria de la GPU.
    Es importante recordar que se debe hacer setupVAO a cada shaderProgram con cada figura 
    que desea dibujar
    """

    # 1- Creamos la Figura del cielo en la GPU
    sky_shape = create_sky(y0=-1, y1=1.0) # Creamos los vertices e indices (guardandolos en un objeto shape)
    gpu_sky = GPUShape().initBuffers() # Se le pide memoria a la GPU para guardar la figura
    simplePipeline.setupVAO(gpu_sky) # Se le dice al ShaderProgram NORMAL como leer esta parte de la memoria 
    ChicoPipeline.setupVAO(gpu_sky) # Se le dice al ShaderProgram del EFECTO 1 (Achicar) como leer esta parte de la memoria 
    NochePipeline.setupVAO(gpu_sky) # Se le dice al ShaderProgram del EFECTO 2 (Anochecer) como leer esta parte de la memoria 
    gpu_sky.fillBuffers(sky_shape.vertices, sky_shape.indices, GL_STATIC_DRAW) # Llenamos esta memoria de la GPU con los vertices e indices

    # 2- Creamos la Figura del pilar en la GPU
    pilar_shape = create_pilar(y0=-1, y1=0.0) # Creamos los vertices e indices (guardandolos en un objeto shape)
    gpu_pilar = GPUShape().initBuffers() # Se le pide memoria a la GPU para guardar la figura
    simplePipeline.setupVAO(gpu_pilar) # Se le dice al ShaderProgram NORMAL como leer esta parte de la memoria 
    ChicoPipeline.setupVAO(gpu_pilar) # Se le dice al ShaderProgram del EFECTO 1 (Achicar) como leer esta parte de la memoria 
    NochePipeline.setupVAO(gpu_pilar) # Se le dice al ShaderProgram del EFECTO 2 (Anochecer) como leer esta parte de la memoria 
    gpu_pilar.fillBuffers(pilar_shape.vertices, pilar_shape.indices, GL_STATIC_DRAW) # Llenamos esta memoria de la GPU con los vertices e indices

     # 3- Creamos la Figura de la corinf en la GPU
    corsup_shape = create_corsup(y0=0.075, y1=0.4) # Creamos los vertices e indices (guardandolos en un objeto shape)
    gpu_corsup = GPUShape().initBuffers() # Se le pide memoria a la GPU para guardar la figura
    simplePipeline.setupVAO(gpu_corsup) # Se le dice al ShaderProgram NORMAL como leer esta parte de la memoria 
    ChicoPipeline.setupVAO(gpu_corsup) # Se le dice al ShaderProgram del EFECTO 1 (Achicar) como leer esta parte de la memoria 
    NochePipeline.setupVAO(gpu_corsup) # Se le dice al ShaderProgram del EFECTO 2 (Anochecer) como leer esta parte de la memoria 
    gpu_corsup.fillBuffers(corsup_shape.vertices, corsup_shape.indices, GL_STATIC_DRAW) # Llenamos esta memoria de la GPU con los vertices e indices

    # 4- Creamos la Figura del corinf en la GPU 
    corinf_shape = create_corinf(y0=0.0, y1=0.075) # Creamos los vertices e indices (guardandolos en un objeto shape)
    gpu_corinf = GPUShape().initBuffers() # Se le pide memoria a la GPU para guardar la figura
    simplePipeline.setupVAO(gpu_corinf) # Se le dice al ShaderProgram NORMAL como leer esta parte de la memoria 
    ChicoPipeline.setupVAO(gpu_corinf) # Se le dice al ShaderProgram del EFECTO 1 (Achicar) como leer esta parte de la memoria 
    NochePipeline.setupVAO(gpu_corinf) # Se le dice al ShaderProgram del EFECTO 2 (Anochecer) como leer esta parte de la memoria 
    gpu_corinf.fillBuffers(corinf_shape.vertices, corinf_shape.indices, GL_STATIC_DRAW) # Llenamos esta memoria de la GPU con los vertices e indices

     # 5- Creamos la Figura del triangulo en la GPU
    triangulo_shape = create_triangulo(y0=0.3, y1=0.4) # Creamos los vertices e indices (guardandolos en un objeto shape)
    gpu_triangulo = GPUShape().initBuffers() # Se le pide memoria a la GPU para guardar la figura
    simplePipeline.setupVAO(gpu_triangulo) # Se le dice al ShaderProgram NORMAL como leer esta parte de la memoria 
    ChicoPipeline.setupVAO(gpu_triangulo) # Se le dice al ShaderProgram del EFECTO 1 (Achicar) como leer esta parte de la memoria 
    NochePipeline.setupVAO(gpu_triangulo) # Se le dice al ShaderProgram del EFECTO 2 (Anochecer) como leer esta parte de la memoria 
    gpu_triangulo.fillBuffers(triangulo_shape.vertices, triangulo_shape.indices, GL_STATIC_DRAW) # Llenamos esta memoria de la GPU con los vertices e indices

    # 6- Creamos la Figura de la franja en la GPU 
    franja_shape = create_franja(y0=0.06, y1=0.07) # Creamos los vertices e indices (guardandolos en un objeto shape)
    gpu_franja = GPUShape().initBuffers() # Se le pide memoria a la GPU para guardar la figura
    simplePipeline.setupVAO(gpu_franja) # Se le dice al ShaderProgram NORMAL como leer esta parte de la memoria 
    ChicoPipeline.setupVAO(gpu_franja) # Se le dice al ShaderProgram del EFECTO 1 (Achicar) como leer esta parte de la memoria 
    NochePipeline.setupVAO(gpu_franja) # Se le dice al ShaderProgram del EFECTO 2 (Anochecer) como leer esta parte de la memoria 
    gpu_franja.fillBuffers(franja_shape.vertices, franja_shape.indices, GL_STATIC_DRAW)

    # 6- Creamos la Figura de rubi en la GPU 
    rubi_shape = create_rubi(y0=0.1, y1=0.175, y2=0.25) # Creamos los vertices e indices (guardandolos en un objeto shape)
    gpu_rubi = GPUShape().initBuffers() # Se le pide memoria a la GPU para guardar la figura
    simplePipeline.setupVAO(gpu_rubi) # Se le dice al ShaderProgram NORMAL como leer esta parte de la memoria 
    ChicoPipeline.setupVAO(gpu_rubi) # Se le dice al ShaderProgram del EFECTO 1 (Achicar) como leer esta parte de la memoria 
    NochePipeline.setupVAO(gpu_rubi) # Se le dice al ShaderProgram del EFECTO 2 (Anochecer) como leer esta parte de la memoria 
    gpu_rubi.fillBuffers(rubi_shape.vertices, rubi_shape.indices, GL_STATIC_DRAW)


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
        Se usa el shaderProgram del efecto 1: Achicar
        """
        if (controller.effect1):
            # Se le dice a OpenGL que use el shaderProgram del efecto 1: Achicar
            glUseProgram(ChicoPipeline.shaderProgram)
            ChicoPipeline.drawCall(gpu_sky) # Se dibuja el cielo
            ChicoPipeline.drawCall(gpu_pilar) # Se dibuja el pilar
            ChicoPipeline.drawCall(gpu_corsup) # Se dibuja la corinf
            ChicoPipeline.drawCall(gpu_corinf) # Se dibuja el corinf
            ChicoPipeline.drawCall(gpu_triangulo) # Se dibuja el triangulo
            ChicoPipeline.drawCall(gpu_franja) # Se dibuja de la franja
            ChicoPipeline.drawCall(gpu_rubi) # Se dibuja el rubi
        # Si esta el efecto 2 activado (se activa o desactiva con la tecla [W]
        # Se usa el shaderProgram del efecto 2: Anochecer
        elif (controller.effect2):
            # Se le dice a OpenGL que use el shaderProgram del efecto 2: Anochecer
            glUseProgram(NochePipeline.shaderProgram)
            NochePipeline.drawCall(gpu_sky) # Se dibuja el cielo
            NochePipeline.drawCall(gpu_pilar) # Se dibuja el pilar
            NochePipeline.drawCall(gpu_corsup) # Se dibuja la corinf
            NochePipeline.drawCall(gpu_corinf) # Se dibuja el corinf
            NochePipeline.drawCall(gpu_triangulo) # Se dibuja el triangulo
            NochePipeline.drawCall(gpu_franja) # Se dibuja la franja
            NochePipeline.drawCall(gpu_rubi) # Se dibuja rubi
        # Si no hay un efecto activado
        # Se usa el shaderProgram normal
        else:
            # Se le dice a OpenGL que use el shaderProgram normal
            glUseProgram(simplePipeline.shaderProgram)
            simplePipeline.drawCall(gpu_sky) # Se dibuja el cielo
            simplePipeline.drawCall(gpu_pilar) # Se dibuja el pilar
            simplePipeline.drawCall(gpu_corsup) # Se dibuja la corinf
            simplePipeline.drawCall(gpu_corinf) # Se dibuja el corinf
            simplePipeline.drawCall(gpu_triangulo) # Se dibuja el triangulo
            simplePipeline.drawCall(gpu_franja) # Se dibuja ela franja
            simplePipeline.drawCall(gpu_rubi) # Se dibuja ela rubi

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpu_sky.clear()
    gpu_pilar.clear()
    gpu_corsup.clear()
    gpu_corinf.clear()
    gpu_triangulo.clear()
    gpu_franja.clear()
    gpu_rubi.clear()

    glfw.terminate()