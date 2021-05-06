"""Funciones para crear distintas figuras y escenas """

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
    P4 = np.array([[-0.5, -0.06, 0]]).T
    T0 = np.array([[-0.13, 0.35, 0]]).T
    alpha = 1
    T1 = 3 * alpha * (P1 - P0)
    # Matrices de Hermite y Beziers
    H_M = cv.hermiteMatrix(P4, P0, T0, T1)
    B_M = cv.bezierMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N//2)
    offset = N//2 
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts) * 2, 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = cv.generateT(ts[i])
        curve[i, 0:3] = np.matmul(H_M, T).T
        curve[i + offset, 0:3] = np.matmul(B_M, T).T
        
    return curve

def createColorChasis(r, g, b):
    # Crea un shape del chasis de un auto a partir de una curva personalizada
    vertices = []
    indices = []
    curve = evalMixCurve(64) # Se obtienen los puntos de la curva
    delta = 1 / len(curve) # distancia del step /paso
    x_0 = -0.5 # Posicion x inicial de la recta inferior
    y_0 = -0.2 # Posicion y inicial de la recta inferior
    counter = 0 # Contador de vertices, para indicar los indices

    # Se generan los vertices
    for i in range(len(curve)-1):
        c_0 = curve[i] # punto i de la curva
        r_0 = [x_0 + i*delta, y_0] # punto i de la recta
        c_1 = curve[i + 1] # punto i + 1 de la curva
        r_1 = [x_0 + (i+1)*delta, y_0] # punto i + 1 de la recta
        vertices += [c_0[0], c_0[1], 0, r + 0.3, g + 0.3, b + 0.3]
        vertices += [r_0[0], r_0[1], 0, r, g, b]
        vertices += [c_1[0], c_1[1], 0, r + 0.3, g + 0.3, b + 0.3]
        vertices += [r_1[0], r_1[1], 0, r, g, b]
        indices += [counter + 0, counter +1, counter + 2]
        indices += [counter + 2, counter + 3, counter + 1]
        counter += 4

    return bs.Shape(vertices, indices)


def createCar(pipeline):
    # Se crea la escena del auto de la pregunta 1

    # Se crean las shapes en GPU
    gpuChasis = createGPUShape(createColorChasis(0.7, 0, 0), pipeline) # Shape del chasis 
    gpuGrayCircle =  createGPUShape(createColorCircle(20, 0.4, 0.4, 0.4), pipeline) # Shape del circulo gris
    gpuBlackCircle =  createGPUShape(createColorCircle(20, 0, 0, 0), pipeline) # Shape del circulo negro
    gpuBlueQuad = createGPUShape(bs.createColorQuad(0.2, 0.2, 1), pipeline) # Shape de quad azul

    # Nodo del chasis rojo
    redChasisNode = sg.SceneGraphNode("redChasis")
    redChasisNode.childs = [gpuChasis]

    # Nodo del circulo gris
    grayCircleNode = sg.SceneGraphNode("grayCircleNode")
    grayCircleNode.childs = [gpuGrayCircle]
    
    # Nodo del circulo negro
    blackCircleNode = sg.SceneGraphNode("blackCircle")
    blackCircleNode.childs = [gpuBlackCircle]

    # Nodo del quad celeste
    blueQuadNode = sg.SceneGraphNode("blueQuad")
    blueQuadNode.childs = [gpuBlueQuad]

    # Nodo del circulo gris escalado
    scaledGrayCircleNode = sg.SceneGraphNode("slGrayCircle")
    scaledGrayCircleNode.transform = tr.scale(0.6, 0.6, 0.6)
    scaledGrayCircleNode.childs = [grayCircleNode]

    # Nodo de una rueda, escalado
    wheelNode = sg.SceneGraphNode("wheel")
    wheelNode.transform = tr.scale(0.22, 0.22, 0.22)
    wheelNode.childs = [blackCircleNode, scaledGrayCircleNode]

    # Nodo de la ventana, quad celeste escalado
    windowNode = sg.SceneGraphNode("window")
    windowNode.transform = tr.scale(0.22, 0.15, 1)
    windowNode.childs = [blueQuadNode]
     
    # Rueda izquierda posicionada
    leftWheel = sg.SceneGraphNode("lWheel")
    leftWheel.transform = tr.translate(-0.3, -0.2, 0)
    leftWheel.childs = [wheelNode]

    # Rueda derecha posicionada
    rightWheel = sg.SceneGraphNode("rWheel")
    rightWheel.transform = tr.translate(0.26, -0.2, 0)
    rightWheel.childs = [wheelNode]

    # Ventana posicionada
    translateWindow = sg.SceneGraphNode("tlWindow")
    translateWindow.transform = tr.translate(-0.08, 0.06, 0.0)
    translateWindow.childs = [windowNode]

    # Nodo padre auto
    carNode = sg.SceneGraphNode("car")
    carNode.childs = [redChasisNode, translateWindow, leftWheel, rightWheel]

    return carNode

