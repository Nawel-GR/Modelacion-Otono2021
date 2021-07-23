import grafica.scene_graph as sg
import grafica.transformations as tr
import grafica.easy_shaders as es
import grafica.newLightShaders as nl
import Modelo as mod
import Pieza as pr
import numpy as np
import glfw


class objeto:
    def __init__(self):

        pieza = sg.SceneGraphNode("Vara")
        pieza.transform = tr.matmul([tr.rotationZ(np.pi/2),tr.scale(2,2,0)])
        pieza.childs = [pr.createStick(es.SimpleTransformShaderProgram())] 

        piece_tr = sg.SceneGraphNode("pieza_tr")
        piece_tr.childs = [pieza]

        self.posicion = np.zeros(3)
        self.posicion[0] = 0
        self.posicion[1] = 0.5       
        self.posicion[2] = 0  
        self.object = piece_tr
        self.angle = 0


    def draw(self,pipeline):
        x=self.posicion[0]
        y=self.posicion[1]
        z=self.posicion[2]
        self.object.transform = tr.matmul([tr.translate(x,y,z),tr.rotationZ(np.pi/4),tr.scale(2,2,1)])
        sg.drawSceneGraphNode(self.object, pipeline, "model")

# Clase para manejar una camara que se mueve en coordenadas polares
class PolarCamera:
    def __init__(self):
        self.center = np.array([0.0, 0.0, -0.5]) # centro de movimiento de la camara y donde mira la camara
        self.theta = 0                           # coordenada theta, angulo de la camara
        self.rho = 5                             # coordenada rho, distancia al centro de la camara
        self.eye = np.array([0.0, 0.0, 0.0])     # posicion de la camara
        self.height = 0.5                        # altura fija de la camara
        self.up = np.array([0, 0, 1])            # vector up
        self.viewMatrix = None                   # Matriz de vista
    
    # Añadir ángulo a la coordenada theta 
    def set_theta(self, delta):
        self.theta = (self.theta + delta) % (np.pi * 2)

    # Añadir distancia a la coordenada rho, sin dejar que sea menor o igual a 0
    def set_rho(self, delta):
        if ((self.rho + delta) > 0.1):
            self.rho += delta
    
    # Actualizar la matriz de vista
    def update_view(self):
        # Se calcula la posición de la camara con coordenadas poleras relativas al centro
        self.eye[0] = self.rho * np.sin(self.theta) + self.center[0]
        self.eye[1] = self.rho * np.cos(self.theta) + self.center[1]
        self.eye[2] = self.height + self.center[2]

        # Se genera la matriz de vista
        viewMatrix = tr.lookAt(
            self.eye,
            self.center,
            self.up
        )
        return viewMatrix

