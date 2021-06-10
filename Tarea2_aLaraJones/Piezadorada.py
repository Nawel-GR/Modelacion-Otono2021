"""Creacion del rompecabezas """

import numpy as np
import math
from OpenGL.GL import *
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.ex_curves as cv
import grafica.scene_graph as sg

def createGPUShape(shape, pipeline):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

def createTextureGPUShape(shape, pipeline, path):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape con texturas
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    gpuShape.texture = es.textureSimpleSetup(
        path, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    return gpuShape

def createColorTriangle(r, g, b):
    # Funcion para crear un triangulo con un color personalizado

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -0.5, -0.5, 0.0,  r, g, b,
         0.5, -0.5, 0.0,  r, g, b,
         0.0,  0.5, 0.0,  r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2]

    return bs.Shape(vertices, indices)


def createColorCircle(N, r, g, b):
    # Funcion para crear un circulo con un color personalizado
    # Poligono de N lados 

    # First vertex at the center, white color
    vertices = [0, 0, 0, r, g, b]
    indices = []

    dtheta = 2 * math.pi / N

    for i in range(N):
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            0.5 * math.cos(theta), 0.5 * math.sin(theta), 0,

            # color generates varying between 0 and 1
                  r, g, b]

        # A triangle is created using the center, this and the next vertex
        indices += [0, i, i+1]

    # The final triangle connects back to the second vertex
    indices += [0, N, 1]

    return bs.Shape(vertices, indices)


def evalMixCurve(N):
    # Funcion para generar N puntos entre 0 y 1 de una curva personalizada
    # Hermite + Bezier para modelar la superficie de un auto

    # Puntos de Control
    P0 = np.array([[0.07, 0.14, 0]]).T
    P1 = np.array([[0.27, -0.04, 0]]).T
    P2 = np.array([[0.42, 0.06, 0]]).T
    P3 = np.array([[0.5, -0.06, 0]]).T
    #P4 = np.array([[-0.5, -0.06, 0]]).T
    #T0 = np.array([[-0.13, 0.35, 0]]).T
    #alpha = 1
    #T1 = 3 * alpha * (P1 - P0)
    # Matrices de Hermite y Beziers
    #H_M = cv.hermiteMatrix(P4, P0, T0, T1)
    B_M = cv.bezierMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)#//2)
    #offset = N
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 3), dtype=float) #len(ts) * 2
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = cv.generateT(ts[i])
        #curve[i, 0:3] = np.matmul(H_M, T).T
        curve[i, 0:3] = np.matmul(B_M, T).T
        
    return curve


def evalMixCurve2(N):
    # Puntos de Control
    P0 = np.array([[-0.1, 0.25, 0]]).T
    P1 = np.array([[-0.3, 0.5, 0]]).T
    P2 = np.array([[0.3, 0.5, 0]]).T
    P3 = np.array([[0.1, 0.25, 0]]).T
    
    # Matrices de Hermite y Beziers
    B_M = cv.bezierMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = cv.generateT(ts[i])
        curve[i] = np.matmul(B_M, T).T
        
    return curve


def createColorChasis(r, g, b):
    # Crea un shape del chasis de un auto a partir de una curva personalizada
    vertices = []
    indices = []
    curve = evalMixCurve2(64) # Se obtienen los puntos de la curva
    delta = (1 / len(curve))/5 # distancia del step /paso
    x_0 = -0.1 # Posicion x inicial de la recta inferior
    y_0 = 0.25 # Posicion y inicial de la recta inferior
    counter = 0 # Contador de vertices, para indicar los indices

    # Se generan los vertices
    for i in range(len(curve)-1):
        c_0 = curve[i] # punto i de la curva
        r_0 = [x_0 + i*delta, y_0] # punto i de la recta
        c_1 = curve[i + 1] # punto i + 1 de la curva
        r_1 = [x_0 + (i+1)*delta, y_0] # punto i + 1 de la recta
        vertices += [c_0[0], c_0[1], 0, r - 0.06, g - 0.06, b - 0.06]
        vertices += [r_0[0], r_0[1], 0, r, g, b]
        vertices += [c_1[0], c_1[1], 0, r - 0.06, g - 0.06, b - 0.06]
        vertices += [r_1[0], r_1[1], 0, r, g, b]
        indices += [counter + 0, counter +1, counter + 2]
        indices += [counter + 2, counter + 3, counter + 1]
        counter += 4

    return bs.Shape(vertices, indices)

def createPiece(pipeline):

    # Se crean las shapes en GPU
    gpuChasis1 = createGPUShape(createColorCircle(30,0.8, 0.8, 0.1), pipeline) # Shape del chasis 
    gpuYellowQuad1 = createGPUShape(bs.createColorQuad(0.8, 0.8, 0.1), pipeline) # Shape de quad azul
    gpuChasis2 = createGPUShape(createColorChasis(0.9, 0.9, 0.1), pipeline) 
    gpuYellowQuad2 = createGPUShape(bs.createColorQuad(0.9, 0.9, 0.1), pipeline) 

    # Nodo de la circunfernecia de arriba
    redChasisNode2_1 = sg.SceneGraphNode("redChasis")
    redChasisNode2_1.childs = [gpuChasis2]

    # Nodo de la circunfernecia de la derecha
    redChasisNode2_2 = sg.SceneGraphNode("redChasis")
    redChasisNode2_2.transform = tr.matmul([tr.translate(-0.05, 0.05, 0),tr.rotationZ(-1.57)])
    redChasisNode2_2.childs = [gpuChasis2]


    # Nodo de la ventana, quad celeste escalado
    windowNode2 = sg.SceneGraphNode("window")
    windowNode2.transform = tr.matmul([tr.translate(-0.0, 0.05, 0), tr.scale(0.4, 0.4, 1)])
    windowNode2.childs = [gpuYellowQuad2]


    # Nodo de a figura final Grande
    Piece2Node = sg.SceneGraphNode("window")
    Piece2Node.childs = [windowNode2,redChasisNode2_1,redChasisNode2_2]

    #Pequeño

    # Nodo de la circunfernecia de arriba
    redChasisNode1_1 = sg.SceneGraphNode("redChasis")
    redChasisNode1_1.transform = tr.matmul([tr.translate(0.0, 0.35, 0), tr.scale(0.15, 0.15, 1)])
    redChasisNode1_1.childs = [gpuChasis1]

    # Nodo de la circunfernecia de la derecha
    redChasisNode1_2 = sg.SceneGraphNode("redChasis")
    redChasisNode1_2.transform = tr.matmul([tr.translate(0.3, 0.05, 0),tr.scale(0.15, 0.15, 1)])
    redChasisNode1_2.childs = [gpuChasis1]

    # Nodo de la ventana, quad celeste escalado
    windowNode2 = sg.SceneGraphNode("window")
    windowNode2.transform = tr.matmul([tr.translate(-0.0, 0.05, 0), tr.scale(0.25, 0.25, 1)])
    windowNode2.childs = [gpuYellowQuad1]

    # Nodo de a figura final
    Piece1Node = sg.SceneGraphNode("window")
    Piece1Node.transform = tr.scale(0.9, 0.9, 1)
    Piece1Node.childs = [windowNode2,redChasisNode1_1,redChasisNode1_2]

    # Nodo padre auto
    carNode = sg.SceneGraphNode("car")
    carNode.childs = [Piece2Node,Piece1Node]

    return carNode




