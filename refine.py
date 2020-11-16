import inspect
import types

def refine(f: callable):
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
                raise TypeError(f"{k} of value {v} does not satify refinement {P}")
        return f(*args, **kwargs)

    return f2
