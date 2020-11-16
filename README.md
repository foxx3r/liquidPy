# Refinement types and Dependent types in Python

This repository consists of my experiments on adding
refinement types and predicate types to python.

## Refining function call args

I make use of type hints added in Python 3.5 to
retrofit refinement types to python.

Define predicates as functions which return boolean values

```python
def N(i: int) -> bool:
  return i > 0
  
def CapitaliseName(s: str) -> bool:
  return len(s) > 0 and s[0].isupper()
```

Define a function with type hints pointing to the predicate functions

```python
def emp_greeting(dept: str, name: CapitaliseName, age: N) -> str:
  return f"{name} ({dept}), {age} yo"
  
emp_greeting("cs", "vikrant", -21) # This works, it shouldn't
```

The function works without validation of the types. Let's refine
it using the `refine` function

```python
@refine
def emp_greeting(dept: str, name: CapitaliseName, age: N) -> str:
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

## Issues

- Predicate functions should be without side effects in my opinion
- Refinement of variables

