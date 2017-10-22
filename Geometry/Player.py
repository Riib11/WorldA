from OpenGL.GLUT import *
from OpenGL.GL import *
from math import pi

from Geometry.Basics import *
import Geometry.Stack as Stack

class Player:
    def __init__(self,game,tfm=None):
        self.game = game
        self.tfm = tfm or Tfm.zero()

        self.mv_fwd = Vec([0,0,1])
        self.mv_rgt = Vec([1,0,0])
        self.mv_up = Vec([0,1,0])
        self.speed = 5.0

    def reorient(self):
        pass # this doesn't work
        self.mv_fwd = self.game.cam.tfm.orientVec(self.mv_fwd)
        self.mv_rgt = self.game.cam.tfm.orientVec(self.mv_rgt)
        self.mv_up = self.game.cam.tfm.orientVec(self.mv_up)

    def update(self,dt):
        isDown = self.game.input.isDown

        # want to move relative to camera look
        # self.reorient()

        # moving
        rgt,fwd,up = 0,0,0

        # left/right
        if isDown(b'a')  : rgt = 1
        elif isDown(b'd'): rgt = -1
        # for/back
        if isDown(b's')  : fwd = -1
        elif isDown(b'w'): fwd = 1
        # up/down
        if isDown(b'q')  : up = -1
        if isDown(b'e')  : up = 1

        self.tfm.translate( self.speed * dt * (rgt*self.mv_rgt + fwd*self.mv_fwd + up*self.mv_up) )

    def startdraw(self):
        self.tfm.center()

    def enddraw(self):
        self.tfm.uncenter()