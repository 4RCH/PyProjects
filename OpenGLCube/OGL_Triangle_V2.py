import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

vertex_src = """
# version 330 core

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_color;

out vec3 v_color;

void main()
{
    gl_Position = vec4(a_position, 1.0);
    v_color = a_color;
}
"""

fragment_src = """
# version 330 core

in vec3 v_color;
out vec4 out_color;

void main()
{
    out_color = vec4(v_color, 1.0);
}
"""

surface = (640,480)
pos_center = ()

def window_resize(window, width, height):
    glViewport(0, 0, width, height)

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

class QuadObj(object):
    """ Creates a gabe triangle object"""

    def __init__(self):
        """Constructor"""
        self.verts = None
        self.colours = None
        self.position = (0.0,0.0,0.0)
        self.indices = None
        self.shaderPackage = ()
        
        self.vertSetup()
        self.colSetup()
        self.indexSetup()
        self.PackForShader()
    
    def vertSetup(self):
        """ Create a set of vertices"""
        self.verts = (-0.5, -0.5, 0.0,
                      0.5, -0.5, 0.0,
                      -0.5, 0.5, 0.0,
                      0.5, 0.5, 0.0,
                      0.0, 0.75, 0.0)
        print ("List of vertices: ", self.verts)
        
    def colSetup(self):
        """ Set vertex colours"""
        self.colours = (1.0, 0.0, 0.0,
                        0.0, 1.0, 0.0,
                        0.0, 0.0, 1.0,
                        1.0, 1.0, 1.0,
                        0.0, 0.0, 0.0)
        print ("List of colours: ", self.colours)
    
    def indexSetup(self):
        self.indices = (0, 1, 2,
                        1, 2, 3,
                        2, 3, 4)
        self.indices = np.array(self.indices, dtype=np.uint32)
        print ("Verts index: ", self.indices)
        
    def PackForShader(self):
        step_size = 3
        shuffle_start = 0
        shuffle_end = shuffle_start + step_size
        
        vert_num = len(self.verts)
        vert_whole = ()
        vert_group = ()
        
        list_complete = False
        while not list_complete:
            if shuffle_start != vert_num:
                vert_coords = (self.verts[shuffle_start:shuffle_end])
                col_values = (self.colours[shuffle_start:shuffle_end])
                vert_whole = (vert_coords + col_values)
                
                shuffle_start += step_size
                shuffle_end += step_size
                                
                vert_group = vert_group + vert_whole
                
            else:
                list_complete = True

        self.shaderPackage = vert_group
        self.shaderPackage = np.array(self.shaderPackage, dtype=np.float32)


class TriObj(object):
    """ Creates a gabe triangle object"""

    def __init__(self):
        """Constructor"""
        self.verts = None
        self.colours = None
        self.position = (0.0,0.0,0.0)
        self.indices = None
        self.shaderPackage = ()
        
        self.vertSetup()
        self.colSetup()
        self.indexSetup()
        self.PackForShader()
    
    def vertSetup(self):
        """ Create a set of vertices"""
        self.verts = (-0.5, -0.5, 0.0,
                      0.5, -0.5, 0.0,
                      0.0, 0.5, 0.0)
        #print (self.verts)
        
    def colSetup(self):
        """ Set vertex colours"""
        self.colours = (1.0, 0.0, 0.0,
                        0.0, 1.0, 0.0,
                        0.0, 0.0, 1.0)
        
    def indexSetup(self):
        self.indices = (0, 1, 2,
                        1, 2, 3)
        self.indices = np.array(self.indices, dtype=np.uint32)
        print (self.indices)
    
    def PackForShader(self):
        step_size = 3
        shuffle_start = 0
        shuffle_end = shuffle_start + step_size
        
        vert_num = len(self.verts)
        vert_whole = ()
        vert_group = ()
        
        list_complete = False
        while not list_complete:
            if shuffle_start != vert_num:
                vert_coords = (self.verts[shuffle_start:shuffle_end])
                col_values = (self.colours[shuffle_start:shuffle_end])
                vert_whole = (vert_coords + col_values)
                
                shuffle_start += step_size
                shuffle_end += step_size
                                
                vert_group = vert_group + vert_whole
                
            else:
                list_complete = True

        self.shaderPackage = vert_group
        self.shaderPackage = np.array(self.shaderPackage, dtype=np.float32)


if not glfw.init():
    raise Exception ("glfw not initialized")

gabe_window = glfw.create_window(surface[0], surface[1], "Triangle window - Programmable Pipeline", None, None)

if not gabe_window:
    glfw.terminate()
    raise Exception ("window was not created")

glfw.set_window_pos(gabe_window, 128, 128)
glfw.set_window_size_callback(gabe_window, window_resize)

glfw.make_context_current(gabe_window)

# Create a list of vertices and colours, this will be passed to the glBuffer
#gabeTri = TriObj()
gabeQuad = QuadObj()

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))


VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, gabeQuad.shaderPackage.nbytes, gabeQuad.shaderPackage, GL_STATIC_DRAW)

EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, gabeQuad.indices.nbytes, gabeQuad.indices, GL_STATIC_DRAW)


glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

glUseProgram(shader)
glClearColor(0.2, 0.2, 0.2, 1)



def main():
    while not glfw.window_should_close(gabe_window):
        glfw.poll_events()
        # Things to check while the program runs
        glClear(GL_COLOR_BUFFER_BIT)
        
        #glDrawArrays(GL_TRIANGLES, 0, 3)
        glDrawElements(GL_TRIANGLES, len(gabeQuad.indices), GL_UNSIGNED_INT, None)
        
        #
        glfw.swap_buffers(gabe_window)

main()
glfw.terminate()