def createScene(pipeline):
    # Funcion que crea la escena de la pregunta 2

    # Se crean las shapes en GPU

    
    
    
    gpuBrownQuad = createGPUShape(bs.createColorQuad(0.4, 0.2, 0.07), pipeline) # Shape del quad cafe
    gpuBlackQuad = createGPUShape(bs.createColorQuad(0.3, 0.3, 0.3), pipeline) # Shape del quad gris
    gpuWhiteQuad = createGPUShape(bs.createColorQuad(1,1,1), pipeline) # Shape del quad blanco
    gpuYellowQuad =  createGPUShape(bs.createColorQuad(0.8, 0.8, 0.2), pipeline) #shape de rectangulo amarillo
    gpuGreenQuad =  createGPUShape(bs.createColorQuad(0.3, 0.8, 0.3), pipeline) # Shape del quad verde
    gpuGrayQuad = createGPUShape(bs.createColorQuad(0.5, 0.5, 0.5), pipeline) #Shape cuadrado gris
    gpuGreenCircle =  createGPUShape(createColorCircle(20, 0.1, 0.5, 0.1), pipeline) # Shape del circulo verde
    gpuRedCircle =  createGPUShape(createColorCircle(20, 0.8, 0.2, 0.2), pipeline) # Shape del circulo rojo
    gpuOrangeCircle = createGPUShape(createColorCircle(20, 0.9, 0.4, 0.1), pipeline) # Shape del circulo orange
    
    
# Pasto
    grassNode = sg.SceneGraphNode("grass")
    grassNode.transform = tr.scale(2, 2, 1)
    grassNode.childs = [gpuGreenQuad]
    

