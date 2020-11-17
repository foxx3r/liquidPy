import ast, inspect

def __rewrite_AnnAssign(node: ast.AnnAssign):
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

def get_refined_func(f: callable):
    src = inspect.getsource(f)
    mod = ast.parse(src)
    node = mod.body[0]

    for stmt in node.body:
        if type(stmt) != ast.AnnAssign:
            continue
        __rewrite_AnnAssign(stmt)

    cobj = compile(mod, '<string>', 'exec')
    return cobj

