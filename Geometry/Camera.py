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
        self.ksens = 1
        self.msens = 5
        # relative to player
        self.tfm = tfm or Tfm.zero()

        # TODO: should be None to start?
        self.mprev = (0,0)
        # self.mprev = None

    def krot(self,dh,dv):
        h = Rot(dh*self.ksens, Vec.e(1))
        v = Rot(dv*self.ksens, Vec.e(2))
        self.tfm.rotate(h,1)
        self.tfm.rotate(v,2)

    def mrot(self,dh,dv):
        h = Rot(dh*self.msens, Vec.e(1))
        v = Rot(dv*self.msens, Vec.e(2))
        self.tfm.setRotation(h,1)
        self.tfm.setRotation(v,2)

    def update(self,dt):
        dh,dv = 0,0

        # mouse input
        x,y = self.game.input.mpos
        dh = y - self.mprev[1]
        dv = x - self.mprev[0]
        self.mrot(-dh,dv)

        # # keyboard input
        # if self.game.input.isDown(b'g')   : dh =  1
        # elif self.game.input.isDown(b't') : dh = -1
        # if self.game.input.isDown(b'f')   : dv = -1
        # elif self.game.input.isDown(b'h') : dv =  1
        # self.krot(dh*dt,dv*dt)

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