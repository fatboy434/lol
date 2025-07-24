import ast

class MessageInjector(ast.NodeTransformer):
    def __init__(self, main_file):
        self.main_file = main_file

    def visit_FunctionDef(self, node):
        # This is a simplified version that just adds a call to a message router.
        # A more robust solution would also handle arguments and return values.
        if node.name != "__init__":
            node.body.insert(0, ast.Expr(value=ast.Call(
                func=ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr='send_message', ctx=ast.Load()),
                args=[ast.Constant(value=f"Calling function {node.name}")],
                keywords=[]
            )))
        return node

    def inject(self, file_path):
        with open(file_path, "r") as f:
            tree = ast.parse(f.read(), filename=file_path)

        new_tree = self.visit(tree)

        with open(file_path, "w") as f:
            f.write(ast.unparse(new_tree))
