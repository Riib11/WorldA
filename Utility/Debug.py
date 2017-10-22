# decorator for debugging functions
class funcdebug:
    def __init__(self,f):
        self.f = f

    def __call__(self,*args):
        print("[Debug] call:",self.f.__name__,"on ",[*args])
        try: self.f(*args)
        except Exception as e: print("[Debug] error:",e)

@funcdebug
def hello(a,b,c):
    print("hello")

hello(12,3)