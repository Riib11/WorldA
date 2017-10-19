from OpenGL.GLUT import *
from OpenGL.GL import *

color_names = {
    'white'     : (1,1,1),
    'black'     : (0,0,0),
    
    'grey'      : (0.5,0.5,0.5),
    'darkgrey'  : (0.25,0.25,0.25),
    'lightgrey' : (0.75,0.75,0.75),
    
    'red'       : (1,0,0),
    'darkred'   : (0.513, 0.027, 0.058),
    
    'green'     : (0,1,0),
    'darkgreen' : (0.125, 0.513, 0.027),
    
    'blue'      : (0,0,1),
    'darkblue'  : (0.039, 0.117, 0.698),
    'lightblue' : (0.188, 0.945, 0.952),
    
    'purple'    : (0.525, 0.176, 0.545),
    'pink'      : (0.929, 0.341, 0.956),
    'orange'    : (0.952, 0.494, 0.188),
}

curr_color = None

def glclr(name,a=1.0):
    global curr_color
    c = color_names[name]
    clr = glColor4f(c[0],c[1],c[2],a)
    curr_color = clr