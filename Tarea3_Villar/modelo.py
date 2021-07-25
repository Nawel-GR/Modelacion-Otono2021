""" Funciones para crear distintas figuras y escenas en 3D """

from typing_extensions import final
import numpy as np
import math
from OpenGL.GL import *
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.scene_graph as sg
import grafica.ex_curves as cv

def createGPUShape(pipeline, shape):
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

def createScene(pipeline3D,pipeline2D):
    # Se crean las shapes en GPU
    gpuGreenCube = createGPUShape(pipeline3D, bs.createColorNormalsCube(55/255, 97/255, 54/255)) # Shape del cubo verde
    gpuBrownCube = createGPUShape(pipeline3D, bs.createColorNormalsCube(128/255, 64/255, 0/255)) # Shape del cubo café
    gpuBlackQuad = createGPUShape(pipeline2D, bs.createColorCircle(20,0.,0.,0.)) # Shape del circulo negro
    gpuGreenPrism = createGPUShape(pipeline3D, bs.createColorPrism(35/255, 77/255, 34/255)) # Shape del prisma verde

    # Nodo Prisma
    GreenPrismNode = sg.SceneGraphNode("GreenPrism")
    GreenPrismNode.childs = [gpuGreenPrism]

    # Nodo del cubo Verde
    GreenCubeNode = sg.SceneGraphNode("GreenCube")
    GreenCubeNode.childs = [gpuGreenCube]

    # Nodo del cubo Café
    BrownCubeNode = sg.SceneGraphNode("BrownCube")
    BrownCubeNode.childs = [gpuBrownCube]

    # Nodo del circulo negro
    BlackQuadNode = sg.SceneGraphNode("BlackQuad")
    BlackQuadNode.childs = [gpuBlackQuad]

    # Nodo de la mesa
    FloorNode = sg.SceneGraphNode("floor")
    FloorNode.transform = tr.matmul([tr.translate(0, 0, -1), tr.scale(6, 4, 0.01)])
    FloorNode.childs = [GreenCubeNode]


    #Piezas Madera
    # Standar X
    XBrownPieceNode = sg.SceneGraphNode("XbrownPiece")
    XBrownPieceNode.transform = tr.matmul([tr.translate(0, 0, -0.93), tr.scale(6.16, 0.15, 0.15)])
    XBrownPieceNode.childs = [BrownCubeNode]

    XGreenPrismNode1 = sg.SceneGraphNode("XGreenPrism1")
    XGreenPrismNode1.transform = tr.matmul([tr.translate(1.3, -0.2, -0.93), tr.scale(2.5, 0.35, 0.1)])
    XGreenPrismNode1.childs = [GreenPrismNode]

    XGreenPrismNode2 = sg.SceneGraphNode("XGreenPrism2")
    XGreenPrismNode2.transform = tr.matmul([tr.translate(-1.3, -0.2, -0.93), tr.scale(2.5, 0.35, 0.1)])
    XGreenPrismNode2.childs = [GreenPrismNode]

    # Pairs in X
    XBrownPieceNodeRight = sg.SceneGraphNode("XBrownPieceRight")
    XBrownPieceNodeRight.transform = tr.matmul([tr.translate(0, 2, 0)])
    XBrownPieceNodeRight.childs = [XBrownPieceNode,XGreenPrismNode1,XGreenPrismNode2]
    
    XBrownPieceNodeLeft = sg.SceneGraphNode("XBrownPieceLeft")
    XBrownPieceNodeLeft.transform = tr.matmul([tr.translate(0, -2, 0), tr.rotationZ(3.14)])
    XBrownPieceNodeLeft.childs = [XBrownPieceNode,XGreenPrismNode1,XGreenPrismNode2]

    # Final Pair in X
    XBrownPairPieces = sg.SceneGraphNode("XBrownPair")
    XBrownPairPieces.childs = [XBrownPieceNodeLeft,XBrownPieceNodeRight]

    # Standar Y
    YBrownPieceNode = sg.SceneGraphNode("YbrownPiece")
    YBrownPieceNode.transform = tr.matmul([tr.translate(0, 0, -0.93), tr.scale(0.15, 4, 0.15)])
    YBrownPieceNode.childs = [BrownCubeNode]

    YGreenPrismNode = sg.SceneGraphNode("YGreenPrism")
    YGreenPrismNode.transform = tr.matmul([tr.translate(-0.2, 0, -0.93), tr.scale(0.35, 3.5, 0.1), tr.rotationZ(-1.57)])
    YGreenPrismNode.childs = [GreenPrismNode]

    # Final Pair in Y
    YBrownPieceNodeUp = sg.SceneGraphNode("YBrownPieceUp")
    YBrownPieceNodeUp.transform = tr.matmul([tr.translate(3., 0, 0)])
    YBrownPieceNodeUp.childs = [YBrownPieceNode,YGreenPrismNode]
    
    YBrownPieceNodeDown = sg.SceneGraphNode("YBrownPieceDown")
    YBrownPieceNodeDown.transform = tr.matmul([tr.translate(-3., 0, 0), tr.rotationZ(3.14)])
    YBrownPieceNodeDown.childs = [YBrownPieceNode,YGreenPrismNode]

    YBrownPairPieces = sg.SceneGraphNode("FinalYpair")
    YBrownPairPieces.childs = [YBrownPieceNodeUp,YBrownPieceNodeDown]


    # Wood Pieces
    WoodPieces = sg.SceneGraphNode("YBrownPair")
    WoodPieces.childs = [YBrownPairPieces,XBrownPairPieces]

    #Hoyos

    # Nodo del hoyo negro
    HoleNode = sg.SceneGraphNode("hole")
    HoleNode.transform = tr.scale(0.3,0.3,0)
    HoleNode.childs = [BlackQuadNode]

    # Hole Right
    HoleNodeRight = sg.SceneGraphNode("holeRight")
    HoleNodeRight.transform = tr.translate(0, 1.72, -0.99)
    HoleNodeRight.childs = [HoleNode]

    # Hole Left
    HoleNodeLeft = sg.SceneGraphNode("holeLeft")
    HoleNodeLeft.transform = tr.translate(0, -1.72, -0.99)
    HoleNodeLeft.childs = [HoleNode]
    
    # Par de Nodos paralelos
    PairHoleNode = sg.SceneGraphNode("pairholes")
    PairHoleNode.childs = [HoleNodeRight,HoleNodeLeft]

    # Holesup
    UpHolesNode = sg.SceneGraphNode("holesup")
    UpHolesNode.transform = tr.matmul([tr.translate(2.65, 0., 0.)])
    UpHolesNode.childs = [PairHoleNode]

    # Holesbet
    BetHolesNode = sg.SceneGraphNode("holesbet")
    BetHolesNode.transform = tr.matmul([tr.translate(0., 0., 0.)])
    BetHolesNode.childs = [PairHoleNode]

    # Holesund
    UndHolesNode = sg.SceneGraphNode("holesund")
    UndHolesNode.transform = tr.matmul([tr.translate(-2.65, 0., 0.)])
    UndHolesNode.childs = [PairHoleNode]
    
    # Nodo de la mesa
    TableNode = sg.SceneGraphNode("table")
    TableNode.childs = [FloorNode,UpHolesNode,BetHolesNode,UndHolesNode,WoodPieces] 
    
    # Nodo de la escena para realizar un escalamiento
    sceneNode = sg.SceneGraphNode("scene")
    sceneNode.transform = tr.matmul([tr.translate(0, 0, 0)])
    sceneNode.childs = [TableNode] 

    # Nodo final de la escena 
    trSceneNode = sg.SceneGraphNode("tr_scene")
    trSceneNode.childs = [sceneNode]

    return trSceneNode


