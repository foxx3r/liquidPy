# Powerful Type Systems for Python

PEP 3107: "this PEP makes no attempt to introduce any kind of standard semantics,
even for the built-in types. This work will be left to third-party libraries."

I make use of the open interpretation of annotations to
develop refinement types and dependent types to Python.

## Refinement of function parameters 

```python

from refinement import refine

# ----- Define predicates 

def N(i: int) -> bool:
  return i > 0
  
def CapitalisedName(s: str) -> bool:
  return len(s) > 0 and s[0].isupper()

# ----- Add type hints and refinement decorator
# Notice the use of function identifiers in type hints

@refine
def emp_greeting(dept: str, name: CapitalisedName, age: N) -> str:
  return f"{name} ({dept}), {age} yo"
  
# or just use the decorator as a function
refined_emp_greeting = refine(emp_greeting)

# ----- Call it like any other function

emp_greeting("cs", "vikrant", -21) # TypeError on 2nd argument
emp_greeting("cs", "Vikrant", -21) # TypeError on 3rd argument
emp_greeting("cs", "Vikrant", 21)  # This works
```

## Refining local and global variables

Unfortunately, PEP 526 says 

"Store variable annotations also in function scope: 
The value of having the annotations available locally is just
 not enough to significantly offset the cost of creating and
 populating the dictionary on each function call."

Instead, I temperorily came up with a simple decorator
which allows you to define your predicate and then convert it into
a function which either returns your value or throws a TypeError.

Currently I'm working to unify this with the above syntax of 
refinement types in function parameters.

```python
from refinement import reftype

@reftype
def CapitalisedName(s: str) -> bool:
  return len(s) > 0 and s[0].isupper()

# or

CapitalisedNameType = reftype(CapitalisedName)

name = CapitalisedNameType("vikrant") # TypeError
name = CapitalisedNameType("Vikrant") # This works
```

I would still really prefer something like
```python
name : CapitalisedNameType = "vikrant"
```
Though type annotations for locals are not saved.


*Alternative:* Developing a type checker/ translator to convert
```
varname : annotation_type = expr
# to
varname = annotation_type(expr)
```
For all function type annotations

## Issues

- Predicate functions should be without side effects (my opinion)
- Try to refine variables using type hints, not function calls (translator)
- Currently thinking of how to implement dependent types

