from OpenGL.GLUT import *
from OpenGL.GL import *
from math import pi

from Geometry.Basics import *
import Geometry.Stack as Stack

class Cam:
    def __init__(self,game,tfm=None):
        self.game = game
        
        # relative to player
        self.tfm = tfm or Tfm.zero()
        
        self.rot = [0,0]
        self.drot = [10000,10000,10000]

    def startdraw(self):
        # update rotation via mouse
        if self.game.input.mfocus:
            self.rot = self.game.input.mpos

        # camera transormation
        Stack.start()
        # translate to cam pos
        Stack.push(); (-1 * self.tfm.p.vec())()
        # rotate y axis
        Stack.push(); glRotatef( self.rot[0] * self.drot[0] / 180*pi ,0,1,0)
        # rotate x axis
        Stack.push(); glRotatef(-self.rot[1] * self.drot[1] / 180*pi ,1,0,0)

    def enddraw(self):
        Stack.end() # end cam trans section