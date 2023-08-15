from _ast import *
from _ast import Constant, For, JoinedStr, Name
import ast

class VolcanoTransformer(ast.NodeTransformer):
    pass

class VolcanoVisitor(ast.NodeVisitor):

    if_target = False
    capture_call = False

    def __init__(self, shell_executable):
        self.output = ''
        self.generate_shabang(shell_executable)

    def generate_shabang(self, shell_executable):
        self.output += f'#!{shell_executable}\n'

    def visit_Assign(self, node: ast.Assign):

        for target in node.targets:

            if isinstance(target, ast.Name):
                self.output += f'{target.id}='
                self.visit(node.value)

    def visit_BinOp(self, node: BinOp):

        self.output += f'$( echo "' 

        self.visit(node.left)

        if isinstance(node.op, Add):
            self.output += '+'
        elif isinstance(node.op, Sub):
            self.output += '-'
        elif isinstance(node.op, Mult):
            self.output += '*'
        elif isinstance(node.op, Div):
            self.output += '/'

        self.visit(node.right)

        self.output += '" | bc )'

    def visit_Call(self, node: Call):
            
            is_captured_call = self.capture_call
            
            if is_captured_call:
                self.output += '$('

            self.output += node.func.id
            self.capture_call = True

            for index, arg in enumerate(node.args):
                self.output += ' ' if index == 0 else ', '
                self.visit(arg)

            self.capture_call = False

            if is_captured_call:
                self.output += ')'

    def visit_Constant(self, node: Constant):
        if isinstance(node.value, str):
            self.output += f'"{node.value}"'
        else:
            self.output += str(node.value)

    def visit_For(self, node: For):

        self.output += 'for '

        self.if_target = True
        self.visit(node.target)
        self.if_target = False

        self.output += ' in '
        self.visit(node.iter)

        self.output += ';\n'
        self.output += 'do\n'
        
        for statement in node.body:
            self.visit(statement)

        self.output += '\ndone'

    def visit_FunctionDef(self, node: FunctionDef):

        self.output += f'{node.name} () {{\n'

        for index, arg in enumerate(node.args.args):
            self.output += f'{arg.arg}=${index + 1}\n'

        for statement in node.body:
            self.visit(statement)

        self.output += '\n}'

    def visit_Module(self, node):

        for statement in node.body:
            self.visit(statement)
            self.output += '\n'

    def visit_List(self, node):

        self.output += '"'

        self.capture_call = True
        
        for index, item in enumerate(node.elts):
            self.output += '' if index == 0 else ' '
            self.visit(item)

        self.capture_call = False

        self.output += '"'

    def visit_Name(self, node: Name):

        if self.if_target:
            self.output += node.id
        else:
            self.output += f'${node.id}'

    def visit_JoinedStr(self, node: JoinedStr):

        self.capture_call = True
        self.output += '"' 

        for value in node.values:
            self.visit(value)

        self.output += '"'
        self.capture_call = False

    def visit_Return(self, node: ast.Return):
        self.output += 'echo '

        self.capture_call = True
        self.visit(node.value)
        self.capture_call = False