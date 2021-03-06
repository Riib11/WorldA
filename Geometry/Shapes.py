from OpenGL.GLUT import *
from OpenGL.GL import *

import Geometry.Stack as Stack

from Geometry.Basics import *
from Geometry.Colors import *

class Pln:
    def __init__(self,p,n):
        self.p = p
        self.n = n

#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Facet:
#   - collection of points, connected by edges
#   - DOESN'T have transform
#
class Facet:
    def __init__(self,ps,n):
        self.ps = ps
        self.n = n
    
    def get(self,i): return self.ps[i]
    __getitem__ = get
    
    def set(self,i,v): self.ps[i] = v
    __setitem__ = set
    
    def items(self): return iter(self.ps)
    __iter__ = items

    # abstract
    def gldraw(self): pass
    
    def lines(self):
        glBegin(GL_LINE_STRIP)
        for p in self: p()
        self[-1]();self[0]() # connect to beginning
        glEnd()
    
    def points(self):
        glBegin(GL_POINTS)
        for p in self: p()
        glEnd()
    
    def debug(self,ps,lw):
        self.tfm.debug(0.5,ps,lw)
        glclr('darkgrey')
        glLineWidth(lw)
        self.lines() # lines
        glclr('lightgrey')
        glPointSize(ps)
        self.points() # points

class Tri(Facet):
    def __init__(self,ps):
        (a,b,c) = ps
        super().__init__(ps,(b-a)^(c-a))
    def gldraw(self):
        for p in self: p()
    __call__ = gldraw

class Quad(Facet):
    def __init__(self,ps):
        (a,b,c,d) = ps
        super().__init__(ps,(b-a)^(d-a))
    def gldraw(self):
        self[0](); self[1](); self[3]()
        self[1](); self[2](); self[3]()
    __call__ = gldraw

#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Object:
#   - collection of facets
#   - has transform
#
class Obj:
    def __init__(self,ps,fs,tfm):
        self.ps = ps
        self.fs = fs
        self.tfm = tfm
    
    def get(self,i): return self.fs[i]
    __getitem__ = get
    
    def set(self,i,v): self.fs[i] = v
    __setitem__ = set
    
    def items(self): return iter(self.fs)
    __iter__ = items
    
    def gldraw(self):
        self.tfm.center()
        glBegin(GL_TRIANGLES)
        for f in self: f()
        glEnd()
        self.tfm.uncenter()
    __call__ = gldraw
    
    def points(self):
        self.tfm.center()
        glBegin(GL_POINTS)
        for p in self.ps: p()
        glEnd()
        self.tfm.uncenter()
    
    def debug(self,lw=1,ps=1):
        self.tfm.debug(1,lw,ps)       # transform
        for f in self: f.debug(lw,ps) # faces

class Cuboid(Obj):
    # format for points is: top quad, bottom quad (both clockwise)
    def __init__(self,ps,tfm=None):
        (a,b,c,d, e,f,g,h) = ps
        tfm = tfm or Tfm(Pnt.avg(ps),Vec.e1())
        super().__init__(ps,[ # faces oriented outward
            Quad([a,b,c,d]), # top
            Quad([b,a,e,f]), # front
            Quad([c,b,f,g]), # right
            Quad([d,c,g,h]), # back
            Quad([a,d,h,e]), # left
            Quad([h,g,f,e])  # bottom
        ],tfm)
    def lines(self):
        self.tfm.center()
        for f in self.fs: f.lines()
        self.tfm.uncenter()

class Cube(Cuboid):
    def __init__(self,tfm,s):
        p = tfm.p
        super().__init__([
            # top
            p + Vec([ s, s, s]),
            p + Vec([ s,-s, s]),
            p + Vec([-s,-s, s]),
            p + Vec([-s, s, s]),
            # bottom
            p + Vec([ s, s,-s]),
            p + Vec([ s,-s,-s]),
            p + Vec([-s,-s,-s]),
            p + Vec([-s, s,-s]),
        ],tfm)