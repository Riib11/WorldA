from OpenGL.GLUT import *
from OpenGL.GL import *
from Scene import Scene
from math import pi

from Geometry.Basics import *
from Geometry.Shapes import *
import Geometry.Stack as Stack
from Output.Colors import *

class TestScene(Scene):

    def __init__(self,game):
        super().__init__(game,"TestScene")

        self.unit = 0.5

        self.cube = Cube(Tfm(
            Pnt([2,2,0]),
            Vec.e1(),
            Vec.e3()
        ),self.unit)

        tile_range = 2
        rng = range(-tile_range,tile_range+1)
        self.tiles = [
            Cube(Tfm(
                Pnt([x*2*self.unit,-4*self.unit,z*2*self.unit]),
                Vec.e1(),Vec.e3()
            ),self.unit)
            for x in rng for z in rng
        ]

        self.tiles_colors = ['lightgrey','darkgrey'] * (len(self.tiles)//2 + 1)

    def update(self,dt):
        pass

    def display(self):
        Stack.start()

        # axes
        drawaxes()

        # tiles
        for i in range(len(self.tiles)):
            glclr('blue')
            self.tiles[i]()
            glclr('white')
            glLineWidth(10)
            self.tiles[i].lines()

        # mouse down
        if self.game.input.mdown:
            self.cube.debug(20,10)
        
        # mouse up
        else:
            glclr('white')
            self.cube()
            glclr('black')
            self.cube.lines()

        Stack.end()