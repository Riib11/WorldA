from OpenGL.GLUT import *
from OpenGL.GL import *
from math import pi

from Scenes.Scene import Scene

import Geometry.Stack as Stack
import Geometry.Stack as Stack
import Utility.Constants as Consts

from Geometry.Colors import *
from Geometry.Basics import *
from Geometry.Shapes import *

class RotatingCube(Scene):

    def __init__(self,game):
        super().__init__(game,"RotatingCube")

    def start(self):
        print(
            "---------------------------------------------------------\n" +
            "| starting level: Rotating Cube\n" +
            "---------------------------------------------------------\n" +
            "| * controls:\n"
            "|     - a/d/w/s/q/d  : move left/right/for/back/up/down\n" +
            "|     - mouse        : look\n" + 
            "|     - j/l/i/k      : rotate the cube\n" + 
            "---------------------------------------------------------\n"
        )

        self.unit = 1.0
        self.axes = [Vec.e1(),Vec.e2(),Vec.e3()]

        # cube
        self.cube = Cube(Tfm.zero(),self.unit)
        self.cube_drot = math.pi/2

        # floor
        self.floor = Cuboid(Pnt.arr([
            10,-10,10, 10,-10,-10, -10,-10,-10, -10,-10,10,
            10,-11,10, 10,-11,-10, -10,-11,-10, -10,-11,10
        ]),Tfm.zero())

    def update(self,dt):
        isDown = self.game.input.isDown

        # rotating cube

        # horizontal rotation
        if   isDown(b'j'): h = Rot( self.cube_drot*dt, Vec.e(3))
        elif isDown(b'l'): h = Rot(-self.cube_drot*dt, Vec.e(3))
        else: h = Rot.zero()
        
        # vertical rotation
        if   isDown(b'k'): v = Rot( self.cube_drot*dt, Vec.e(1))
        elif isDown(b'i'): v = Rot(-self.cube_drot*dt, Vec.e(1))
        else: v = Rot.zero()
        
        # apply rotations (need to be sequential)
        self.cube.tfm.rotate(h,1)
        self.cube.tfm.rotate(v,2)

    def display(self):
        Stack.start()

        # axes
        drawaxes()

        # floor
        glclr('green')
        self.floor()

        # cube
        glclr('white')
        self.cube()
        # glclr('black')
        # glLineWidth(10)
        # self.cube.lines()
        # glclr('orange')
        # glPointSize(20)
        # self.cube.points()

        Stack.end()