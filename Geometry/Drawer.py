# import sys
# from OpenGL.GLUT import *
# from OpenGL.GL import *

# from Utility.Debug import *

class Drawer:

    def __init__(self,game):
        self.game = game
        self.pointer = [0]
        self.stack = []

    def poshelper(self,pt,stk):
        if len(pt) == 1: return stk
        else: return self.poshelper(pt[1:],stk[pt[0]])

    # position in stack
    def pos(self): return self.poshelper(self.pointer,self.stack)

    # value at stack pointer
    def val(self): return self.pos()[self.pointer[-1]]

    # start a transformation section
    # @hardcatch
    def start(self): pass

    # end the inner-most transformation section
    # @hardcatch
    def end(self): pass

    # push a transformation matrix
    # @hardcatch
    def push(self): pass

    # pop a transformation matrix
    # @hardcatch
    def pop(self): pass

    # drawing

    def vertecies(self,vs) : pass
    def lines    (self,vs) : pass
    def triangles(self,vs) : pass
    def color    (self,v)  : pass


d = Drawer(None)
d.stack = [
    0,
    [
        [
            1,2,
            [
                [3,4,5]
            ]
        ],
        [
            6,7
        ]
    ],
    8,
    [
        [
            9,10,
            [
                11,12
            ],
            [
                13,14
            ],
            [
                15,16
            ]
        ],
        [
            17,18
        ],
        [
            19,20,21,
            [
                [
                    22,23,23
                ],
                [
                    25,26,27
                ],
                [
                    28,29,30
                ]
            ]
        ]
    ]
]

d.pointer = [1,0,2,0,0]
print(d.val())