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
        self.obj = mod.createStick(es.SimpleModelViewProjectionShaderProgram())
        self.pos_ini = [-1.3,0,-1] 
        
    def move(self,x,y,z):
        self.pos_ini[0] = x
        self.pos_ini[1] = y
        self.pos_ini[2] = z
        self.obj.transform = tr.translate(self.pos_ini[0],self.pos_ini[1], self.pos_ini[2])

    def draw_call(self,pipeline2D):
        sg.drawSceneGraphNode(self.obj, pipeline2D, "model")



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

    def set_center(self,pos):
        self.center =pos
    
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
        self.W_value = 0.0

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
        if key == glfw.KEY_D:
            if action == glfw.PRESS:
                print("previa: ", self.Q_value)
                self.W_value += 0.02
                print("siguiente ", self.Q_value)

        if key == glfw.KEY_W:
            if action == glfw.PRESS:
                print("previa: ", self.Q_value)
                self.Q_value += 0.02
                print("siguiente ", self.Q_value)

        if key == glfw.KEY_A:
            if action == glfw.PRESS:
                print("previa: ", self.W_value)
                self.W_value -= 0.02
                print("siguiente ", self.W_value)

        if key == glfw.KEY_S:
            if action == glfw.PRESS:
                print("previa: ", self.W_value)
                self.Q_value -= 0.02
                print("siguiente ", self.W_value)

        # Caso en que se cierra la ventana
        if key == glfw.KEY_ESCAPE:
            if action == glfw.PRESS:
                glfw.set_window_should_close(window, True)

        # Caso de detectar Control izquierdo, se cambia el metodo de dibujo
        elif key == glfw.KEY_LEFT_CONTROL:
            if action == glfw.PRESS:
                self.showAxis = not self.showAxis


    #Funcion que recibe el input para manejar la camara y controlar sus coordenadas
    def update_camera1(self, delta):
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

    #Funcion que recibe el input para manejar la camara y controlar sus coordenadas
    def update_camera(self, delta, pos):

        self.polar_camera.set_center(pos)
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

class white_b:
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


class Shadow:
    def __init__(self):
        self.pos_ini = [-1.3,0,-0.9] 
        self.Shadow = mod.createShadowNode(-1.,0.0,-0.9, es.SimpleModelViewProjectionShaderProgram(),0,5)
        
    def move(self,x,y,z):
        self.pos_ini[0] = x
        self.pos_ini[1] = y
        self.pos_ini[2] = z
        self.Shadow.transform = tr.translate(self.pos_ini[0],self.pos_ini[1], self.pos_ini[2])

    def draw_call(self,pipeline2D):
        sg.drawSceneGraphNode(self.Shadow, pipeline2D, "model")


class Balls:

    def __init__(self, pipeline, position, velocity, i,j) :

        self.shape = mod.createTexSphereNode(position[0],position[1],position[2], pipeline,i,j)
        self.ang_vel = np.array([0,0,0],dtype=np.float32)
        self.position = position
        self.radius = 0.1
        self.velocity = velocity

    def update_pos(self,x,y,z):
        self.position[0]=x
        self.position[1]=y
        self.position[2]=z
        self.shape.transform = tr.translate(x,y ,z)
    
    def vel_angular(self):

        node=sg.findNode(self.shape,"rot_sphere")
        node.transform = tr.matmul([
        tr.rotationX(self.ang_vel[0]),
        tr.rotationY(self.ang_vel[1]),
        tr.rotationZ(self.ang_vel[2])
    ])

    def update_vel(self):
        print(self.velocity[0])
        print(self.velocity)

    def action(self, gravityAceleration,ang_aceleration, deltaTime):
        # Euler integration
        self.velocity += deltaTime * gravityAceleration
        self.position += self.velocity * deltaTime
        self.ang_vel += ang_aceleration
        self.shape.transform = tr.translate(self.position[0],self.position[1],self.position[2])

    def draw_call(self,pipeline):
        #self.tr_ball.transform = tr.translate(self.position[0],self.position[1],self.position[2])
        sg.drawSceneGraphNode(self.shape, pipeline, "model")

def collideWithBorder(Sphere):

    # Right
    if Sphere.position[0] + Sphere.radius > 1.65:
        Sphere.velocity[0] = -abs(Sphere.velocity[0])

    # Left
    if Sphere.position[0] < -3.65 + Sphere.radius:
        Sphere.velocity[0] = abs(Sphere.velocity[0])

    # Top
    if Sphere.position[1] > 1.65 - Sphere.radius:
        Sphere.velocity[1] = -abs(Sphere.velocity[1])

    # Bottom
    if Sphere.position[1] < -1.65 + Sphere.radius:
        Sphere.velocity[1] = abs(Sphere.velocity[1])

def collideWithBorder_white(Sphere):

    # Right
    if Sphere.position[0] + Sphere.radius > 3.65:
        Sphere.velocity[0] = -abs(Sphere.velocity[0])

    # Left
    if Sphere.position[0] < -1.65 + Sphere.radius:
        Sphere.velocity[0] = abs(Sphere.velocity[0])

    # Top
    if Sphere.position[1] > 1.65 - Sphere.radius:
        Sphere.velocity[1] = -abs(Sphere.velocity[1])

    # Bottom
    if Sphere.position[1] < -1.65 + Sphere.radius:
        Sphere.velocity[1] = abs(Sphere.velocity[1])


def rotate2D(vector, theta):
    """
    Direct application of a 2D rotation
    """
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        cos_theta * vector[0] - sin_theta * vector[1],
        sin_theta * vector[0] + cos_theta * vector[1],
        0.0
    ], dtype = np.float32)

def rotate3D(vector, theta):
    """
    Direct application of a 2D rotation
    """
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)
    R= tr.matmul(tr.rotationX(theta),tr.rotationY(theta),tr.rotationZ(theta))
    return np.array([
        cos_theta * vector[0] - sin_theta * vector[1],
        sin_theta * vector[0] + cos_theta * vector[1],
        0.0
    ], dtype = np.float32)

def collide(Ball1, Ball2):
    """
    If there are a collision between the circles, it modifies the velocity of
    both circles in a way that preserves energy and momentum.
    """
    
    assert isinstance(Ball1, Balls)
    assert isinstance(Ball2, Balls)

    normal = Ball2.position - Ball1.position
    normal /= np.linalg.norm(normal)

    Ball1MovingToNormal = np.dot(Ball2.velocity, normal) > 0.0
    Ball2MovingToNormal = np.dot(Ball1.velocity, normal) < 0.0

    if not (Ball1MovingToNormal and Ball2MovingToNormal):

        # obtaining the tangent direction
        tangent = rotate2D(normal, np.pi/2.0)

        # Projecting the velocity vector over the normal and tangent directions
        # for both circles, 1 and 2.
        v1n = np.dot(Ball1.velocity, normal) * normal
        v1t = np.dot(Ball1.velocity, tangent) * tangent

        v2n = np.dot(Ball2.velocity, normal) * normal
        v2t = np.dot(Ball2.velocity, tangent) * tangent

        # swaping the normal components...
        # this means that we applying energy and momentum conservation
        Ball1.velocity = v2n + v1t
        Ball2.velocity = v1n + v2t

def areColliding(Ball1, Ball2):
    assert isinstance(Ball1, Balls)
    assert isinstance(Ball2, Balls)

    difference = Ball2.position - Ball1.position
    distance = np.linalg.norm(difference)
    collisionDistance = Ball2.radius + Ball1.radius
    return distance < collisionDistance