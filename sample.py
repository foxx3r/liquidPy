from refinement import *
from math import log10

@reftype
def N(i: int) -> bool:
    return i > 0

def LenLimInteger(bound: N) -> bool:
    @reftype
    def LenLim(i: int) -> bool:
        return int(log10(i)) == N
    return LenLim
LenLimInteger = refine(LenLimInteger)

@reftype
def EnglishName(s: str) -> bool:
    return s != '' and s[0].isupper()

def input_details() -> str:
    name : EnglishName = input("Name > ")
    AgeType = LenLimInteger(2)
    age : AgeType = int(input("Age > "))
    return f"{name} {age}"
input_details = refine(input_details)

