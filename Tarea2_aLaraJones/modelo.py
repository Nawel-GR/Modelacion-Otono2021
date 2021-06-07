"""
Nahuel Gómez, CC3501, 2020-1
Tarea 2_a
Modelo
"""

import openmesh as om
import numpy as np
import math
import random

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


def crear_piso(matriz):
    piso_mesh= om.TriMesh()

    xs = np.linspace(-5, 5, len(matriz))
    ys = np.linspace(-5, 5, len(matriz[0]))

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            x=xs[i]
            y =ys[j]
            z= matriz[i][j][0]
            print(z,",")
            piso_mesh.add_vertex([x,y,z])

    index = lambda i, j: i*len(ys) + j 

    for i in range(len(xs)-1):
        for j in range(len(ys)-1):
            
            # Conseguimos los indices por cada cuadrado
            isw = index(i,j)
            ise = index(i+1,j)
            ine = index(i+1,j+1)
            inw = index(i,j+1)

            # Obtenemos los vertices, y agregamos las caras
            vertexs = list(piso_mesh.vertices())

            piso_mesh.add_face(vertexs[isw], vertexs[ise], vertexs[ine])
            piso_mesh.add_face(vertexs[ine], vertexs[inw], vertexs[isw])

    return piso_mesh

def crear_techo(matriz):
    techo_mesh= om.TriMesh()

    xs = np.linspace(-5, 5, len(matriz))
    ys = np.linspace(-5, 5, len(matriz[1]))

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            x=xs[i]
            y =ys[j]
            z= matriz[i][j][1]
            print(z)
            techo_mesh.add_vertex([x,y,z])

    index = lambda i, j: i*len(ys) + j 

    for i in range(len(xs)-1):
        for j in range(len(ys)-1):
            
            # Conseguimos los indices por cada cuadrado
            isw = index(i,j)
            ise = index(i+1,j)
            ine = index(i+1,j+1)
            inw = index(i,j+1)

            # Obtenemos los vertices, y agregamos las caras
            vertexs = list(techo_mesh.vertices())

            techo_mesh.add_face(vertexs[isw], vertexs[ise], vertexs[ine])
            techo_mesh.add_face(vertexs[ine], vertexs[inw], vertexs[isw])

    return techo_mesh


def get_vertexs_and_indexes(mesh):
    # Obtenemos las caras de la malla
    faces = mesh.faces()

    # Creamos una lista para los vertices e indices
    vertexs = []

    # Obtenemos los vertices y los recorremos
    for vertex in mesh.points():
        vertexs += vertex.tolist()
        # Agregamos un color al azar
        vertexs += [random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)]

    indexes = []

    for face in faces:
        # Obtenemos los vertices de la cara
        face_indexes = mesh.fv(face)
        for vertex in face_indexes:
            # Obtenemos el numero de indice y lo agregamos a la lista
            indexes += [vertex.idx()]

    return vertexs, indexes

def get_vertexs_and_indexes_tex(mesh):
    # Obtenemos las caras de la malla
    faces = mesh.faces()

    # Creamos una lista para los vertices e indices
    vertexs = []
    i = 0
    # Obtenemos los vertices y los recorremos
    for vertex in mesh.points():
        vertexs += vertex.tolist()
        # Agregamos un color al azar    
        if i == 0:
            vertexs += [0,0]
            i+= 1
        elif i == 1:      
            vertexs += [1/12,0]
            i+= 1
        elif i == 2:
            vertexs += [1/12,1]
            i += 1
        elif i == 3:
            vertexs += [0,1]
            i=0
        
    indexes = []

    for face in faces:
        # Obtenemos los vertices de la cara
        
        face_indexes = mesh.fv(face)
        for vertex in face_indexes:
            # Obtenemos el numero de indice y lo agregamos a la lista
            indexes += [vertex.idx()]

    return vertexs, indexes

def get_vertexs_and_indexes_tex1(mesh):
    # Obtenemos las caras de la malla
    faces = mesh.faces()

    # Creamos una lista para los vertices e indices
    vertexs = []
    i = 0
    # Obtenemos los vertices y los recorremos
    for vertex in mesh.points():
        vertexs += vertex.tolist()
        # Agregamos un color al azar    
        if i == 0:
            vertexs += [1/12,0]
            i+= 1
        elif i == 1:      
            vertexs += [2/12,0]
            i+= 1
        elif i == 2:
            vertexs += [1/12,1]
            i = 0
        elif i == 3:
            vertexs += [2/12,1]
            i=0
        
    indexes = []

    for face in faces:
        # Obtenemos los vertices de la cara
        
        face_indexes = mesh.fv(face)
        for vertex in face_indexes:
            # Obtenemos el numero de indice y lo agregamos a la lista
            indexes += [vertex.idx()]

    return vertexs, indexes
