from OpenGL.GLUT import *
from OpenGL.GL import *
import math
import copy
import numpy as np

import Geometry.Stack as Stack
import Utility.Constants as Consts

from Geometry.Colors import *

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

    # static methods

    @staticmethod
    def zero(): return Vec([0,0,0])
    
    @staticmethod
    def one (): return Vec([1,1,1])
    
    @staticmethod
    def e1  (): return Vec([1,0,0])
    
    @staticmethod
    def e2  (): return Vec([0,1,0])
    
    @staticmethod
    def e3  (): return Vec([0,0,1])

    @staticmethod
    def e  (i): return Vec([(i-1)==j for j in range(3)])

    # class methods

    # from array
    @classmethod
    def arr(cls,coos):
        vecs = []
        cur = []
        for i in range(len(coos)):
            if len(cur) < 3: cur.append(coos[i])
            else: vecs.append(cls(cur)); cur = [coos[i]]
        if len(cur) == 3: vecs.append(cls(cur))
        return vecs

    # instance methods

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

    def abs2(self): return self * self
    
    def abs(self): return math.sqrt(self * self)
    __abs__ = abs

    def norm(self):
        l = abs(self)
        if Consts.equal(l,0): return self
        else: return (1/l) * self

    def neg(self): return Vec([-x for x in self])
    __neg__ = neg

    def trans(self,p):
        return Pnt([p[i] + self[i] for i in self.range])
    __radd__ = trans # p + v

    def cast(self,p): return Ray(p,self)
    __rrshift__ = cast # p >> v

    def copy(self): return Vec(self.xs[:])

    # the rotational difference between self (v) and u
    # returns Quaternion
    def rotdiff(self,u):
        vn = self.norm()
        un = u.norm()
        angle = math.acos(vn * un) # since abs's are 1
        axis = vn ^ un # orthoganol axis or rotation
        if angle == 0: return Quat.id()
        else:          return Quat.fromVecRot(axis,-angle)

    def get(self,i): return self.xs[i]
    __getitem__ = get

    def setitem(self,i,v): self.xs[i] = v
    __setitem__ = setitem

    def set(self,xs):
        if hasattr(xs,'xs'): self.xs = xs.xs
        else: self.xs = xs

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

    # as point
    def pnt(self): return Pnt(self.xs)

    # debug draw (can extend from a point like a ray)
    def debug(self,lw=1,p=None,ps=1):
        glLineWidth(lw)
        p = p or Pnt.zero()
        glBegin(GL_LINES)
        p();(p + self)()
        glEnd()

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

    # class methods

    # from array
    @classmethod
    def arr(cls,coos):
        pnts = []
        cur = []
        for i in range(len(coos)):
            if len(cur) < 3: cur.append(coos[i])
            else: pnts.append(cls(cur)); cur = [coos[i]]
        if len(cur) == 3: pnts.append(cls(cur))
        return pnts

    # static methods

    @staticmethod
    def zero(): return Pnt([0,0,0])

    # instance methods

    def sub(self,q): return Vec([self[i] - q[i] for i in self.range])
    __sub__ = sub # p - q

    def neg(self): return Pnt([-x for x in self])
    __neg__ = neg

    def copy(self): return Pnt(self.xs[:])

    def get(self,i): return self.xs[i]
    __getitem__ = get

    def setitem(self,i,v): self.xs[i] = v
    __setitem__ = setitem

    def set(self,xs):
        if hasattr(xs,'xs'): self.xs = xs.xs
        else: self.xs = xs

    def items(self): return iter(self.xs)
    __iter__ = items

    # def tostring(self): return "Pnt(" + str(np.around(self.xs,3)) + ")"
    def tostring(self): return "Pnt(" + str(self.xs) + ")"
    __str__ = tostring
    __repr__ = tostring

    def glvertex(self): glVertex3f(self[0],self[1],self[2])
    __call__ = glvertex

    def vec(self): return Vec(self.xs)

    def debug(self,ps=1):
        glPointSize(ps)
        glBegin(GL_POINTS)
        self()
        glEnd()

    @classmethod
    def avg(cls,ps): return cls([np.average([p[0] for p in ps]),np.average([p[1] for p in ps]),np.average([p[2] for p in ps])])

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

    # instance methods

    def scale(self,a): return p >> (a*v)
    __rmul__ = scale # a * r

    def copy(self): return Ray(self.p.copy(),self.v.copy())

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
# Rotation:
#   - represents rotation around an axis
#
class Rot:

    # takes angle and axis:vec
    def __init__(self,t,v):
        self.t = t
        self.v = v
        self.q = Quat.fromAngVec(t,v)

    # static methods

    @staticmethod
    def zero(): return Rot(0,Vec.e1())

    # class methods

    @classmethod
    def fromQuat(cls,q): return q.rot()

    # instance methods

    def add(self,rp): return (self.q * rp.q).rot()
    __add__ = add

    def apply(self,v=None):
        if v:
            qp = self.q * Quat.fromVec(v) * -self.q
            return qp.vec().norm()
        else:
            Stack.push()
            glRotatef(self.t*180/math.pi,self.v[0],self.v[1],self.v[2])
    __call__ = apply

    def neg(self): return Rot(-self.t,self.v)

    def neg(self): return (-self.q).rot()
    __neg__ = neg

    def tostring(self): return "Rot(" + str(self.t) + ":" + str(self.v) + ")"
    __str__ = tostring
    __repr__ = tostring