###Carretera
    ##Base
    wayNode = sg.SceneGraphNode("highway")
    wayNode.transform = tr.matmul([ tr.scale(1.2, 2, 1)])
    wayNode.childs = [gpuBlackQuad]  

    ##Lineas grises (grandes) de la carretera

    # Una linea gris (grande) de la carretera
    grandlineGNode = sg.SceneGraphNode("grandline")
    grandlineGNode.transform = tr.matmul([ tr.scale(0.04, 2.0, 1)])
    grandlineGNode.childs = [gpuGrayQuad]

    #Dos lineas de las carretera 
    grand1lineGNode = sg.SceneGraphNode("grandline1")
    grand1lineGNode.transform = tr.translate(-0.6,0,0)
    grand1lineGNode.childs = [grandlineGNode]

    grand2lineGNode = sg.SceneGraphNode("grandline2")
    grand2lineGNode.transform = tr.translate(0.6,0,0)
    grand2lineGNode.childs = [grandlineGNode]

    grandline_cGNode = sg.SceneGraphNode("grandline2")
    grandline_cGNode.childs = [grand1lineGNode, grand2lineGNode]

    ##Lineas blancas (grandes) de la carretera

    # Una linea blanca (grande) de la carretera
    grandlineNode = sg.SceneGraphNode("grandline")
    grandlineNode.transform = tr.matmul([ tr.scale(0.04, 2.0, 1)])
    grandlineNode.childs = [gpuYellowQuad]

    #Dos lineas de las carretera 
    grand1lineNode = sg.SceneGraphNode("grandline1")
    grand1lineNode.transform = tr.translate(-0.4,0,0)
    grand1lineNode.childs = [grandlineNode]

    grand2lineNode = sg.SceneGraphNode("grandline2")
    grand2lineNode.transform = tr.translate(0.4,0,0)
    grand2lineNode.childs = [grandlineNode]

    grandline_cNode = sg.SceneGraphNode("grandline2")
    grandline_cNode.childs = [grand1lineNode, grand2lineNode]

    ##Lineas blancas (pequeñas) de la carretera

    # Una linea blanca (pequeña) de la carretera
    lineNode = sg.SceneGraphNode("line1")
    lineNode.transform = tr.matmul([ tr.scale(0.03, 0.2, 1)])
    lineNode.childs = [gpuWhiteQuad]

    # Linea 1,2,3
    line_1Node = sg.SceneGraphNode("line_1")
    line_1Node.transform = tr.translate(0, 0.0, 0)
    line_1Node.childs = [lineNode]

    line_2Node = sg.SceneGraphNode("line_2")
    line_2Node.transform = tr.translate(0, -0.40, 0)
    line_2Node.childs = [lineNode]
    
    line_3Node = sg.SceneGraphNode("line_3")
    line_3Node.transform = tr.translate(0, 0.40, 0)
    line_3Node.childs = [lineNode]

    #Conjuntos de 3 lineas
    line_auxNode = sg.SceneGraphNode("line_c")
    line_auxNode.childs = [line_1Node, line_2Node, line_3Node]  

    #Conjunto de 3 lineas 1,2 ,3
    line_c1Node = sg.SceneGraphNode("line_c1")
    line_c1Node.transform = tr.translate(0, 0.6, 0)
    line_c1Node.childs = [line_auxNode]

    line_c2Node = sg.SceneGraphNode("line_c2")
    line_c2Node.transform = tr.translate(0, -0.6, 0)
    line_c2Node.childs = [line_auxNode] 

    #Conjunto mayor 
    line_cNode = sg.SceneGraphNode("line_c")
    line_cNode.childs = [line_c1Node, line_c2Node] 

    # Carretera
    highwayNode = sg.SceneGraphNode("highway")
    highwayNode.childs = [wayNode,grandline_cGNode,grandline_cNode,line_cNode]  


