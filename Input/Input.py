from OpenGL.GLUT import *
from OpenGL.GL import *

class Input:

    def __init__(self,game,capts):
        self.game = game
        self.keyCaptures = capts
        self.keyStates = {
            b'\033' : 0 # default captured
        }
        for k in capts:
            self.keyStates[k] = 0

        self.mpos = (0,0) # mouse position
        self.mdpos = (0,0) # (last) mouse down position
        self.mbtn = None # mouse button currently down
        self.mdown = 0 # mouse is pressed
        self.mfocus = 0 # mouse in window or not

    def setupGlutInputFuncs(self):
        glutKeyboardFunc(self.keyboardDown)
        glutKeyboardUpFunc(self.keyboardUp)
        glutSpecialFunc(self.keyboardDown)
        glutSpecialUpFunc(self.keyboardUp)
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.mouseMotion)
        glutPassiveMotionFunc(self.mousePassiveMotion)
        glutEntryFunc(self.mouseEntry)

    # keyboard

    def keyboardDown(self,k,x,y):
        try: self.keyStates[k] = 1
        except: pass

    def keyboardUp(self,k,x,y):
        try: self.keyStates[k] = 0
        except: pass

    def isDown(self,k):
        try: return self.keyStates[k]
        except: print("key not registered:",k)

    def isUp(self,k): return not self.isDown(k)

    def areAnyDown(self,ks): return any([self.isDown(k) for k in ks])

    def areAnyUp(self,ks): return any([self.isUp(k) for k in ks])

    def areAllDown(self,ks): return not self.areAnyUp(ks)

    def areAllUp(self,ks): return not self.areAnyDown(ks)

    def esc(self): return self.isDown(b'\033')

    # mouse

    def mouseEntry(self,state):
        self.mfocus = state

    def mouse(self,mbtn,state,x,y):
        pos = self.toScreenPosition(x,y)
        
        if state == GLUT_DOWN:
            self.mbtn = mbtn
            self.mdpos = pos
            self.mdown = 1
        else:
            self.mbtn = None
            self.mdown = 0
            # don't update mdpos

    def mouseMotion(self,x,y):
        self.mpos = self.toScreenPosition(x,y)

    def mousePassiveMotion(self,x,y):
        self.mpos = self.toScreenPosition(x,y)

    def toScreenPosition(self,x,y):
        return (2.0 * (x - self.game.w/2) / min(self.game.w,self.game.h),
                2.0 * (self.game.h/2 - y) / min(self.game.w,self.game.h))