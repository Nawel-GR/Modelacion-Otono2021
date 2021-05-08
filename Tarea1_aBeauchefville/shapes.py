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
    # First vertex at the center, white color
    vertices = [0, 0, 0, r, g, b] #rgb
    indices = []

    dtheta = 2 * math.pi / N

    for i in range(N):
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            0.5 * math.cos(theta), 0.5 * math.sin(theta), 0,

            # color generates varying between 0 and 1
                  r/2, g/2, b/2]

        # A triangle is created using the center, this and the next vertex
        indices += [0, i, i+1]

    # The final triangle connects back to the second vertex
    indices += [0, N, 1]

    return bs.Shape(vertices, indices)


def createScene(pipeline):
    # Funcion que crea la escena de la pregunta 2

    # Se crean las shapes en GPU    
    gpuBrownQuad = createGPUShape(bs.createColorQuad(0.4, 0.2, 0.07), pipeline) # Shape del quad cafe
    gpuBlackQuad = createGPUShape(bs.createColorQuad(0.3, 0.3, 0.3), pipeline) # Shape del quad negro claro
    gpuWhiteQuad = createGPUShape(bs.createColorQuad(1,1,1), pipeline) # Shape del cuadrado blanco
    gpuYellowQuad =  createGPUShape(bs.createColorQuad(0.8, 0.8, 0.2), pipeline) #shape de cuadrado amarillo
    gpuGreenQuad =  createGPUShape(bs.createColorQuad(0.3, 0.8, 0.3), pipeline) # Shape del cuadrado verde
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
    wayNode = sg.SceneGraphNode("way")
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
    leaves_dNode.transform = tr.matmul([tr.translate(0.06, 0.15, 0), tr.scale(0.2, 0.2, 0.2)])
    leaves_dNode.childs = [gpuGreenCircle]

    # Hojas izquierda del arbol 
    leaves_iNode = sg.SceneGraphNode("leaves_i")
    leaves_iNode.transform = tr.matmul([tr.translate(-0.06, 0.15, 0), tr.scale(0.2, 0.2, 0.2)])
    leaves_iNode.childs = [gpuGreenCircle]

    # conjunto Hojas del arbol 
    leaves_ccNode = sg.SceneGraphNode("leaves_cc")
    leaves_ccNode.childs = [leaves_cNode,leaves_iNode,leaves_dNode]

    # Manzanas
    apple_1Node = sg.SceneGraphNode("Apple1")
    apple_1Node.transform = tr.matmul([tr.translate(0.0, 0.27, 0), tr.scale(0.05, 0.05, 0.05)])
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
    orange1Node.transform = tr.matmul([tr.translate(0.0, 0.27, 0), tr.scale(0.05, 0.05, 0.05)])
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

    # Nodo del background con todos los nodos anteriores
    backGroundNode = sg.SceneGraphNode("background")
    backGroundNode.childs = [grassNode, highwayNode, forestNode]

    # Nodo padre de la escena
    sceneNode = sg.SceneGraphNode("world")
    sceneNode.childs = [backGroundNode]

    return sceneNode