##Arboles
    #Tronco del arbol
    trunkNode = sg.SceneGraphNode("trunk")
    trunkNode.transform = tr.scale(0.07,0.1,1)
    trunkNode.childs = [gpuBrownQuad]

    # Hojas centrales del arbol 
    leaves_cNode = sg.SceneGraphNode("leaves_c")
    leaves_cNode.transform = tr.matmul([tr.translate(0.0, 0.19, 0), tr.scale(0.2, 0.3, 0.2)])
    leaves_cNode.childs = [gpuGreenCircle]

    # Hojas derecha del arbol 
    leaves_dNode = sg.SceneGraphNode("leaves_d")
    leaves_dNode.transform = tr.matmul([tr.translate(0.05, 0.15, 0), tr.scale(0.2, 0.2, 0.2)])
    leaves_dNode.childs = [gpuGreenCircle]

    # Hojas izquierda del arbol 
    leaves_iNode = sg.SceneGraphNode("leaves_i")
    leaves_iNode.transform = tr.matmul([tr.translate(-0.05, 0.15, 0), tr.scale(0.2, 0.2, 0.2)])
    leaves_iNode.childs = [gpuGreenCircle]

    # conjunto Hojas del arbol 
    leaves_ccNode = sg.SceneGraphNode("leaves_cc")
    leaves_ccNode.childs = [leaves_cNode,leaves_iNode,leaves_dNode]

    # Manzanas
    apple_1Node = sg.SceneGraphNode("Apple1")
    apple_1Node.transform = tr.matmul([tr.translate(0.0, 0.25, 0), tr.scale(0.05, 0.05, 0.05)])
    apple_1Node.childs = [gpuRedCircle]

    apple_2Node = sg.SceneGraphNode("Apple2")
    apple_2Node.transform = tr.matmul([tr.translate(-0.07, 0.15, 0), tr.scale(0.05, 0.05, 0.05)])
    apple_2Node.childs = [gpuRedCircle]

    apple_3Node = sg.SceneGraphNode("Apple2")
    apple_3Node.transform = tr.matmul([tr.translate(0.07, 0.15, 0), tr.scale(0.05, 0.05, 0.05)])
    apple_3Node.childs = [gpuRedCircle]

    #Se crea manzano
    applethreeNode = sg.SceneGraphNode("apple_three")
    applethreeNode.childs = [trunkNode,leaves_ccNode,apple_1Node,apple_2Node,apple_3Node]

    #manzano 1
    apple_three1Node = sg.SceneGraphNode("apple_three1")
    apple_three1Node.transform = tr.translate(0.0, 0.6, 0)
    apple_three1Node.childs = [applethreeNode]

    #manzano 2
    apple_three2Node = sg.SceneGraphNode("apple_three1")
    apple_three2Node.transform = tr.translate(0.0, 0.1, 0)
    apple_three2Node.childs = [applethreeNode]
    

    #manzano 3
    apple_three3Node = sg.SceneGraphNode("apple_three1")
    apple_three3Node.transform = tr.translate(0.0, -0.4, 0)
    apple_three3Node.childs = [applethreeNode]

    #manzano 4
    apple_three4Node = sg.SceneGraphNode("apple_three1")
    apple_three4Node.transform = tr.translate(0.0, -0.9, 0)
    apple_three4Node.childs = [applethreeNode]

    #conjunto manzanos
    apple_three_cNode = sg.SceneGraphNode("apple_three_c")
    apple_three_cNode.transform = tr.translate(0.8, 0, 0)
    apple_three_cNode.childs = [apple_three1Node,apple_three2Node,apple_three3Node,apple_three4Node]


    # Naranjas
    orange1Node = sg.SceneGraphNode("Orange1")
    orange1Node.transform = tr.matmul([tr.translate(0.0, 0.25, 0), tr.scale(0.05, 0.05, 0.05)])
    orange1Node.childs = [gpuOrangeCircle]

    orange2Node = sg.SceneGraphNode("Orange2")
    orange2Node.transform = tr.matmul([tr.translate(-0.07, 0.15, 0), tr.scale(0.05, 0.05, 0.05)])
    orange2Node.childs = [gpuOrangeCircle]

    orange3Node = sg.SceneGraphNode("Orange3")
    orange3Node.transform = tr.matmul([tr.translate(0.07, 0.15, 0), tr.scale(0.05, 0.05, 0.05)])
    orange3Node.childs = [gpuOrangeCircle]

    #Se crea naranjo
    oranjethreeNode = sg.SceneGraphNode("orange_three")
    oranjethreeNode.childs = [trunkNode,leaves_ccNode,orange1Node,orange2Node,orange3Node]

    #naranjo 1
    orange_three1Node = sg.SceneGraphNode("orange_three1")
    orange_three1Node.transform = tr.translate(0.0, 0.1, 0)
    orange_three1Node.childs = [oranjethreeNode]
    

    #naranjo 2
    orange_three2Node = sg.SceneGraphNode("orange_three2")
    orange_three2Node.transform = tr.translate(0.0, -0.4, 0)
    orange_three2Node.childs = [oranjethreeNode]

    #naranjo 3
    orange_three3Node = sg.SceneGraphNode("orange_three3")
    orange_three3Node.transform = tr.translate(0.0, -0.9, 0)
    orange_three3Node.childs = [oranjethreeNode]

    #conjunto manzanos
    orange_three_cNode = sg.SceneGraphNode("orange_three_c")
    orange_three_cNode.transform = tr.translate(-0.8, 0, 0)
    orange_three_cNode.childs = [orange_three1Node,orange_three2Node,orange_three3Node]


    #Nodo que crea los arboles
    forestNode = sg.SceneGraphNode("arbolles")
    forestNode.childs = [apple_three_cNode,orange_three_cNode]


##final

    # Nodo del background con todos los nodos anteriores
    backGroundNode = sg.SceneGraphNode("background")
    backGroundNode.childs = [grassNode, highwayNode, translateWindMill1Node, forestNode]

    # Nodo padre de la escena
    sceneNode = sg.SceneGraphNode("world")
    sceneNode.childs = [backGroundNode]

    return sceneNode




