from refinement import *

def N(i: int) -> bool:
    return i > 0

def testf(a: N):
    x : int = 2.4
    y : N = -10
    print("X is ", x)
    print("Y is ", y)
    return a % x == 0

r = refine(testf)

r(10)
r(-10)
