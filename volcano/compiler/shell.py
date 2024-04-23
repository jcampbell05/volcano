import ast
from volcano.ast.shell import *
from typing import Any

class Shell(ast.NodeVisitor):

    def visit_Script(self, node):
        output = "#!"
        return output

    def __call__(self, root) -> Any:
        output = self.visit(root)
        return output