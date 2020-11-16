import inspect
import types

def refine(f: callable):
    ''' Refines a function parameters '''
    tas = f.__annotations__
    predicates = {
        k: v for k, v in tas.items()
        if isinstance(v, types.FunctionType)
    } 

    def f2(*args, **kwargs):
        callargs = inspect.getcallargs(f, *args, **kwargs)
        for k, v in callargs.items():
            if k not in predicates:
                continue
            P = predicates[k]
            if not P(v):
                raise TypeError(f"Argument {k} of value {v} does not satify refinement {P.__name__}")
        return f(*args, **kwargs)

    return f2

def reftype(P: callable):
    ''' Defines a refinement type from a predicate '''
    def f2(v):
        if not P(v):
            raise TypeError(f"Value {v} does not satify refinement {P.__name__}")
        return v

    return f2

