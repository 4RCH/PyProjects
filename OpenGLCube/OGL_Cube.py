import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


# Define a cube
cube_vert = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

# Define edges
cube_edge = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (5, 1),
    (5, 4),
    (5, 7),
    (6, 3),
    (6, 4),
    (6, 7)
)

cube_faces = (
    (0, 1, 2, 3),
    (4, 5, 7, 6),
    (0, 1, 5, 4),
    (2, 3, 6, 7),
    (0, 3, 6, 4),
    (1, 2, 7, 5)
)

colours = (
    (0,0,0),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,1,1)    
)

def glCube():
    glBegin(GL_QUADS)
    for surface in cube_faces:
        x = 0
        for vert in surface:
            glColor3fv((colours[x]))
            glVertex3fv(cube_vert[vert])
            x += 1
    glEnd()
    
    glBegin(GL_LINES)
    for edge in cube_edge:
        for vert in edge:
            glColor3fv((1,1,1))
            glVertex3fv(cube_vert[vert])
            
    glEnd()

def main():        
    
    pygame.init()
    display = (320, 240)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0, 0, -1)
    #glRotatef(0, 0, 0, 0)
    object_passed = False
    
    while object_passed == False:
        for event in pygame.event.get():
            if event.type == pygame.quit:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(1, 0, 0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(-1, 0, 0)
                if event.key == pygame.K_UP:
                    glTranslatef(0, -1, 0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0, 1, 0)
            #if event.type == pygame.MOUSEWHEEL:
                #if event.y > 0:
                    #glTranslatef(0, 0, 1)
                #if event.y < 0:
                    #glTranslatef(0, 0, -1)
        
        x = glGetDoublev(GL_MODELVIEW_MATRIX)
        #print (x)
        
        #camera_x = x[3][0]
        #camera_y = x[3][1]
        camera_z = x[3][2]
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)        
        glTranslatef(0, 0, -0.1)
        
        glCube()
        pygame.display.flip()
        pygame.time.wait(10)
        
        if camera_z <= 0:
            object_passed = True

main()
pygame.quit()
quit()