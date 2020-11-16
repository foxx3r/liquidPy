# Refinement types and Dependent types in Python

This repository consists of my experiments on adding
refinement types and predicate types to python.

## Refining function parameters

I make use of type hints added in Python 3.5 to
retrofit refinement types to python.

Define predicates as functions which return boolean values

```python
def N(i: int) -> bool:
  return i > 0
  
def CapitalisedName(s: str) -> bool:
  return len(s) > 0 and s[0].isupper()
```

Define a function with type hints pointing to the predicate functions

```python
def emp_greeting(dept: str, name: CapitalisedName, age: N) -> str:
  return f"{name} ({dept}), {age} yo"
  
emp_greeting("cs", "vikrant", -21) # This works, it shouldn't
```

The function works without validation of the types. Let's refine
it using the `refine` function

```python
@refine
def emp_greeting(dept: str, name: CapitalisedName, age: N) -> str:
  return f"{name} ({dept}), {age} yo"
  
# or

refined_emp_greeting = refine(emp_greeting)
```

Now this ain't gonna work unless all the predicates are satisfied.

```python
emp_greeting("cs", "vikrant", -21) # TypeError on 2nd argument
emp_greeting("cs", "Vikrant", -21) # TypeError on 3rd argument
```

Notice how we ignore built-in callables like `str`.

Let's pass satisfactory arguments to the function.

```python
emp_greeting("cs", "Vikrant", 21) # This works
```

## Refining local and global variables

Unfortunately, PEP 526 says that its too costly to store all local
type annotations in a dictionary. Instead, I came up with a simple decorator
which allows you to define your predicate and then convert it into
a function which either returns your value or throws a TypeError.

```python
@reftype
def CapitalisedName(s: str) -> bool:
  return len(s) > 0 and s[0].isupper()

# or

CapitalisedNameType = reftype(CapitalisedName)

```

This would allow you to run the validation like so:

```python
name = CapitalisedNameType("vikrant") # TypeError
```

I would still really prefer something like
```python
name : CapitalisedNameType = "vikrant"
```
Though I can't seem to find the inspection API for locals.

"Store variable annotations also in function scope: 
The value of having the annotations available locally is just
 not enough to significantly offset the cost of creating and
 populating the dictionary on each function call."
- PEP 526

Alternative: Developing a type checker/ translator to convert
```
varname : annotation_type = expr
# to
varname = annotation_type(expr)
```
For all function type annotations


## Issues

- Predicate functions should be without side effects in my opinion
- Try to refine variables using type hints, not function calls
- An easy syntax for dependent types

