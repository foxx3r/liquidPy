import ast
import inspect
import types

class FunctionRefiner(ast.NodeTransformer):
    def visit_FunctionDef(self, node: ast.FunctionDef):
        for stmt in node.body:
            self.visit(stmt)
        return node

    def visit_If(self, node: ast.If):
        for stmt in node.body:
            self.visit(stmt)
        return node

    def visit_AnnAssign(self, node: ast.AnnAssign):
        print("Transforming")
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
        return node

def get_refined_function(f: types.FunctionType):
    refiner = FunctionRefiner()

    src = inspect.getsource(f)
    node = ast.parse(src)
    node = refiner.visit(node)

    cobj = compile(node, '<string>', 'exec')
    name = cobj.co_names[-1]
    scope = dict()
    exec(cobj, f.__globals__, scope)
    return scope[name]

