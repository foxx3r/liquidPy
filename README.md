# Refinement Types & Dependent Types for Python

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

x = N(4) # type(x) == int not N
y = CapitalisedName('vikrant') # TypeError

# ----- Add type hints 
# Notice the use of function identifiers in type hints

@refine
def greet(dept: str, name: CapitalisedName, age: N) -> str:
  return f"{name} ({dept}), {age} yo"

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
# to
varname = annotation(expr)
```
by inspecting the function to be refined and modifying the AST.


```python
from refinement import refine, reftype

@reftype
def CapitalisedName(s: str) -> bool:
  return len(s) > 0 and s[0].isupper()

@refine
def fname() -> str:
    name : CapitalisedName = input()
    return name
```

## Dependent Types

Types can also depend on some input, 
These use the familiar syntax of returning functions

```python
from refinement import refine, reftype

@refine
def MinLenList(lim: N):
    @reftype
    def LenLimit(l: list) -> bool:
        return len(l) >= lim
    return LenLimit
    
SiblingsType = MinLenList(2)

@refine
def get_siblings() -> list:
    in = input("Enter names separated by space: ")
    sbls : SiblingsType = in.split()
    return sbls
    
```

## Issues

- Predicate functions should be without side effects (my opinion)
- SMT solving/ verification
- Refinement of global variables

