import sys

# decorator for debugging functions
class debug:
    def __init__(self,f):
        self.f = f

    def __call__(self,*args):
        print("[Debug] call:",self.f.__name__,"on ",[*args])
        try: self.f(*args)
        except Exception as e: print("[Debug] error:",e)

class hardcatch:
    def __init__(self,f): self.f = f
    def __call__(self,*args):
        try: self.f(*args)
        except Exception as e:
            print("[DebugHard] error:",e)
            sys.exit(1)

# # example
# @funcdebug
# def hello(a,b,c):
#     print("hello")
# hello(12,3)