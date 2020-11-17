# Powerful Type Systems for Python

PEP 3107: "this PEP makes no attempt to introduce any kind of standard semantics,
even for the built-in types. This work will be left to third-party libraries."

I make use of the open interpretation of annotations to
develop refinement types and dependent types for Python.
All refinement happens in runtime without any static
type checking with the help of metaprogramming.

## Refinement of function parameters 

```python
from refinement import refine, reftype

# ----- Define predicates 

@reftype
def N(i: int) -> bool:
  return i > 0
  
@reftype
def CapitalisedName(s: str) -> bool:
  return len(s) > 0 and s[0].isupper()

# These can be used like normal type conversions
x = N(4)

# ----- Add type hints 

# Notice the use of function identifiers in type hints
def greet(dept: str, name: CapitalisedName, age: N) -> str:
  return f"{name} ({dept}), {age} yo"

# ----- Add refinement
greet = refine(greet)

# ----- Call it like any other function

greet("cs", "vikrant", -21) # TypeError on 2nd argument
greet("cs", "Vikrant", -21) # TypeError on 3rd argument
greet("cs", "Vikrant", 21)  # This works
```

## Refining local variables

[WIP]

Unfortunately, PEP 526 says 

"Store variable annotations also in function scope: 
The value of having the annotations available locally is just
 not enough to significantly offset the cost of creating and
 populating the dictionary on each function call."

So, I rewrite all
```
varname : annotation = expr
```

to

```
varname = annotation(expr)
```

by inspecting the function to be refined and modifying the AST.


```python
from refinement import refine, reftype

@reftype
def CapitalisedName(s: str) -> bool:
  return len(s) > 0 and s[0].isupper()

def fname() -> CapitalisedName:
    name : CapitalisedName = input()
    return name
```

Types can also depend on some input, 
These use the familiar syntax of returning functions

```python
from refinement import refine, reftype
from math import log10

def LenLimInteger(lim: N):
    @reftype
    def LenLimit(i: N) -> bool:
        return int(log10(i)) == lim
    return LenLimit

# For good measures, add refinement to this function as well
LenLimInteger = refine(LenLimInteger)

# Let's make a type for integers of length 2
AgeType = LenLimInteger(2)

# And we can use this as
def get_age() -> N:
    age: AgeType = int(input("Your age = "))
    return age

```

## Issues

- Predicate functions should be without side effects (my opinion)
- @refine decorator isn't working (OS error, can't find source code)
- Refinement of global variables
- Currently thinking of how to implement dependent types

