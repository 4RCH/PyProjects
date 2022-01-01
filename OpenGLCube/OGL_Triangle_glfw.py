import glfw
from OpenGL.GL import *
import numpy as np


surface = (640,480)
pos_center = ()

def screenres(monitor = 0):
    monitorsID = monitor
    monitorsID = glfw.get_monitors()
    monitor_info = glfw.get_video_mode(monitorsID[0])
    monitor_used = monitor_info[0]
    screen_res = (monitor_used.width, monitor_used.height)
    return screen_res

def win_pos_middle():
    screen_res = screenres()
    xpos = (screen_res[0]/2)-(surface[0]/2),(screen_res[1]/2)-(surface[1]/2)
    return xpos

def triangle():
    vertices = [-0.5, -0.5, 0.0, 0.5, -0.5, 0.0, 0.0,0.5, 0.0]
    vertColours = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
    
    vertices = np.array(vertices, dtype=np.float32)
    vertColours = np.array(vertColours, dtype=np.float32)
    triInfo = (vertices, vertColours)
    return triInfo

if not glfw.init():
    raise Exception ("glfw not initialized")

gabe_window = glfw.create_window(surface[0], surface[1], "Triangle window - Fixed Function Pipeline", None, None)

if not gabe_window:
    glfw.terminate()
    raise Exception ("window was not created")

glfw.set_window_pos(gabe_window, 128, 128)
glfw.make_context_current(gabe_window)

glClearColor(0.1, 0.1, 0.1, 1)

polyTri = triangle()
for i in polyTri:
    print (i)

glEnableClientState(GL_VERTEX_ARRAY)
glVertexPointer(3, GL_FLOAT, 0, polyTri[0])

glEnableClientState(GL_COLOR_ARRAY)
glColorPointer(3, GL_FLOAT, 0, polyTri[1])


def main():
    while not glfw.window_should_close(gabe_window):
        glfw.poll_events()
        # Things to check while the program runs
        glClear(GL_COLOR_BUFFER_BIT)
        
        glRotatef(0.1, 0, 1, 0)
        
        
        glDrawArrays(GL_TRIANGLES, 0, 3)
        
        glfw.swap_buffers(gabe_window)

main()
glfw.terminate()