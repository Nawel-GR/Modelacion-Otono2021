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

    width = 800
    height = 800
    title = "Tarea 3 Poll"

    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    controller = crt.Controller()
    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controller.on_key)

    # Pipeline con shaders con multiples fuentes de luz
    phongPipeline = nl.MultiplePhongShaderProgram()
    phongTexPipeline = nl.MultipleTexturePhongShaderProgram()

    # This shader program does not consider lighting
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.75, 0.75, 0.75, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuAxis = mod.createGPUShape(mvpPipeline, bs.createAxis(4))
    
    scene = mod.createScene(phongPipeline,mvpPipeline)

    #vara = crt.objeto()
    '''
    Spheres = []
    balls = crt.Balls()
    white_b = crt.white_ball()
    #shadow_White = crt.Shadow()
    balls.pos_inicial()   
    '''
    balls = []
    white_b = crt.Balls(phongTexPipeline,[-1.0,0.0,-0.9],np.array([1.0,0.8,0.0]),0,5)

    white_b.update_pos(0,0,0)
    k = 0

    for i in range(6):
        for j in range(3):
            #eliminable
            velocity = np.array([
            random.uniform(-1.0, 1.0),
            random.uniform(-1.0, 1.0),
            0.0
            ])
            balls.append(crt.Balls(phongTexPipeline,[1.0,0.0,-0.9],velocity,j,i))
            
            k += 1
            if k >= 15:
                break
        if k >=15:
            break


    contador =[0,0]
    trans_coord = [np.sin(np.pi/3) * 0.1 *2, -0.1]

    for i in balls:
        i.update_pos(0.15 + trans_coord[0]* contador[0],trans_coord[1]*contador[1], 0)

        if contador[0] == contador[1]:
            contador[0] += 1
            contador[1] = -contador[0]

        else:
            contador[1] +=2 

    vel_angular = np.array([
        random.uniform(-0.2,0.2),
        random.uniform(-0.2,0.2),
        0.0
    ],dtype= np.float32)

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

        # Using GLFW to check for input events
        glfw.poll_events()
        perfMonitor.update(glfw.get_time())

        #controller.update_camera(delta)
        controller.update_camera(delta,np.array([white_b.position[0],white_b.position[1],0.0],dtype=np.float32))
        camera = controller.get_camera()
        viewMatrix = camera.update_view()
        deltaTime = perfMonitor.getDeltaTime()

        # Setting up the projection transform
        projection = tr.perspective(60, float(width) / float(height), 0.1, 100)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # The axis is drawn without lighting effects        
        glUseProgram(mvpPipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        #mvpPipeline.drawCall(gpuAxis, GL_LINES)

        #vara.move(controller.Q_value,controller.W_value,0)
        #vara.draw_call(mvpPipeline)

        lightingPipeline = phongPipeline
        lightposition = [0, 0, 2.3]

        # Setting all uniform shader variables
        glUseProgram(lightingPipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), 0.25, 0.25, 0.25)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        # Ya no se necesita la posicion de la fuentes de lus, se declaran constantes en los shaders
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), camera.eye[0], camera.eye[1], camera.eye[2])
        glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 100)
        
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.01)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.05)

        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)

        # Drawing
        sg.drawSceneGraphNode(scene, lightingPipeline, "model")
        
        # Se dibuja con el pipeline de texturas
        glUseProgram(phongTexPipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "La"), 0.25, 0.25, 0.25)
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ld"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ls"), 0.5, 0.5, 0)

        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Kd"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        # Ya no se necesita la posicion de la fuentes de lus, se declaran constantes en los shaders
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "viewPosition"), camera.eye[0], camera.eye[1], camera.eye[2])
        glUniform1ui(glGetUniformLocation(phongTexPipeline.shaderProgram, "shininess"), 100)
        
        glUniform1f(glGetUniformLocation(phongTexPipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(phongTexPipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(phongTexPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(phongTexPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(phongTexPipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)
        
        #white_b.move(controller.Q_value,controller.W_value,0)
        
        #balls.draw_call(phongTexPipeline)
        #white_b.draw_call(phongTexPipeline)
        
        for ball in balls:
            # moving each circle
            ball.action(np.array([0.0, 0.0,0.0], dtype=np.float32),vel_angular, deltaTime)
            ball.vel_angular()


            # checking and processing collisions against the border
            crt.collideWithBorder(ball)
        

            
        white_b.action(np.array([0.0, 0.0,0.0], dtype=np.float32),np.array([0.0,0.0,0.0],dtype=np.float32), deltaTime)
        crt.collideWithBorder_white(white_b)


        for i in range(len(balls)):
                for j in range(i+1, len(balls)):
                    if crt.areColliding(balls[i], balls[j]):
                        crt.collide(balls[i], balls[j])
                    #elif areColliding(white_b,balls[j]):
                    #    collide(white_b,balls[j])
                    #elif areColliding(white_b,balls[i]):
                    #    collide(white_b,balls[i])

        for ball in balls:
            ball.draw_call(phongTexPipeline)


        white_b.draw_call(phongTexPipeline)




        # Once the drawing is rendered, buffers are 
        # swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    gpuAxis.clear()
    scene.clear()
    #for i in Spheres:
    #    i.clear()
    glfw.terminate()