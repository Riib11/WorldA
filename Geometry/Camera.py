from OpenGL.GLUT import *
from OpenGL.GL import *
from math import pi

import Geometry.Stack as Stack
import Utility.Constants as Consts

from Geometry.Basics import *

class Cam:
    def __init__(self,game,tfm=None):
        self.game = game
        self.active = True
        self.sensativity = 1
        # relative to player
        self.tfm = tfm or Tfm.zero()

    def rotstep(self,dh,dv):
        h = Rot(dh * self.sensativity, Vec.e(1))
        v = Rot(dv * self.sensativity, Vec.e(2))
        self.tfm.rotate(h,1)
        self.tfm.rotate(v,2)

    def update(self,dt):
        dh,dv = 0,0
        if self.game.input.isDown(b'g'): dh = 1
        elif self.game.input.isDown(b't'): dh = -1
        if self.game.input.isDown(b'f'): dv = -1
        elif self.game.input.isDown(b'h'): dv = 1
        self.rotstep(dh*dt,dv*dt)

    def startdraw(self):
        self.tfm.center()

        # # TEMP: a fix
        # update rotation via mouse
        # x,y = self.game.input.mpos
        # Stack.start()
        # Stack.push(); glRotatef( self.rot[0]*self.sensativity,0,1,0)
        # Stack.push(); glRotatef(-self.rot[1]*self.sensativity,1,0,0)

    def enddraw(self):
        self.tfm.uncenter()