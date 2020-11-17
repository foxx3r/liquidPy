import inspect
import types
import ast_rewrite

def refine(f: types.FunctionType):
    ''' Refines a function's body and signature '''
    assert type(f) == types.FunctionType, "refine() can only accept functions"

    # Find all predicate functions in signature annotations
    tas = f.__annotations__
    predicates = {
        k: v for k, v in tas.items()
        if isinstance(v, types.FunctionType)
    } 

    # Rewrite the function's AST to call annotations like functions
    rf = ast_rewrite.get_refined_function(f)
    print(rf)

    # Build a wrapped function for replacement
    def wrapped(*args, **kwargs):
        # Get dictionary of arguments
        callargs = inspect.getcallargs(f, *args, **kwargs)

        # Check predicate for each argument
        for k, v in callargs.items():
            if k not in predicates:
                continue
            P = predicates[k]
            if not P(v):
                raise TypeError(f"Argument {k} of value {v} does not satify refinement {P.__name__}")

        # Run the refined function
        retval = rf(*args, **kwargs)

        # Check predicate for return value
        if 'return' in predicates:
            P = predicates['return']
            if not P(retval):
                raise TypeError(f"Return value {retval} does not satify refinement {P.__name__}")
        return retval

    return wrapped

########
# TEST #
########

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