def createTextureNormalSphere(N,k,l):
    # Funcion para crear una esfera con normales y texturizada

    vertices = []           # lista para almacenar los verices
    indices = []            # lista para almacenar los indices
    dTheta =   np.pi /N   # angulo que hay entre cada iteracion de la coordenada theta
    dPhi =   2* np.pi /N     # angulo que hay entre cada iteracion de la coordenada phi
    rho = 0.3               # radio de la esfera
    c = 0                   # contador de vertices, para ayudar a indicar los indices


    # Se recorre la coordenada theta
    for i in range(N):
        
        theta = i * dTheta # angulo theta en esta iteracion
        theta1 = (i + 1) * dTheta # angulo theta en la iteracion siguiente
         # Se recorre la coordenada phi
        for j in range(N):
            phi = j*dPhi # angulo phi en esta iteracion
            phi1 = (j+1)*dPhi # angulo phi en la iteracion siguiente

            # Se crean los vertices necesarios son coordenadas esfericas para cada iteracion

            # Vertice para las iteraciones actuales de theta (i) y phi (j) 
            v0 = [rho*np.sin(theta)*np.cos(phi), rho*np.sin(theta)*np.sin(phi), rho*np.cos(theta)]
            # Vertice para las iteraciones siguiente de theta (i + 1) y actual de phi (j) 
            v1 = [rho*np.sin(theta1)*np.cos(phi), rho*np.sin(theta1)*np.sin(phi), rho*np.cos(theta1)]
            # Vertice para las iteraciones actual de theta (i) y siguiente de phi (j + 1) 
            v2 = [rho*np.sin(theta1)*np.cos(phi1), rho*np.sin(theta1)*np.sin(phi1), rho*np.cos(theta1)]
            # Vertice para las iteraciones siguientes de theta (i + 1) y phi (j + 1) 
            v3 = [rho*np.sin(theta)*np.cos(phi1), rho*np.sin(theta)*np.sin(phi1), rho*np.cos(theta)]

            # Se crean los vectores normales para cada vertice segun los valores de rho tongo 
            n0 = [np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)]
            n1 = [np.sin(theta1)*np.cos(phi), np.sin(theta1)*np.sin(phi), np.cos(theta1)]
            n2 = [np.sin(theta1)*np.cos(phi1), np.sin(theta1)*np.sin(phi1), np.cos(theta1)]
            n3 = [np.sin(theta)*np.cos(phi1), np.sin(theta)*np.sin(phi1), np.cos(theta)]


            # Creamos los triangulos superiores
            #        v0
            #       /  \
            #      /    \
            #     /      \
            #    /        \
            #   /          \
            # v1 ---------- v2
            if i == 0:
                #           vertices           UV coord    normales
                vertices += [v0[0], v0[1], v0[2], (k +( 0.5 + np.arctan2(v0[0],v0[2])/(2*np.pi)))/3  , (l +(0.5-np.arctan(v0[1]/rho*(2*np.pi/5))/np.pi))/6, n0[0], n0[1], n0[2]]
                vertices += [v1[0], v1[1], v1[2], (k +(0.5 + np.arctan2(v1[0],v1[2])/(2*np.pi)))/3  , (l +(0.5-np.arctan(v1[1]/rho*(2*np.pi/5))/np.pi))/6, n1[0], n1[1], n1[2]]
                vertices += [v2[0], v2[1], v2[2], (k +(0.5 + np.arctan2(v2[0],v2[2])/(2*np.pi)))/3  , (l +(0.5-np.arctan(v2[1]/rho*(2*np.pi/5))/np.pi))/6, n2[0], n2[1], n2[2]]
                indices += [ c + 0, c + 1, c +2 ]
                c += 3
            
            # Creamos los triangulos inferiores
            # v0 ---------- v3
            #   \          /3
            #    \        /
            #     \      /
            #      \    /
            #       \  /
            #        v1
            elif i == N:
                #           vertices           UV coord    normales
                vertices += [v0[0], v0[1], v0[2],(k + (0.5+ np.arctan2(v0[0],v0[2])/(2*np.pi)))/3  , (l + (0.5-np.arctan(v0[1]/rho*(2*np.pi/5))/np.pi))/6, n0[0], n0[1], n0[2]]
                vertices += [v1[0], v1[1], v1[2],(k + (0.5+ np.arctan2(v1[0],v1[2])/(2*np.pi)))/3  , (l + (0.5-np.arctan(v1[1]/rho*(2*np.pi/5))/np.pi))/6, n1[0], n1[1], n1[2]]
                vertices += [v3[0], v3[1], v3[2],(k + (0.5+ np.arctan2(v3[0],v3[2])/(2*np.pi)))/3  , (l + (0.5-np.arctan(v3[1]/rho*(2*np.pi/5))/np.pi))/6, n3[0], n3[1], n3[2]]
                indices += [ c + 0, c + 1, c +2 ]
                c += 3
            
            # Creamos los quads intermedios
            #  v0 -------------- v3
            #  | \                |
            #  |    \             |
            #  |       \          |
            #  |          \       |
            #  |             \    |
            #  |                \ |
            #  v1 -------------- v2
            else: 
                #           vertices           UV coord    normales
                vertices += [v0[0], v0[1], v0[2],(k+ (0.5 + np.arctan2(v0[0],v0[2])/(2*np.pi)))/3  , (l + (0.5-np.arctan(v0[1]/rho*(2*np.pi/5))/np.pi))/6, n0[0], n0[1], n0[2]]
                vertices += [v1[0], v1[1], v1[2],(k+ (0.5 + np.arctan2(v1[0],v1[2])/(2*np.pi)))/3  , (l + (0.5-np.arctan(v1[1]/rho*(2*np.pi/5))/np.pi))/6, n1[0], n1[1], n1[2]]
                vertices += [v2[0], v2[1], v2[2],(k+ (0.5 + np.arctan2(v2[0],v2[2])/(2*np.pi)))/3  , (l + (0.5-np.arctan(v2[1]/rho*(2*np.pi/5))/np.pi))/6, n2[0], n2[1], n2[2]]
                vertices += [v3[0], v3[1], v3[2],(k+ (0.5 + np.arctan2(v3[0],v3[2])/(2*np.pi)))/3  , (l + (0.5-np.arctan(v3[1]/rho*(2*np.pi/5))/np.pi))/6, n3[0], n3[1], n3[2]]
                indices += [ c + 0, c + 1, c +2 ]
                indices += [ c + 2, c + 3, c + 0 ]
                c += 4
    return bs.Shape(vertices, indices)


