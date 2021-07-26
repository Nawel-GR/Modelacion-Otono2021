import grafica.scene_graph as sg
import grafica.transformations as tr
import grafica.easy_shaders as es
import grafica.newLightShaders as nl
import Modelo as mod
import numpy as np
import glfw

#clase de la vara
class objeto:
    def __init__(self):
        self.obj = mod.createStick(es.SimpleModelViewProjectionShaderProgram())
        self.pos_ini = [-1.3,0,-1] 
        
    def move(self,x,y,z):
        self.pos_ini[0] = x
        self.pos_ini[1] = y
        self.pos_ini[2] = z
        self.obj.transform = tr.matmul([tr.translate(self.pos_ini[0],self.pos_ini[1], self.pos_ini[2]),tr.rotationZ(-np.pi/2)])

    def draw_call(self,pipeline2D):
        sg.drawSceneGraphNode(self.obj, pipeline2D, "model")


class PolarCamera:
    def __init__(self):
        self.center = 0,0,0
        self.theta = 0                           
        self.rho = 3.                             
        self.eye = np.array([0.0, 0.0, 0.0])    
        self.height = 0.1                       
        self.up = np.array([0, 0, 1])            
        self.viewMatrix = None                   
    
    def set_theta(self, delta):
        self.theta = (self.theta + delta) % (np.pi * 2)

    def set_rho(self, delta):
        if ((self.rho + delta) > 0.1):
            self.rho += delta

    def set_center(self,pos):
        self.center =pos

    def update_view(self):
        self.eye[0] = self.rho * np.sin(self.theta) + self.center[0]
        self.eye[1] = self.rho * np.cos(self.theta) + self.center[1]
        self.eye[2] = self.height + self.center[2]

        viewMatrix = tr.lookAt(
            self.eye, self.center, self.up
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
        self.polar_camera = PolarCamera() #Puede ser cambiado para otra visualización

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


#Sombra de la bola
class Shadow:
    def __init__(self):
        self.pos_ini = [-1.3,0,-1] 
        self.Shadow = mod.createShadowNode(-1.,0.0,-0.9, es.SimpleModelViewProjectionShaderProgram())
        
    def move(self,x,y,z):
        self.pos_ini = x,y,z
        self.Shadow.transform = tr.translate(self.pos_ini[0],self.pos_ini[1], self.pos_ini[2])

    def draw_call(self,pipeline2D):
        sg.drawSceneGraphNode(self.Shadow, pipeline2D, "model")

#Pelotas de pool
class Pool_Ball:

    def __init__(self, pipeline, pos, vel, i,j) :

        self.shape = mod.createTexSphereNode(pos[0],pos[1],pos[2], pipeline,i,j)
        self.position = pos
        self.velocity = vel
        self.ang_vel = np.array([0,0,0],dtype=np.float32)
        self.radius = 0.1
        self.notinhole = True

    def move(self,x,y,z):
        self.position = x,y,z
        self.shape.transform = tr.translate(x,y ,z)
    
    def vel_angular(self):
        node=sg.findNode(self.shape,"rot_sphere")
        node.transform = tr.matmul([tr.rotationX(self.ang_vel[0]),  tr.rotationY(self.ang_vel[1]), tr.rotationZ(self.ang_vel[2])])

    def action(self, gravityAceleration,ang_aceleration, deltaTime):
        self.velocity += deltaTime * gravityAceleration
        self.position += self.velocity * deltaTime
        self.ang_vel += ang_aceleration
        self.shape.transform = tr.translate(self.position[0],self.position[1],self.position[2])

    def draw_call(self,pipeline):
        sg.drawSceneGraphNode(self.shape, pipeline, "model")


'''
A continuación se encuentran las funciones de colisiones, se podrá notar que
existe un desfase entre las pelotas de colores y la pelota principal
esto se debe principalmente a la traslación inicial que se les hace a estas

'''

def rotate(vector, theta):
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        cos_theta * vector[0] - sin_theta * vector[1],
        sin_theta * vector[0] + cos_theta * vector[1],
        0.0
    ], dtype = np.float32)

#Solo para las bolas de colores, implementación de entrar en el hoyo.
def inHole(ball):
    assert isinstance(ball, Pool_Ball)

    pos = ball.position
    if ball.position[0] + ball.radius > 1.55:
        if np.abs(ball.position[1]) > 1.65 - ball.radius:
            return True
    
    elif ball.position[0] < -3.55 + ball.radius:
        if np.abs(ball.position[1]) > 1.65 - ball.radius:
            return True
    
    elif ball.position[0] + ball.radius > -1.1  and ball.position[0] < -0.9 + ball.radius:
        if np.abs(ball.position[1]) > 1.65 - ball.radius:
            return True

#Colisiones con el borde
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

def collideWithBorder2(Sphere):

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

#colisión entre pelotas
def collide(Ball1, Ball2):
        
    assert isinstance(Ball1, Pool_Ball)
    assert isinstance(Ball2, Pool_Ball)

    normal = Ball2.position - Ball1.position
    normal /= np.linalg.norm(normal)

    Ball1MovingToNormal = np.dot(Ball2.velocity, normal) > 0.0
    Ball2MovingToNormal = np.dot(Ball1.velocity, normal) < 0.0

    if not (Ball1MovingToNormal and Ball2MovingToNormal):

        tangent = rotate(normal, np.pi/2.0)

        v1n = np.dot(Ball1.velocity, normal) * normal
        v1t = np.dot(Ball1.velocity, tangent) * tangent

        v2n = np.dot(Ball2.velocity, normal) * normal
        v2t = np.dot(Ball2.velocity, tangent) * tangent

        Ball1.velocity = v2n + v1t
        Ball2.velocity = v1n + v2t

def collide2(Ballwhite, Ball2):
        
    assert isinstance(Ballwhite, Pool_Ball)
    assert isinstance(Ball2, Pool_Ball)

    normal = Ball2.position - Ballwhite.position
    normal[0] -= 2
    normal /= np.linalg.norm(normal)

    Ball1MovingToNormal = np.dot(Ball2.velocity, normal) > 0.0
    Ball2MovingToNormal = np.dot(Ballwhite.velocity, normal) < 0.0

    if not (Ball1MovingToNormal and Ball2MovingToNormal):  
        tangent = rotate(normal, np.pi/2.0)

        v1n = np.dot(Ballwhite.velocity, normal) * normal
        v1t = np.dot(Ballwhite.velocity, tangent) * tangent

        v2n = np.dot(Ball2.velocity, normal) * normal
        v2t = np.dot(Ball2.velocity, tangent) * tangent

        Ballwhite.velocity = v2n + v1t
        Ball2.velocity = v1n + v2t

#efecto de la colision
def areColliding(Ball1, Ball2):
    assert isinstance(Ball1, Pool_Ball)
    assert isinstance(Ball2, Pool_Ball)

    difference = Ball2.position - Ball1.position
    distance = np.linalg.norm(difference)
    collisionDistance = Ball2.radius + Ball1.radius
    return distance < collisionDistance

def areColliding2(Ballwhite, Ball2):
    assert isinstance(Ballwhite, Pool_Ball)
    assert isinstance(Ball2, Pool_Ball)

    difference = Ball2.position - Ballwhite.position
    difference[0] -= 2 #desface
    distance = np.linalg.norm(difference)
    collisionDistance = Ball2.radius + Ballwhite.radius
    return distance < collisionDistance

