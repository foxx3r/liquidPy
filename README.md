# Powerful Type Systems for Python

PEP 3107: "this PEP makes no attempt to introduce any kind of standard semantics,
even for the built-in types. This work will be left to third-party libraries."

I make use of the open interpretation of annotations to
develop refinement types and dependent types for Python.

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

by rewriting the function using metaprogramming.


```python
from refinement import refine

def CapitalisedName(s: str) -> bool:
  return len(s) > 0 and s[0].isupper()

@refine
def greeting() -> CapitalisedName:
    name : CapitalisedName = "vikrant"
    return name
```

## Issues

- Predicate functions should be without side effects (my opinion)
- Currently thinking of how to implement dependent types

