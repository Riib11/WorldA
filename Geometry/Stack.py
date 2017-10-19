from OpenGL.GLUT import *
from OpenGL.GL import *

# there is a default section
stack = [0]

# start a new stack section
def start():
    # print("-- new section",len(stack))
    stack.append(0)

def push():
    stack[-1] += 1
    glPushMatrix()
    # print("push",stack[-1]-1,"->",stack[-1])

def pop():
    if stack[-1] > 0:
        stack[-1] -= 1
        glPopMatrix()
        # print("pop",stack[-1]+1,"->",stack[-1])
    else: raise ValueError("An extra pop was called")

# end stack section
def end():
    if len(stack) == 1: raise ValueError("Can't end default stack section")
    if stack[-1] != 0:
        # pop everything before ending section
        for i in range(stack[-1]): pop()
    del stack[-1]
    # print("-- end section",len(stack)+1)