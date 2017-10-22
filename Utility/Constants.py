import numpy as np

# for checking equality of floats
EPSILON = 1.0e-8
# genertic default decimal accuracy
ACCURACY = 5

def equal(a,b):
    try:
        return abs(a-b) < EPSILON
    except:
        if hasattr(a,'__iter__') and hasattr(b,'__iter__'):
            i = 0
            for x in a:
                if not equal(x,b[i]): return False
                i += 1
            return True
        else:
            return False



# can provide class to try and instanciate in after the 
def rounded(a):
    try: return round(a,ACCURACY)
    except:
        if hasattr(a,'__iter__'):
            res = []
            for x in a:
                res.append(rounded(x))
            return res