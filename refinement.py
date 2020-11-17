import inspect
import types
import ast_rewrite

def refine(f: types.FunctionType):
    ''' Refines a function's body and signature '''
    assert type(f) == types.FunctionType, "refine() can only accept functions"
    
    # Rewrite the function's AST to call annotations like functions
    rf_cobj = ast_rewrite.get_refined_func(f)
    exec(rf_cobj)
    rf_name = rf_cobj.co_names[0]
    rf = locals()[rf_name] 

    # Find all predicate functions in signature annotations
    tas = f.__annotations__
    predicates = {
        k: v for k, v in tas.items()
        if isinstance(v, types.FunctionType)
    } 

    # Build a wrapped function for replacement
    def wrapped(*args, **kwargs):
        # Get dictionary of arguments
        callargs = inspect.getcallargs(rf, *args, **kwargs)
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

