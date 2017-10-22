import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from time import time
from Output.Colors import *

from Input.Input import Input
from Geometry.Camera import Cam
from Geometry.Player import Player

class Game:

    def __init__(self,args):
        # params
        self.name = args['name']
        self.w = args['width']
        self.h = args['height']
        self.dt = args['dt']
        self.fullscreen = args['fullscreen']

        # input
        self.input = Input(self,args['keycaps'])

        # cam
        self.cam = Cam(self)

        # player
        self.player = Player(self)

        # time
        self.active = True
        self.t = time()

        # scenes
        self.scenes = []
        self.scene_names = []
        self.current = None

    # sets scene and calls `scene.start()`
    # can pass scene name or serial id
    def setScene(self,id):
        if isinstance(id,int):
            self.current = self.scenes[id]
            self.current.start()
        if isinstance(id,str):
            self.current = self.scenes[self.scene_names.index(id)]
            self.current.start()
        else: print("[!] invalid scene id")

    def update(self,x):
        # main controls
        if self.input.esc(): self.quit()
        if self.input.isDown(b'1'): self.setFullscreen(0)
        if self.input.isDown(b'2'): self.setFullscreen(1)

        nt = time()
        dt = nt - self.t
        self.current.update(dt) # scene
        self.cam.update(dt)  # camera
        self.player.update(dt)  # player
        glutPostRedisplay()
        
        if self.active:
            self.t = nt
            glutTimerFunc(self.dt,self.update,0)
        
        else: sys.exit(1)

    def main(self):
        # init rendering
        glutInit([])
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.w, self.h)
        glutCreateWindow(self.name)
        glEnable(GL_DEPTH_TEST)
        # glEnable(GL_BLEND) # idk how to use this

        # register callbacks
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        self.input.setupGlutInputFuncs()

        # fullscreen
        if self.fullscreen: glutFullScreen()

        # game loop
        print("starting game loop")
        glutTimerFunc(self.dt,self.update,0)

        # glut loop
        glutMainLoop()

        return 0

    def setFullscreen(self,fs):
        if fs and not self.fullscreen:
            glutFullScreen()
            self.fullscreen = True
        elif not fs and self.fullscreen:
            glutReshapeWindow(self.w, self.h)
            glutPositionWindow(0,0)
            self.fullscreen = False

    def quit(self):
        self.active = False

    def display(self):
        # init
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # camera start draw
        self.cam.startdraw()
        # player start draw
        self.player.startdraw()
        
        # scene
        self.current.display()

        # player end draw
        self.player.enddraw()
        # camera end draw
        self.cam.enddraw()
        
        # render
        glFlush()

    def reshape(self, w,h):
        glViewport(0, 0, w, h)
        self.w, self.h = w, h
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        # perspective
        near = 1
        far = 50
        if w > h: glFrustum(-w/h, w/h, -1, 1, near, far)
        else: glFrustum(-1, 1, -h/w, h/w, near, far)
        
        # orthographic
        # if w > h: glOrtho(-w/h*2.0, w/h*2.0, -2.0, 2.0, -2.0, 2.0)
        # else: glOrtho(-2.0, 2.0, -h/w * 2.0, h/w * 2.0, -2.0, 2.0)