# Clase para manejar el controlador y la camara polar
class Controller:

    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True

        # Variables para controlar la camara
        self.is_up_pressed = False
        self.is_down_pressed = False
        self.is_left_pressed = False
        self.is_right_pressed = False
        self.Q_value = 0.0
        self.A_value = 0.0

        # Se crea instancia de la camara
        self.polar_camera = PolarCamera()

    # Entregar la referencia a la camara
    def get_camera(self):
        return self.polar_camera

    # Metodo para ller el input del teclado
    def on_key(self, window, key, scancode, action, mods):
        
        # Caso de detectar la tecla [UP], actualiza estado de variable
        if key == glfw.KEY_UP:
            if action == glfw.PRESS:
                self.is_up_pressed = True
            elif action == glfw.RELEASE:
                self.is_up_pressed = False

        # Caso de detectar la tecla [DOWN], actualiza estado de variable
        if key == glfw.KEY_DOWN:
            if action == glfw.PRESS:
                self.is_down_pressed = True
            elif action == glfw.RELEASE:
                self.is_down_pressed = False

        # Caso de detectar la tecla [RIGHT], actualiza estado de variable
        if key == glfw.KEY_RIGHT:
            if action == glfw.PRESS:
                self.is_right_pressed = True
            elif action == glfw.RELEASE:
                self.is_right_pressed = False

        # Caso de detectar la tecla [LEFT], actualiza estado de variable
        if key == glfw.KEY_LEFT:
            if action == glfw.PRESS:
                self.is_left_pressed = True
            elif action == glfw.RELEASE:
                self.is_left_pressed = False

        # Caso de detectar la barra espaciadora, se cambia el metodo de dibujo
        if key == glfw.KEY_SPACE:
            if action == glfw.PRESS:
                self.fillPolygon = not self.fillPolygon
        if key == glfw.KEY_Q:
            if action == glfw.PRESS:
                print("previa: ", self.Q_value)
                self.Q_value += 0.02
                print("siguiente ", self.Q_value)

        if key == glfw.KEY_W:
            if action == glfw.PRESS:
                print("previa: ", self.Q_value)
                self.Q_value -= 0.02
                print("siguiente ", self.Q_value)

        if key == glfw.KEY_A:
            if action == glfw.PRESS:
                print("previa: ", self.A_value)
                self.Q_value += 0.02
                print("siguiente ", self.A_value)

        if key == glfw.KEY_S:
            if action == glfw.PRESS:
                print("previa: ", self.A_value)
                self.Q_value -= 0.02
                print("siguiente ", self.A_value)

        # Caso en que se cierra la ventana
        if key == glfw.KEY_ESCAPE:
            if action == glfw.PRESS:
                glfw.set_window_should_close(window, True)

        # Caso de detectar Control izquierdo, se cambia el metodo de dibujo
        elif key == glfw.KEY_LEFT_CONTROL:
            if action == glfw.PRESS:
                self.showAxis = not self.showAxis


    #Funcion que recibe el input para manejar la camara y controlar sus coordenadas
    def update_camera(self, delta):
        # Camara rota a la izquierda
        if self.is_left_pressed:
            self.polar_camera.set_theta(-2 * delta)

        # Camara rota a la derecha
        if self.is_right_pressed:
            self.polar_camera.set_theta( 2 * delta)
        
        # Camara se acerca al centro
        if self.is_up_pressed:
            self.polar_camera.set_rho(-5 * delta)

        # Camara se aleja del centro
        if self.is_down_pressed:
            self.polar_camera.set_rho(5 * delta)

class white_ball:
    def __init__(self) :
        self.Sphere = mod.createTexSphereNode(-1.,0.0,-0.9, nl.MultipleTexturePhongShaderProgram(),0,5)
        self.pos_ini = [-1,0,-0.9]
    
    def move(self,x,y,z):
        self.pos_ini[0] = x
        self.pos_ini[1] = y
        self.pos_ini[2] = z
        self.Sphere.transform = tr.translate(self.pos_ini[0],self.pos_ini[1], self.pos_ini[2])


    def draw_call(self,pipeline):
        sg.drawSceneGraphNode(self.Sphere, pipeline, "model")    


class Balls:

    def __init__(self) :

        self.Sphere = []
        k= 0
        for i in range(6):
            for j in range(3):
                self.Sphere.append(mod.createTexSphereNode(1.,0.0,-0.9, nl.MultipleTexturePhongShaderProgram(),j,i))
                k += 1
            if k == 15:
                break

    
    def pos_inicial(self):
        contador =[0,0]
        trans_coord = [np.sin(np.pi/3) * 0.05 *2, -0.05]

        for i in self.Sphere:
            
            i.transform = tr.translate(0.15 + trans_coord[0]* contador[0],trans_coord[1]*contador[1], 0)

            if contador[0] == contador[1]:
                contador[0] += 1
                contador[1] = -contador[0]

            else:
                contador[1] +=2 

    def draw_call(self,pipeline):
        for i in self.Sphere:
            sg.drawSceneGraphNode(i, pipeline, "model")
