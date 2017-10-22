from Geometry.Basics import *
import Utility.Constants as Consts

v = Vec([0,1,0])
w = Vec([1,0,0])
t = Tfm.zero()
q = Quat.fromVecRot(Vec.e2(),10,True)

while True:
    print(Consts.rounded(t.up),end='')
    q(t)
    input("")