def createTexSphereNode(posx,posy,posz,pipeline,i,j):
    # Funcion para crear Grafo de una esfera texturizada de la escena, se separa en otro grafo, por si se quiere dibujar con otro material
    sphere = createTextureGPUShape(createTextureNormalSphere(15,i,j), pipeline, "sprites/Balls.png") # Shape de la esfera texturizada


    rotationSphere = sg.SceneGraphNode("rot_sphere")
    rotationSphere.transform = tr.identity()
    rotationSphere.childs = [sphere]
    # Nodo de la esfera trasladado y escalado
    sphereNode = sg.SceneGraphNode("sphere")
    sphereNode.transform =tr.matmul([
        tr.translate(posx,posy,posz),
        tr.rotationY(-np.pi/2),
        tr.scale(0.3,0.3,0.3)
    ])
    sphereNode.childs = [rotationSphere]

    # Nodo del del objeto escalado con el mismo valor de la escena base
    scaledSphere = sg.SceneGraphNode("sc_sphere")
    scaledSphere.transform = tr.scale(5, 5, 5)
    scaledSphere.childs = [sphereNode]

    return scaledSphere

def createShadowNode(posx,posy,posz,pipeline,i,j):
    BlackCircle = createGPUShape(pipeline, bs.createColorCircle(20,0.,0.,0.)) # Shape del circulo negro

    # Nodo de la esfera trasladado y escalado
    ShadowNode = sg.SceneGraphNode("shadow")
    ShadowNode.transform =tr.matmul([
        tr.translate(posx,posy,posz),
        tr.rotationY(-np.pi/2),
        tr.scale(0.3,0.3,1)
    ])
    ShadowNode.childs = [BlackCircle]

    # Nodo del del objeto escalado con el mismo valor de la escena base
    scaledShadow = sg.SceneGraphNode("sc_sphere")
    scaledShadow.transform = tr.scale(5, 5,1)
    scaledShadow.childs = [ShadowNode]
    
    return scaledShadow

