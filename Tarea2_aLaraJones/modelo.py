"""
Nahuel Gómez, CC3501, 2020-1
Tarea 2_a
Modelo
"""

import openmesh as om
import numpy as np
import math
import random
from OpenGL.GL import *
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.ex_curves as cv
import grafica.scene_graph as sg

def create_quad():
    # Creamos una malla de triangulos
    mesh = om.TriMesh()

    #  2 ==== 1
    #  |\   0 |
    #  | \    |
    #  |   \  |
    #  |    \ |
    #  | 1   \|
    #  3 ==== 0

    # Agregamos algunos vertices a la malla
    vh0 = mesh.add_vertex([0.5, -0.5, 0])
    vh1 = mesh.add_vertex([0.5, 0.5, 0])
    vh2 = mesh.add_vertex([-0.5, 0.5, 0])
    vh3 = mesh.add_vertex([-0.5, -0.5, 0])

    # Agregamos algunas caras a la malla
    fh0 = mesh.add_face(vh0, vh1, vh2)
    fh1 = mesh.add_face(vh0, vh2, vh3)

    return mesh

def _create(matriz,tipo):#tipo = 0 = piso, tipo 1 = techo
    _mesh= om.TriMesh()

    xs = np.linspace(-5, 5, len(matriz))
    ys = np.linspace(-5, 5, len(matriz[tipo]))

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            x=xs[i]
            y =ys[j]
            z= matriz[i][j][tipo]
            _mesh.add_vertex([x,y,z])

    index = lambda i, j: i*len(ys) + j 

    for i in range(len(xs)-1):
        for j in range(len(ys)-1):
            
            # indice por cuadro
            i_1 = index(i,j)
            i_2 = index(i+1,j)
            i_3 = index(i+1,j+1)
            i_4 = index(i,j+1)
            # Obtenemos los vertices, y agregamos las caras
            vertexs = list(_mesh.vertices())

            _mesh.add_face(vertexs[i_1], vertexs[i_2], vertexs[i_3])
            _mesh.add_face(vertexs[i_3], vertexs[i_4], vertexs[i_1])
            
            if i %4 == 0:
                _mesh.set_texcoord2D(vertexs[i_4], [i+j,i+j+1])
                _mesh.set_texcoord2D(vertexs[i_3], [i+j+1,i+j+1])
                _mesh.set_texcoord2D(vertexs[i_2], [i+j+1,i+j])
                _mesh.set_texcoord2D(vertexs[i_1], [i+j,i+j])
                   
            if i%4 == 1:
                _mesh.set_texcoord2D(vertexs[i_1], [i+j,i+j+1])
                _mesh.set_texcoord2D(vertexs[i_2], [i+j+1,i+j+1])
                _mesh.set_texcoord2D(vertexs[i_3], [i+j+1,i+j])
                _mesh.set_texcoord2D(vertexs[i_4], [i+j,i+j])
                
            if i%4 == 2:
                _mesh.set_texcoord2D(vertexs[i_2], [i+j,i+j+1])
                _mesh.set_texcoord2D(vertexs[i_1], [i+j+1,i+j+1])
                _mesh.set_texcoord2D(vertexs[i_4], [i+j+1,i+j])
                _mesh.set_texcoord2D(vertexs[i_3], [i+j,i+j])
                
            if i%4 == 3:
                _mesh.set_texcoord2D(vertexs[i_3], [i+j,i+j+1])
                _mesh.set_texcoord2D(vertexs[i_4], [i+j+1,i+j+1])
                _mesh.set_texcoord2D(vertexs[i_1], [i+j+1,i+j])
                _mesh.set_texcoord2D(vertexs[i_2], [i+j,i+j])       
    return _mesh

