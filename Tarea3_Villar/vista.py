""" Tarea 3"""

import glfw
from OpenGL.GL import *
import numpy as np
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.performance_monitor as pm
import grafica.lighting_shaders as ls
import grafica.scene_graph as sg
import grafica.newLightShaders as nl
import Controlador as crt
import Modelo as mod
import random 



if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 900
    height = 900
    title = "Tarea 3 Poll"

    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    controller = crt.Controller()
    glfw.set_key_callback(window, controller.on_key)

    glClearColor(0.75, 0.75, 0.75, 1.0)
    glEnable(GL_DEPTH_TEST)

    # Pipeline con shaders con multiples fuentes de luz
    phongPipeline = nl.MultiplePhongShaderProgram()
    phongTexPipeline = nl.MultipleTexturePhongShaderProgram()
    Pipeline = es.SimpleModelViewProjectionShaderProgram()
    
    scene = mod.createScene(phongPipeline,Pipeline)
    vara = crt.objeto()
    sombra = crt.Shadow()

    white_b = crt.Pool_Ball(phongTexPipeline,[-1.0,0.0,-0.9],np.array([1.0,0.8,0.0]),2,5)
    white_b.move(0,0,0)
    
    balls = []
    shadows = []

    k = 0
    for i in range(6):
        for j in range(3):
            velocity = np.array([random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), 0.0])
            balls.append(crt.Pool_Ball(phongTexPipeline,[1.0,0.0,-0.9],velocity,j,i))
            shadows.append(crt.Shadow()) #Sombra de cada bola
            k += 1
            if k >= 15:
                break
        if k >=15:
            break

    count =[0,0]
    trans = [np.sin(np.pi/3) * 0.1 *2, -0.1]

    for i in balls:
        i.move(0.15 + trans[0]* count[0],trans[1]*count[1], 0)
        if count[0] == count[1]:
            count[0] += 1
            count[1] = -count[0]
        else:
            count[1] +=2 

    vel_angular = np.array([random.uniform(-0.1,0.1), random.uniform(-0.1,0.1), 0.0],dtype= np.float32)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    t0 = glfw.get_time()

    # Application loop
    while not glfw.window_should_close(window):
        # Variables del tiempo
        t1 = glfw.get_time()
        delta = t1 -t0
        t0 = t1

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Using GLFW to check for input events
        glfw.poll_events()
        perfMonitor.update(glfw.get_time())


        controller.update_camera(delta,np.array([white_b.position[0],white_b.position[1],0.0],dtype=np.float32))
        camera = controller.get_camera()
        viewMatrix = camera.update_view()
        deltaTime = perfMonitor.getDeltaTime()

        # Setting up the projection transform
        projection = tr.perspective(60, float(width) / float(height), 0.1, 100)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Setting all uniform shader variables
        glUseProgram(phongPipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "La"), 0.25, 0.25, 0.25)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ld"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Kd"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "viewPosition"), camera.eye[0], camera.eye[1], camera.eye[2])
        glUniform1ui(glGetUniformLocation(phongPipeline.shaderProgram, "shininess"), 100)
        
        glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "constantAttenuation"), 0.01)
        glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "quadraticAttenuation"), 0.05)

        glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)

        #Mesa de pool
        sg.drawSceneGraphNode(scene, phongPipeline, "model")
        

        glUseProgram(Pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(Pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(Pipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)
        glUniformMatrix4fv(glGetUniformLocation(Pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())

        vara.move(white_b.position[0]+0.4,white_b.position[1],-0.8)
        vara.draw_call(Pipeline)

        #Sombra de la bola blanca
        sombra.move(white_b.position[0],white_b.position[1],-0.093)
        sombra.draw_call(Pipeline)

        #sombra de las demás pelotas
        for i in balls:
            sombra.move(i.position[0]+2,i.position[1],-0.093)       
            sombra.draw_call(Pipeline)

        # Se dibuja con el pipeline de texturas
        glUseProgram(phongTexPipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "La"), 0.25, 0.25, 0.25)
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ld"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ls"), 0.5, 0.5, 0)

        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Kd"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "viewPosition"), camera.eye[0], camera.eye[1], camera.eye[2])
        glUniform1ui(glGetUniformLocation(phongTexPipeline.shaderProgram, "shininess"), 100)
        
        glUniform1f(glGetUniformLocation(phongTexPipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(phongTexPipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(phongTexPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(phongTexPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(phongTexPipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)
        
        for i in balls:
            i.action(np.array([0., 0.,0.], dtype=np.float32),vel_angular, deltaTime)
            i.vel_angular()
            crt.collideWithBorder(i)
        
        white_b.action(np.array([0.0, 0.0,0.0], dtype=np.float32),np.array([0.0,0.0,0.0],dtype=np.float32), deltaTime)
        crt.collideWithBorder_w(white_b)


        for i in range(len(balls)):
            for j in range(i+1, len(balls)):
                if crt.areColliding(balls[i], balls[j]):
                    crt.collide(balls[i], balls[j])
            #if crt.areColliding(balls[i],white_b):
            #    crt.collide(balls[i],white_b)


        for i in balls:
            i.draw_call(phongTexPipeline)

        white_b.draw_call(phongTexPipeline)

        #End
        glfw.swap_buffers(window)

  
    scene.clear()
    for i in balls:
        i.clear()
    glfw.terminate()