#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Quat:
#   - the quaternion you know and love
#   - has composition via `*`
#
class Quat:

    def __init__(self,r,i,j,k):
        self.r,self.i,self.j,self.k = r,i,j,k

    # static methods

    @staticmethod
    def zero(): return Quat(0,0,0,0)

    # class methods

    @classmethod
    # create from axis vector and rotation
    def fromAngVec(cls,t,v):
        costd2 = math.cos(t/2)
        sintd2 = math.sin(t/2)
        return cls(costd2, sintd2*v[0], sintd2*v[1], sintd2*v[2])

    @classmethod
    def fromVec(cls,v): return Quat(0,v[0],v[1],v[2])

    # instance methods

    # get as rotation
    def rot(self):
        m = math.sqrt(self.i**2 + self.j**2 + self.k**2)
        if m:
            t = 2 * math.atan2(m,self.r)
            v = Vec([self.i/m, self.j/m, self.k/m])
            return Rot(t,v)
        
        else: return Rot.zero()

    def vec(self): return Vec([self.i,self.j,self.k])

    # hamiltonian product
    def mul(self,w): return Quat(
            self.r*w.r - self.i*w.i - self.j*w.j - self.k*w.k,
            self.r*w.i + self.i*w.r + self.j*w.k - self.k*w.j,
            self.r*w.j - self.i*w.k + self.j*w.r + self.k*w.i,
            self.r*w.k + self.i*w.j - self.j*w.i + self.k*w.r
        )
    __mul__ = mul

    def abs(self,x=None): return math.sqrt(self.r**2 + self.i**2 + self.j**2 + self.k**2)
    __abs__ = abs

    def inverse(self):
        den = abs(self)
        return Quat(self.r/den,-self.i/den,-self.j/den,-self.k/den)
    __neg__ = inverse

    # TODO: need this?
    def norm(self):
        den = abs(self)
        return Quat(self.r/den, self.i/den, self.j/den, self.k/den)

    # TODO:
    def pow(self,n): pass

    def tostring(self): return "Quat(" + str([self.r,self.i,self.j,self.k]) + ")"
    __str__ = tostring
    __repr__ = tostring

#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Transform:
#   - point with forward and up directions
#   - can be either
#           - point tfm: only single point
#           - object/facet tfm: has point origin, and attached collection of points
#
class Tfm:
    def __init__(self,p=None,rot=None):
        self.p = p or Pnt.zero()
        self.rot = rot or Rot.zero()
        # four extra rotations if needed
        self.srots = [None,None,None]

    # static methods

    @staticmethod
    def zero(): return Tfm()

    # class methods

    # instance methods

    def center(self):
        Stack.start()
        # center position
        self.p.vec()()
        # rotation
        self.rot()
        # sequential rotations
        for r in self.srots:
            if r: r()

    def uncenter(self): Stack.end()

    def orient(self,v,excluded=[]):
        w = (-self.rot)(v)
        for i in range(len(self.srots)):
            r = self.srots[i]
            if r and not (i in excluded):
                w = (-r)(w)
        return w

    def translate(self,v): self.p = self.p + v

    def setPosition(self,p): self.p = p

    # index if for a sequential rotation
    def rotate(self,rot,i=0):
        # for main rotation
        if not i: self.rot = self.rot + rot
        # for sequenctial rotation
        else:
            # not initialized yet
            if not self.srots[i]: self.srots[i] = rot
            # is initialized
            else: self.srots[i] = self.srots[i] + rot

    def setRotation(self,rot,i=0):
        if not i: self.rot = rot
        else: self.srots[i] = rot

    def debug(self,size=1,ps=1,lw=1):
        p0 = Pnt.zero()
        self.center()
        glclr('white'); p0.debug(ps)                # point
        glclr('red')  ; Vec.e1().debug(lw,p0,ps)    # axis 1
        glclr('green'); Vec.e2().debug(lw,p0,ps)    # axis 2
        glclr('blue') ; Vec.e3().debug(lw,p0,ps)    # axis 3
    
# debug axes
axes_vecs = Vec.arr([4,0,0, 0,4,0, 0,0,4])
def drawaxes():
    glclr('red');axes_vecs[0].debug()
    glclr('green');axes_vecs[1].debug()
    glclr('blue');axes_vecs[2].debug()