def evalMixCurve0(N):
    # Funcion para generar N puntos entre 0 y 1 de una curva personalizada
    # Hermite + Bezier para modelar la superficie de un auto

    # Puntos de Control
    P0 = np.array([[-0.25, 0., 0]]).T
    P1 = np.array([[-0.25, 0.25, 0]]).T
    P2 = np.array([[0.25, 0.25, 0]]).T
    P3 = np.array([[0.25, 0., 0]]).T
    
    # Matriz de Beziers
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

def evalMixCurve1(N):
    # Funcion para generar N puntos entre 0 y 1 de una curva personalizada
    # Hermite + Bezier para modelar la superficie de un auto

    # Puntos de Control
    P0 = np.array([[-0.25, -0.2, 0]]).T
    P1 = np.array([[-0.25, 0.0, 0]]).T
    P2 = np.array([[0.25, 0.0, 0]]).T
    P3 = np.array([[0.25, -0.2, 0]]).T
    
    # Matriz de Beziers
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

def evalMixCurve2(N):
    # Funcion para generar N puntos entre 0 y 1 de una curva personalizada
    # Hermite + Bezier para modelar la superficie de un auto

    # Puntos de Control
    P0 = np.array([[-0.3, -0.25, 0]]).T
    P1 = np.array([[-0.25, -0.3, 0]]).T
    P2 = np.array([[0.25, -0.3, 0]]).T
    P3 = np.array([[0.3, -0.25, 0]]).T
    
    # Matriz de Beziers
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

