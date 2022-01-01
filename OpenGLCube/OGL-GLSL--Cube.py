import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr

vertex_src = """
# version 330 core

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_color;

uniform mat4 rotation;

out vec3 v_color;

void main()
{
    gl_Position = rotation * vec4(a_position, 1.0);
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
    
class CubeObj(object):
    """ Creates a gabe triangle object"""

    def __init__(self):
        """Constructor"""
        self.cube_verts = None
        self.colours = None
        self.position = (0.0,0.0,0.0)
        self.indices = None
        self.shaderPackage = ()
        
        self.cubeSetup(1)
        self.colSetup()
        self.indexSetup()
        self.PackForShader()
    
    def cubeSetup(self, size = 1):
        origin = (0.0,0.0,0.0)        
        vertsList = (origin[0], origin[1], origin[2],
                     (origin[0] + size), origin[1], origin[2],
                     (origin[0] + size), (origin[1] + size), origin[2],
                     origin[0], (origin[1] + size), origin[2],
                     origin[0], origin[1], (origin[2] + size),
                     (origin[0] + size), origin[1], (origin[2] + size),
                     (origin[0] + size), (origin[1] + size), (origin[2] + size),
                     origin[0], (origin[1] + size), (origin[2] + size))
        
        self.cube_verts = self.centerCube(size, vertsList)
        print("Cube coordinates: ", self.cube_verts)
    
    def centerCube(self, size, vertsList, center = (0,0,0)):
        offset = size / 2
        coords_offset = ()
        for coord in vertsList:
            coord_newpos = float(coord - offset)
            coords_offset += (coord_newpos,)                                          
        return coords_offset
        
    def colSetup(self):
        """ Set vertex colours"""
        self.colours = (1.0, 0.0, 0.0,
                        0.0, 1.0, 0.0,
                        0.0, 0.0, 1.0,
                        1.0, 1.0, 1.0,
                        1.0, 0.0, 0.0,
                        0.0, 1.0, 0.0,
                        0.0, 0.0, 1.0,
                        0.0, 0.0, 0.0
                        )
        print ("List of colours: ", self.colours)
    
    def indexSetup(self):
        self.indices = (0, 1, 2, 0, 2, 3,
                        4, 5, 6, 4, 6, 7,
                        0, 1, 5, 0, 4, 5,
                        2, 3, 7, 2, 7, 6,
                        3, 4, 0, 3, 4, 7,
                        1, 2, 5, 5, 6, 2
                        )
        self.indices = np.array(self.indices, dtype=np.uint32)
        print ("Verts index: ", self.indices)
        
    def PackForShader(self):
        step_size = 3
        shuffle_start = 0
        shuffle_end = shuffle_start + step_size
        
        vert_num = len(self.cube_verts)
        vert_whole = ()
        vert_group = ()
        
        list_complete = False
        while not list_complete:
            if shuffle_start != vert_num:
                vert_coords = (self.cube_verts[shuffle_start:shuffle_end])
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

gabe_window = glfw.create_window(surface[0], surface[1], "Cube window", None, None)

if not gabe_window:
    glfw.terminate()
    raise Exception ("window was not created")

glfw.set_window_pos(gabe_window, 128, 128)
glfw.set_window_size_callback(gabe_window, window_resize)

glfw.make_context_current(gabe_window)

gabeQuad = CubeObj()

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
glEnable(GL_DEPTH_TEST)
rotation_location = glGetUniformLocation(shader, "rotation")

def main():
    while not glfw.window_should_close(gabe_window):
        glfw.poll_events()
        # Things to check while the program runs
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
        
        glUniformMatrix4fv(rotation_location, 1, GL_FALSE, pyrr.matrix44.multiply(rot_x, rot_y))
        
        glDrawElements(GL_TRIANGLES, len(gabeQuad.indices), GL_UNSIGNED_INT, None)
        
        #
        glfw.swap_buffers(gabe_window)

main()
glfw.terminate()