import sys
from OpenGL.GLUT import *
from OpenGL.GL import *

# there is a default section
stack = [0]

# start a new stack section
def start():
    # print("-- new section",len(stack))
    stack.append(0)

def push():
    try:
        stack[-1] += 1
        glPushMatrix()
    except Exception as e:
        print(e)
        sys.exit(1)

def pop():
    try:
        if stack[-1] > 0:
            stack[-1] -= 1
            glPopMatrix()
        else: raise ValueError("An extra pop was called")
    except Exception as e:
        print(e)
        sys.exit(1)

# end stack section
def end():
    if len(stack) == 1: raise ValueError("Can't end default stack section")
    if stack[-1] != 0:
        # pop everything before ending section
        for i in range(stack[-1]): pop()
    del stack[-1]