def evalMixCurve3(N):
    # Funcion para generar N puntos entre 0 y 1 de una curva personalizada
    # Hermite + Bezier para modelar la superficie de un auto

    # Puntos de Control
    P0 = np.array([[-0.25, 0., 0]]).T
    P1 = np.array([[-0.25, 0.1, 0]]).T
    P2 = np.array([[0.25, 0.1, 0]]).T
    P3 = np.array([[0.25, 0., 0]]).T
    
    # Matriz de Beziers
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

def createWhite(r, g, b):
    # Crea un shape del chasis de un auto a partir de una curva personalizada
    vertices = []
    indices = []
    curve = evalMixCurve0(64) # Se obtienen los puntos de la curva
    curve2 = evalMixCurve1(64) # Se obtienen los puntos de la curva
    counter = 0 # Contador de vertices, para indicar los indices

    # Se generan los vertices
    for i in range(len(curve)-1):
        c_0 = curve[i] # punto i de la curva
        r_0 = curve2[i]# punto i de la recta
        c_1 = curve[i + 1] # punto i + 1 de la curva
        r_1 = curve2[i + 1] # punto i + 1 de la recta
        vertices += [c_0[0], c_0[1], 0, r + 0.3, g + 0.3, b + 0.3]
        vertices += [r_0[0], r_0[1], 0, r, g, b]
        vertices += [c_1[0], c_1[1], 0, r + 0.3, g + 0.3, b + 0.3]
        vertices += [r_1[0], r_1[1], 0, r, g, b]
        indices += [counter + 0, counter +1, counter + 2]
        indices += [counter + 2, counter + 3, counter + 1]
        counter += 4

    return bs.Shape(vertices, indices)

