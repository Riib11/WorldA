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
        self.speed = 2.0

    def update(self,dt):
        ipt = self.game.input

        # move

        # left
        if ipt.isDown(b'a'): self.tfm.trans(
            self.speed * dt * self.mv_rgt)
        # right
        elif ipt.isDown(b'd'): self.tfm.trans(
            -self.speed * dt * self.mv_rgt)
        # forward
        if ipt.isDown(b's'): self.tfm.trans(
            -self.speed * dt * self.mv_fwd)
        # backward
        elif ipt.isDown(b'w'): self.tfm.trans(
            self.speed * dt * self.mv_fwd)
        # up
        if ipt.isDown(b'q'): self.tfm.trans(
            -self.speed * dt * self.mv_up)
        # down
        if ipt.isDown(b'e'): self.tfm.trans(
            self.speed * dt * self.mv_up)

    def startdraw(self):
        Stack.start()
        self.tfm() # center self

    def enddraw(self):
        Stack.end()