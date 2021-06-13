"""
Nahuel Gómez, CC3501, 2020-1
Tarea 2_a
Vista
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import grafica.lighting_shaders as ls
import grafica.transformations as tr
import grafica.easy_shaders as es
from grafica.assets_path import getAssetPath
import modelo as pr
import controlador as crt



if __name__ == "__main__":

    if len(sys.argv)!=4:
        print("ingrese el input indicado porfavor")
        exit()

    cave=sys.argv[1]
    texture= sys.argv[2]
    N=(int(sys.argv[3]))

    cave = np.load(cave)

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 1500
    height = 900

    window = glfw.create_window(width, height, "Tarea 2", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, crt.on_key)

    #Haciendo el callback para el mouse
    glfw.set_input_mode(window,glfw.CURSOR,glfw.CURSOR_DISABLED)
    glfw.set_cursor_pos_callback(window, crt.cursor_pos_callback)
    glfw.set_mouse_button_callback(window, crt.mouse_button_callback)

    # Assembling the shader program
    pipeline = es.SimpleModelViewProjectionShaderProgram()
    texpipeline_light = ls.SpotlightTexturePhongShaderProgram()
    textpipeline_nolight = es.SimpleTextureModelViewProjectionShaderProgram()
    
    # Setting up the clear screen color
    glClearColor(0.5, 0.5, 0.5, 1.0)

    # As we work in 3D, we need to check which part is in front, and which one is at the back
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST)
    
    # Gpu Piso
    Piso_mesh = pr._create(cave,0)
    shapePiso = pr.toShape(Piso_mesh)

    gpuPiso_malla = es.GPUShape().initBuffers()
    texpipeline_light.setupVAO(gpuPiso_malla)
    gpuPiso_malla.fillBuffers(shapePiso.vertices, shapePiso.indices, GL_STATIC_DRAW)
    gpuPiso_malla.texture = es.textureSimpleSetup(getAssetPath(texture), GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)    

    # Gpu Techo
    Techo_mesh = pr._create(cave,1)
    shapeTecho = pr.toShape(Techo_mesh)

    gpuTecho_malla = es.GPUShape().initBuffers()
    texpipeline_light.setupVAO(gpuTecho_malla)
    gpuTecho_malla.fillBuffers(shapeTecho.vertices, shapeTecho.indices, GL_STATIC_DRAW)
    gpuTecho_malla.texture = es.textureSimpleSetup(getAssetPath(texture), GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)

    #Se incorpora personaje
    joven = crt.Principal_dibujo()
    
    #Se incorporan piezas
    piezas_list = []

    for i in range(N):
        piezas_list.append(crt.objeto(len(cave)-5,len(cave[0])-5))

    for i in piezas_list:
        print(pr.up_z(Piso_mesh, i.posicion))
        i.update_z(pr.up_z(Piso_mesh, i.posicion))

    #variables a utilizar
    t_0, t_2 = glfw.get_time(), glfw.get_time()
    z_0, x_0 = 0. , 0.
    up = np.array((0., 0., 1.))
    viewPos = np.zeros(3)
    viewPos[2] = 2.0
    i=0
    personaje_pos = np.zeros(3)
    camera_theta = np.pi/4

    while not glfw.window_should_close(window):
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (crt.Controlador.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Getting the time difference from the previous iteration
        t_1 = glfw.get_time()
        dt = t_1 - t_0
        t_0 = t_1

        x_1, z_1 = glfw.get_cursor_pos(window)

        dz = z_1 - z_0
        z_0 = z_1

        dx = x_1 - x_0
        x_0 = x_1

        # Angulos de vision
        phi, theta = crt.Movimiento.angulo(dx, dz, dt)
        
        # Simple correction
        new_pi = phi + np.pi * 0.5

        # Vector at
        at = np.array([np.cos(phi) * np.sin(theta), np.sin(phi) * np.sin(theta), np.cos(theta)])
        
        # Side vector, this helps us define our sideway movement
        new_side = np.array([np.cos(new_pi) * np.sin(theta), np.sin(new_pi) * np.sin(theta), 0])

        # We have to redefine our at and forward vectors now considering our character's position.
        new_at = at + viewPos
        forward = new_at - viewPos

        # Move character 
        crt.Movimiento.move(window, viewPos, forward, new_side, dt)

        # Setting camera (eye, at, up)
        view = tr.lookAt(viewPos,new_at,up)

        # Setting up the projection transform
        glUseProgram(texpipeline_light.shaderProgram)
        projection = tr.perspective(60, float(width)/float(height), 0.1, 100)

        glUniformMatrix4fv(glGetUniformLocation(texpipeline_light.shaderProgram, "projection"), 1, GL_TRUE, projection)

        glUniform3f(glGetUniformLocation(texpipeline_light.shaderProgram, "La"), 0.5, 0.5, 0.5) #Solo un poquito de luz
        glUniform3f(glGetUniformLocation(texpipeline_light.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(texpipeline_light.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(texpipeline_light.shaderProgram, "Ka"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(texpipeline_light.shaderProgram, "Kd"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(texpipeline_light.shaderProgram, "Ks"), 0.0, 0.0, 0.0)

        glUniform3f(glGetUniformLocation(texpipeline_light.shaderProgram, "lightposition"),*crt.Movimiento.poslinterna)
        glUniform3f(glGetUniformLocation(texpipeline_light.shaderProgram, "lightDirection"), *new_at)
        glUniform3f(glGetUniformLocation(texpipeline_light.shaderProgram, "viewPosition"), *viewPos)
        glUniform1ui(glGetUniformLocation(texpipeline_light.shaderProgram, "focused"),10)
        glUniform1ui(glGetUniformLocation(texpipeline_light.shaderProgram, "shininess"),2)       
        glUniform1f(glGetUniformLocation(texpipeline_light.shaderProgram, "constantAttenuation"), 1.0)
        glUniform1f(glGetUniformLocation(texpipeline_light.shaderProgram, "linearAttenuation"), 0.0)
        glUniform1f(glGetUniformLocation(texpipeline_light.shaderProgram, "quadraticAttenuation"), 0.0)        

        glUniformMatrix4fv(glGetUniformLocation(texpipeline_light.shaderProgram, "view"), 1, GL_TRUE, view)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glUniformMatrix4fv(glGetUniformLocation(texpipeline_light.shaderProgram, "model"), 1, GL_TRUE, tr.uniformScale(1))
        
        #Drawcall
        texpipeline_light.drawCall(gpuPiso_malla)
        texpipeline_light.drawCall(gpuTecho_malla)

        personaje_pos[0]=new_at[0]
        personaje_pos[1]=new_at[1]

        #cambiamos de pipeline para las piezas
        glUseProgram(pipeline.shaderProgram)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.uniformScale(1))
        k=0
        for j in piezas_list:
            j.update_angle(phi)
            j.draw(pipeline)
            
            if (j.take(personaje_pos)):
                piezas_list.pop(k)
            k +=1

        #Cambiamos de pipeline para el personaje
        glUseProgram(textpipeline_nolight.shaderProgram)

        glUniformMatrix4fv(glGetUniformLocation(textpipeline_nolight.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(textpipeline_nolight.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(textpipeline_nolight.shaderProgram, "model"), 1, GL_TRUE, tr.uniformScale(1))

        if pr.up_z(Piso_mesh,personaje_pos) != None:
            personaje_pos[2]=pr.up_z(Piso_mesh,personaje_pos)+ 0.5
            viewPos[2]= personaje_pos[2]
        
        joven.update(personaje_pos,phi)

        if len(piezas_list)==0: # Ganamos
            joven.win_draw(textpipeline_nolight)

        elif  (crt.Controlador.leftClickOn ):
            if i == 4 or i == -1 :                
                i =0
            joven.draw(textpipeline_nolight,i)
            i +=1

        elif crt.Controlador.rightClickOn:
            if i == -1 or i == 4:
                i = 3
            joven.draw(textpipeline_nolight,i)
            i -=1
        
        else:
            joven.draw(textpipeline_nolight,0)

        glfw.swap_buffers(window)
    glfw.terminate()