def toShape(mesh):

    # Requesting normals per face
    mesh.request_face_normals()

    # Requesting normals per vertex
    mesh.request_vertex_normals()

    # Computing all requested normals
    mesh.update_normals()

    # At this point, we are sure we have normals computed for each face.
    assert mesh.has_face_normals()

    vertices = []
    indices = []

    def extractCoordinates(numpyVector3):
        assert len(numpyVector3) == 3
        x = vertex[0]
        y = vertex[1]
        z = vertex[2]
        return [x,y,z]

    # Checking each face
    for faceIt in mesh.faces():

        # Checking each vertex of the face
        for faceVertexIt in mesh.fv(faceIt):

            # Obtaining the position and normal of each vertex
            vertex = mesh.point(faceVertexIt)
            normal = mesh.normal(faceVertexIt)

            x, y, z = extractCoordinates(vertex)
            nx, ny, nz = extractCoordinates(normal)

            texcoords = mesh.texcoord2D(faceVertexIt)
            tx = texcoords[0]
            ty = texcoords[1]
            
            vertices += [x, y, z, tx, ty, nx, ny, nz]
            indices += [len(vertices)//8 - 1]

    return bs.Shape(vertices, indices)

def toShapeRoof(mesh):
    # Requesting normals per face
    mesh.request_face_normals()

    # Requesting normals per vertex
    mesh.request_vertex_normals()

    # Computing all requested normals
    mesh.update_normals()

    # At this point, we are sure we have normals computed for each face.
    assert mesh.has_face_normals()

    vertices = []
    indices = []

    def extractCoordinates(numpyVector3):
        assert len(numpyVector3) == 3
        x = vertex[0]
        y = vertex[1]
        z = vertex[2]
        return [x,y,z]

    # Checking each face
    for faceIt in mesh.faces():

        # Checking each vertex of the face
        for faceVertexIt in mesh.fv(faceIt):

            # Obtaining the position and normal of each vertex
            vertex = mesh.point(faceVertexIt)
            normal = mesh.normal(faceVertexIt)

            x, y, z = extractCoordinates(vertex)
            nx, ny, nz = extractCoordinates(normal)

            nx = nx*-1
            ny = ny*-1
            nz = nz*-1

            texcoords = mesh.texcoord2D(faceVertexIt)
            tx = texcoords[0]
            ty = texcoords[1]
                            
            vertices += [x, y, z, tx, ty, nx, ny, nz]
            indices += [len(vertices)//8 - 1]

    return bs.Shape(vertices, indices)

def up_z(mesh,position):
    mesh_faces = mesh.faces()

    for face in mesh_faces:
        vert_f = list(mesh.fv(face))
        vert_1 = mesh.point(vert_f[0]).tolist()
        vert_2 = mesh.point(vert_f[1]).tolist()
        vert_3 = mesh.point(vert_f[2]).tolist()
        
        if (abs(vert_1[0]-position[0]) <=1 and abs(vert_1[1]-position[1])<=1):
            z = vert_1[2]           
            return z
        if (abs(vert_2[0]-position[0]) <=1 and abs(vert_2[1]-position[1])<=1):
            z = vert_2[2]           
            return z
        if (abs(vert_3[0]-position[0]) <=1 and abs(vert_3[1]-position[1])<=1):
            z = vert_3[2]           
            return z


#Creación de la pieza del rompecabezas
def createGPUShape(shape, pipeli_3):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape
    gpuShape = es.GPUShape().initBuffers()
    pipeli_3.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

def createTextureGPUShape(shape, pipeli_3, path):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape con texturas
    gpuShape = es.GPUShape().initBuffers()
    pipeli_3.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    gpuShape.texture = es.textureSimpleSetup(
        path, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    return gpuShape

def createColorCircle(N, r, g, b):
    # Funcion para crear un circulo con un color personalizado Poligono de N lados 
    vertices = [0, 0, 0, r, g, b]
    indices = []

    dtheta = 2 * math.pi / N

    for i in range(N):
        theta = i * dtheta
        vertices += [
            # vertex coordinates
            0.5 * math.cos(theta), 0.5 * math.sin(theta), 0,

            # color generates varying between 0 and 1
                  r+0.2, g+0.2, b+0.2]

        # A triangle is created using the center, this and the next vertex
        indices += [0, i, i+1]

    # The final triangle connects back to the second vertex
    indices += [0, N, 1]
    return bs.Shape(vertices, indices)


def evalMixCurve(N):
    # Puntos de Control de la curva
    P0 = np.array([[-0.1, 0.25, 0]]).T
    P1 = np.array([[-0.3, 0.5, 0]]).T
    P2 = np.array([[0.3, 0.5, 0]]).T
    P3 = np.array([[0.1, 0.25, 0]]).T
    
    # Matriz de Beziers
    B_M = cv.bezierMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 3), dtype=float)
    
    # Relleno de los puntos de la curva
    for i in range(len(ts)):
        T = cv.generateT(ts[i])
        curve[i] = np.matmul(B_M, T).T
        
    return curve


def createColorPiece(r, g, b):
    # Crea un shape de la pieza
    vertices = []
    indices = []
    curve = evalMixCurve(64) # Obtención de puntos
    delta = (1 / len(curve))/5 # distancia del step /paso
    x_0 = -0.1 # Posicion x inicial de la recta inferior
    y_0 = 0.25 # Posicion y inicial de la recta inferior
    counter = 0 # Contador de vertices

    # Se generan los vertices
    for i in range(len(curve)-1):
        c_0 = curve[i]
        r_0 = [x_0 + i*delta, y_0] 
        c_1 = curve[i + 1]
        r_1 = [x_0 + (i+1)*delta, y_0] 
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
    gpuPiece2 = createGPUShape(createColorPiece(0.9, 0.9, 0.1), pipeline) #Pieza trasera
    gpuYellowQuad2 = createGPUShape(bs.createColorQuad(0.9, 0.9, 0.1), pipeline) 
    gpuPiece1 = createGPUShape(createColorPiece(0.75, 0.75, 0.1), pipeline)#Pieza superpuesta
    gpuYellowQuad1 = createGPUShape(bs.createColorQuad(0.75, 0.75, 0.1), pipeline) 
    gpuPiece3 = createGPUShape(createColorCircle(30,0.9, 0.1, 0.1), pipeline)#Pieza extra

#Pieza Trasera
    # Nodo de la circunfernecia de arriba
    PieceNode2_1 = sg.SceneGraphNode("Piece_T")
    PieceNode2_1.childs = [gpuPiece2]

    # Nodo de la circunfernecia de la derecha
    PieceNode2_2 = sg.SceneGraphNode("Piece_T")
    PieceNode2_2.transform = tr.matmul([tr.translate(-0.05, 0.05, 0),tr.rotationZ(-1.57)])
    PieceNode2_2.childs = [gpuPiece2]


    # Nodo Cuadrado
    windowNode2 = sg.SceneGraphNode("Quad_T")
    windowNode2.transform = tr.matmul([tr.translate(-0.0, 0.05, 0), tr.scale(0.4, 0.4, 1)])
    windowNode2.childs = [gpuYellowQuad2]

    # Nodo de a figura final Grande
    piezatrasera = sg.SceneGraphNode("Quad_T")
    piezatrasera.childs = [windowNode2,PieceNode2_1,PieceNode2_2]
    
#Pieza superpuesta
    # Nodo de la circunfernecia de arriba
    PieceNode1_1 = sg.SceneGraphNode("Piece_S")
    PieceNode1_1.transform = tr.matmul([tr.translate(0.0, 0.06, 0), tr.scale(0.8, 0.8, 1)])
    PieceNode1_1.childs = [gpuPiece1]

    # Nodo de la circunfernecia de la derecha
    PieceNode1_2 = sg.SceneGraphNode("Piece_S")
    PieceNode1_2.transform = tr.matmul([tr.translate(0.01, 0.05, 0),tr.scale(0.8, 0.8, 1),tr.rotationZ(-1.57)])
    PieceNode1_2.childs = [gpuPiece1]

    # Nodo Cuadrado
    windowNode1 = sg.SceneGraphNode("Quad_S")
    windowNode1.transform = tr.matmul([tr.translate(-0.0, 0.05, 0), tr.scale(0.33, 0.33, 1)])
    windowNode1.childs = [gpuYellowQuad1]

    # Nodo de a figura final
    piezasuper = sg.SceneGraphNode("Quad_S")
    piezasuper.childs = [windowNode1,PieceNode1_1,PieceNode1_2]

#Pieza Extra
    # Nodo de la circunfernecia de arriba
    PieceNode3_1 = sg.SceneGraphNode("Piece_S")
    PieceNode3_1.transform = tr.matmul([tr.translate(0.0, 0.33, 0), tr.scale(0.1, 0.1, 1)])
    PieceNode3_1.childs = [gpuPiece3]

    # Nodo de la circunfernecia de la derecha
    PieceNode3_2 = sg.SceneGraphNode("Piece_S")
    PieceNode3_2.transform = tr.matmul([tr.translate(0.28, 0.05, 0),tr.scale(0.1, 0.1, 1)])
    PieceNode3_2.childs = [gpuPiece3]

    # Nodo Cuadrado
    windowNode3 = sg.SceneGraphNode("Quad_S")
    windowNode3.transform = tr.matmul([tr.translate(-0.0, 0.05, 0), tr.scale(0.2, 0.2, 1)])
    windowNode3.childs = [gpuYellowQuad2] #Se reutiliza

    # Nodo de a figura final
    piezaextr = sg.SceneGraphNode("Quad_S")
    piezaextr.childs = [windowNode3,PieceNode3_1,PieceNode3_2]

    # Nodo que junta
    PreFinalNodePiece = sg.SceneGraphNode("FinalPiece")
    PreFinalNodePiece.childs = [piezatrasera,piezasuper,piezaextr]

    # Nodo padre 
    FinalNodePiece = sg.SceneGraphNode("FinalPiece")
    FinalNodePiece.childs = [PreFinalNodePiece]

    return FinalNodePiece