def createWood(r, g, b):
    # Crea un shape del chasis de un auto a partir de una curva personalizada
    vertices = []
    indices = []
    curve = evalMixCurve3(64) # Curva arriba
    curve2 = evalMixCurve2(64) # Curva abajo
    counter = 0 # Contador de vertices, para indicar los indices

    # Se generan los vertices
    for i in range(len(curve)-1):
        c_0 = curve[i] # punto i de la curva
        r_0 = curve2[i] # punto i de la recta
        c_1 = curve[i + 1] # punto i + 1 de la curva
        r_1 = curve2[i+1] # punto i + 1 de la recta
        vertices += [c_0[0], c_0[1], 0, r + 0.2, g + 0.2, b + 0.2]
        vertices += [r_0[0], r_0[1], 0, r, g, b]
        vertices += [c_1[0], c_1[1], 0, r + 0.2, g + 0.2, b + 0.2]
        vertices += [r_1[0], r_1[1], 0, r, g, b]
        indices += [counter + 0, counter +1, counter + 2]
        indices += [counter + 2, counter + 3, counter + 1]
        counter += 4

    return bs.Shape(vertices, indices)

def createStick(pipeline):
    # Se crea la escena del auto de la pregunta 1

    # Se crean las shapes en GPU
    gpuWhitePol = createGPUShape(pipeline, createWhite(250/255, 250/255, 250/255) ) # Punta
    gpuBrownPol = createGPUShape(pipeline, createWood(158/255, 128/255, 100/255)) # Palo largo
    gpuBlackPol = createGPUShape(pipeline, createWhite(0/255, 0/255, 0/255)) #Adorno

    # Nodo del palo grande
    WoodNode = sg.SceneGraphNode("BrownStick")
    WoodNode.transform = tr.matmul([tr.translate(0.,0.,0.) , tr.scale(0.25,2,0)])
    WoodNode.childs = [gpuBrownPol]

    # Nodo de la punta
    WhiteNode = sg.SceneGraphNode("tip")
    WhiteNode.transform = tr.matmul([tr.translate(0.1,0.12,0.) , tr.scale(0.2,0.15,0)])
    WhiteNode.childs = [gpuWhitePol]

    # Nodo de Raya 1
    DesignNode1 = sg.SceneGraphNode("design1")
    DesignNode1.transform = tr.matmul([tr.translate(0.,-0.11,0.) , tr.scale(0.27,0.05,0)])
    DesignNode1.childs = [gpuBlackPol]

    # Nodo de Raya 2
    DesignNode2 = sg.SceneGraphNode("design2")
    DesignNode2.transform = tr.matmul([tr.translate(0.,-0.13,0.) , tr.scale(0.27,0.05,0)])
    DesignNode2.childs = [gpuBlackPol]

    # Nodo de Raya 3
    DesignNode3 = sg.SceneGraphNode("design3")
    DesignNode3.transform = tr.matmul([tr.translate(0.,-0.15,0.) , tr.scale(0.27,0.05,0)])
    DesignNode3.childs = [gpuBlackPol]

    # Union
    StickNode = sg.SceneGraphNode("StickUnion")
    StickNode.transform = tr.matmul([tr.scale(0.7,2,0),tr.translate(0,0.2,0)])
    StickNode.childs = [WoodNode,WhiteNode,DesignNode1,DesignNode2,DesignNode3]

    # Nodo padre 
    FinalNode = sg.SceneGraphNode("Stick")
    FinalNode.transform =tr.matmul([
        tr.rotationY(-np.pi/2),
        tr.scale(0.3,0.3,1)
    ])
    FinalNode.childs = [StickNode]

    return FinalNode

