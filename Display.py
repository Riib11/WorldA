import sys
from random import random
import math
from math import pi
import operator
import numpy as np

from OpenGL.GLUT import *
from OpenGL.GL import *

NAME = "Test Display"

W, H = 500, 500

R1 = 0
R2 = 0
S = 1

def display():
    # init
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # transformations
    glPushMatrix(); glRotatef(R2*180.0/pi,1,0,0)
    glPushMatrix(); glRotatef(R1*180.0/pi,0,1,0)
    # glPushMatrix(); glScale3f(S,S,S)

    # draw   
    glBegin(GL_TRIANGLES) 
    glVertex3f(-1,-1, 0)
    glVertex3f( 1,-1, 0)
    glVertex3f( 0, 1, 0)
    glEnd()

    # pop
    glPopMatrix()
    glPopMatrix()
    # glPopMatrix()
    
    # Render the scene.
    glFlush()

def keyboard(key, x, y):
    # Handle ESC key.
    if key == b'\033':  
    # "\033" is the Escape key
        sys.exit(1)

def special(key, x, y): pass

def initRendering():
    """ Initialize aspects of the GL scene rendering.  """
    glEnable (GL_DEPTH_TEST)


def reshape(w, h):
    """ Register a window resize by changing the viewport.  """
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if w > h:
        glOrtho(-w/h*2.0, w/h*2.0, -2.0, 2.0, -2.0, 2.0)
    else:
        glOrtho(-2.0, 2.0, -h/w * 2.0, h/w * 2.0, -2.0, 2.0)

def main(argc, argv):

    """ The main procedure, sets up GL and GLUT. """

    glutInit(argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)

    glutInitWindowPosition(
        int(glutGet(GLUT_SCREEN_WIDTH)/2 - W/2),
        int(glutGet(GLUT_SCREEN_HEIGHT)/2 - H/2)
    )
    glutInitWindowSize(W, H)
    glutCreateWindow(NAME)
    initRendering()

    # Register interaction callbacks.
    
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special)
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)

    glutMainLoop()

    return 0