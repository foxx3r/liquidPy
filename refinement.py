import ast_rewrite
import inspect
import types
from functools import wraps

def __refine_signature(f: types.FunctionType):
    ''' Build a wrapped function for refining function parameters and return type '''
    assert type(f) == types.FunctionType, "Only functions can be refined"

    # Find all predicate functions in signature annotations
    tas = f.__annotations__
    predicates = {
        k: v for k, v in tas.items()
        if isinstance(v, types.FunctionType)
    } 

    def wrapped(*args, **kwargs):
        # Get dictionary of arguments
        callargs = inspect.getcallargs(f, *args, **kwargs)

        # Check predicate for each argument
        for k, v in callargs.items():
            if k not in predicates:
                continue
            predicates[k](v)

        # Run the refined function
        retval = f(*args, **kwargs)

        # Check predicate for return value
        if 'return' in predicates:
            predicates['return'](retval)
        return retval

    return wrapped

def reftype(f: types.FunctionType):
    assert type(f) == types.FunctionType, "Predicate should be a function"
    assert len(f.__annotations__) == 2, "Predicate should type hint the input parameter, the output should be bool" 
    assert f.__annotations__['return'] == bool, "Predicate should return a boolean value"

    # Refine the signature of the function
    wf = __refine_signature(f)

    # TODO: Verification of program in this function
    # Should be solved in an SMT solver

    # Add error throwing
    def wrf(v):
        if not wf(v):
            raise TypeError(f"Value {v} does not satify refinement {f.__name__}")
        return v

    return wrf

def refine(f: types.FunctionType):
    ''' Refines a function's body and signature '''
    assert type(f) == types.FunctionType, "Only functions can be refined"

    # Rewrite the function body's AST to call annotations 
    src = inspect.getsource(f)
    rf = ast_rewrite.get_refined_function(f, src)

    # Refine the signature of the function
    wrf = __refine_signature(rf)

    return wrf

