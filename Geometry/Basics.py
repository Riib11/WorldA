from OpenGL.GLUT import *
from OpenGL.GL import *
import Geometry.Stack as Stack
from Output.Colors import *
import math
import numpy as np

#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Vector:
#   - triple
#   - has algebra
#   - call to gltranslate
#
class Vec:
    def __init__(self,xs):
        self.xs = xs
        self.range = range(len(xs))

    def add(self,u): return Vec([self[i]+u[i] for i in self.range])
    __add__ = add
    
    def sub(self,u): return Vec([self[i]-u[i] for i in self.range])
    __sub__ = sub
    
    def dot(self,u): return sum([self[i]*u[i] for i in self.range])
    __mul__ = dot

    def cross(self,u,op=False):
        v = self
        return Vec([u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]])
    __xor__ = cross # v ^ u

    def scale(self,a): return Vec([a*x for x in self])
    __rmul__ = scale # a * v

    def mag2(self): return self * self
    
    def mag(self): return math.sqrt(self * self)

    def abs(self):
        l = self.mag()
        if l: return (1/l) * self
        return self # 0 length
    __abs__ = abs

    def neg(self): return Vec([-x for x in self])
    __neg__ = neg

    def trans(self,p):
        return Pnt([p[i] + self[i] for i in self.range])
    __radd__ = trans # p + v

    def cast(self,p): return Ray(p,self)
    __rrshift__ = cast # p >> v

    def get(self,i): return self.xs[i]
    __getitem__ = get

    def setitem(self,i,v): xs[i] = v
    __setitem__ = setitem

    def set(self,xs): self.xs = xs

    def items(self): return iter(self.xs)
    __iter__ = items

    # def tostring(self): return "Vec(" + str(np.around(self.xs,3)) + ")"
    def tostring(self): return "Vec(" + str(self.xs) + ")"
    __str__ = tostring
    __repr__ = tostring

    def gltranslate(self):
        Stack.push()
        glTranslatef(self[0],self[1],self[2])
    __call__ = gltranslate

    # from array
    def arr(coos):
        vecs = []
        cur = []
        for i in range(len(coos)):
            if len(cur) < 3: cur.append(coos[i])
            else: vecs.append(Vec(cur)); cur = [coos[i]]
        if len(cur) == 3: vecs.append(Vec(cur))
        return vecs

    # as point
    def pnt(self): return Pnt(self.xs)

    # debug draw (can extend from a point like a ray)
    def debug(self,lw=1,p=None,ps=1):
        glLineWidth(lw)
        p = p or Pnt.zero()
        glBegin(GL_LINES)
        p();(p + self)()
        glEnd()

    def zero(): return Vec([0,0,0])
    def one (): return Vec([1,1,1])
    def e1  (): return Vec([1,0,0])
    def e2  (): return Vec([0,1,0])
    def e3  (): return Vec([0,0,1])

#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Point:
#   - triple
#   - has algebra
#   - call to glvertex
#
class Pnt:
    def __init__(self,xs):
        self.xs = xs
        self.range = range(len(xs))

    def sub(self,q): return Vec([self[i] - q[i] for i in self.range])
    __sub__ = sub # p - q

    def neg(self): return Pnt([-x for x in self])
    __neg__ = neg

    def get(self,i): return self.xs[i]
    __getitem__ = get

    def setitem(self,i,v): xs[i] = v
    __setitem__ = setitem

    def set(self,xs): self.xs = xs

    def items(self): return iter(self.xs)
    __iter__ = items

    # def tostring(self): return "Pnt(" + str(np.around(self.xs,3)) + ")"
    def tostring(self): return "Pnt(" + str(self.xs) + ")"
    __str__ = tostring
    __repr__ = tostring

    def glvertex(self): glVertex3f(self[0],self[1],self[2])
    __call__ = glvertex

    # from array
    def arr(coos):
        pnts = []
        cur = []
        for i in range(len(coos)):
            if len(cur) < 3: cur.append(coos[i])
            else: pnts.append(Pnt(cur)); cur = [coos[i]]
        if len(cur) == 3: pnts.append(Pnt(cur))
        return pnts

    def vec(self): return Vec(self.xs)

    def debug(self,ps=1):
        glPointSize(ps)
        glBegin(GL_POINTS)
        self()
        glEnd()

    @classmethod
    def avg(cls,ps): return cls([np.average([p[0] for p in ps]),np.average([p[1] for p in ps]),np.average([p[2] for p in ps])])

    def zero(): return Pnt([0,0,0])

#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Ray:
#   - point and vector direction
#   - ray.q gets point at end of ray
#
class Ray:
    def __init__(self,p,v):
        self.p = p
        self.v = v
        self.q = p + v # target

    def scale(self,a): return p >> (a*v)
    __rmul__ = scale # a * r

    def tostring(self): return "Ray(" + str(self.p) + ";" + str(self.v) + ")"
    __str__ = tostring
    __repr__ = tostring

    # red --green-> green
    def debug(self,lw,ps):
        # line
        glclr('green')
        glLineWidth(lw)
        glBegin(GL_LINES);self.p();self.q();glEnd()
        # points
        glclr('red');self.p.debug(ps)
        glclr('green');self.q.debug(ps)

#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Transform:
#   - point with look and up directions
#   - can be either
#           - point tfm: only single point
#           - object tfm: has point origin, and attached collection of points
#
class Tfm:
    def __init__(self,ps,p=None,fwd=None,up=None):
        # location
        if isinstance(ps,list): # isn't a point transform
            self.point = False
            self.ps = ps            # points attached to transform
            self.p = p or ps[0]     # point location
            self.vs = [pi - self.p for pi in ps] # vectors to all points
        else:                   # is a point transform
            self.point = True
            self.p = ps             # single point location

        # orientation
        self.fwd = fwd or Vec.e1()  # look orientation
        self.up = up or Vec.e3()    # up orientation

    def update_points(self):
        # update all attached points
        if not self.point:
            for i in range(len(self.ps)):
                self.ps[i] = self.p + self.vs[i]
        # update rotation?

    # TODO
    def lookat(self): pass

    def setloc(self,x,y,z):
        self.p.set(x,y,z)
        self.update_points()

    def trans(self,v):
        self.p = self.p + v
        self.update_points()
        
    # TODO
    def rotate(self,rx,ry,rz): pass

    # TODO - center to transform
    def center(self):
        Stack.push()
        self.p.vec()() # translate to position
        # rotate
    __call__ = center

    def tostring(self): return "Tfm(" + str(self.p) + ";" + str(self.fwd) + ")"
    __str__ = tostring
    __repr__ = tostring

    def debug(self,size=1,ps=1,lw=1):
        # center point
        glclr('red');self.p.debug(ps)         # center
        glclr('red');(size*abs(self.fwd)).debug(lw,self.p,ps) # look
        glclr('blue');(size*abs(self.up)).debug(lw,self.p,ps)  # up
        if not self.point:                      # if attached to obj points
            glclr('lightgrey',0.5)
            self.vs[0].debug(lw,self.p,ps)
            # for v in self.vs: v.debug(lw,self.p,ps)
    
    def zero(): return Tfm(Pnt.zero())

axes_vecs = Vec.arr([4,0,0, 0,4,0, 0,0,4])
def drawaxes():
    glclr('red');axes_vecs[0].debug()
    glclr('green');axes_vecs[1].debug()
    glclr('blue');axes_vecs[2].debug()