from refinement import *
from math import log10

@reftype
def N(i: int) -> bool:
    return i > 0

@refine
def LenLimInteger(bound: N) -> bool:
    @reftype
    def LenLim(i: int) -> bool:
        return len(str(i)) == bound
    return LenLim

AgeType = LenLimInteger(2)
AgeType(20)

@reftype
def EnglishName(s: str) -> bool:
    return s != '' and s[0].isupper()

@refine
def details() -> str:
    name : EnglishName = input("Name > ")
    AgeType = LenLimInteger(2)
    age : AgeType = int(input("Age > "))
    return f"{name} {age}"

