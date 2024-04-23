from volcano.ast.shell import *
from typing import any

class Shell(ast.NodeVisitor):

    def __call__(self, root) -> Any:
        output = self.visit(root)
        return output