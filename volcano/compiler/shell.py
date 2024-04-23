from volcano.ast.shell import *

class Shell(ast.NodeVisitor):
    def __call__(self, root):
        output = self.visit(root)
        return output