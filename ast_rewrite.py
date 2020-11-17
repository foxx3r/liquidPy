import ast
import inspect
import types

def __rewrite_AnnAssign(node: ast.AnnAssign):
    print("Rewrote")
    ann = node.annotation
    val = node.value

    lineno = node.lineno
    end_lineno = node.end_lineno
    col_offset = node.col_offset
    end_col_offset = node.end_col_offset

    call = ast.Call(
            func=ann, args=[val], keywords=[],
            lineno=lineno, end_lineno=end_lineno,
            col_offset=col_offset, end_col_offset=end_col_offset,
        )
    node.value = call

def __recur_rewrite_body(body: list):
    for stmt in body:
        if type(stmt) != ast.AnnAssign:
            continue
        __rewrite_AnnAssign(stmt)

def get_refined_function(f: types.FunctionType):
    src = inspect.getsource(f)
    module = ast.parse(src)
    node = module.body[0]
    node.name = "refined_function"
    __recur_rewrite_body(node.body)
    cobj = compile(module, '<string>', 'exec')
    scope = dict()
    exec(cobj, f.__globals__, scope)
    return scope['refined_function']

