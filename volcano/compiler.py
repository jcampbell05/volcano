from _ast import *
from _ast import Constant, For, JoinedStr, Name
import ast
import importlib.util

class VolcanoTransformer(ast.NodeTransformer):
    
    def visit_Module(self, node):
        
        # Add import stdlib statement to beginning of module body
        #
        new_body = [ast.parse('import volcano.stdlib').body[0]] + node.body
        node.body = new_body

        return node

class VolcanoVisitor(ast.NodeVisitor):

    if_target = False
    capture_call = False
    indent_token = '    '

    def __init__(self, shell_executable):
        self.output = ''
        self.generate_shabang(shell_executable)

    def generate_shabang(self, shell_executable):
        self.output += f'#!{shell_executable}\n'

    def visit_Assign(self, node: Assign):

        for target in node.targets:

            if isinstance(target, Name):
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
            self.output += self.indent_token
            self.visit(statement)

        self.output += '\ndone'

    def visit_FunctionDef(self, node: FunctionDef):

        self.output += f'{node.name} () {{\n'

        for index, arg in enumerate(node.args.args):
            self.output += f'{arg.arg}=${index + 1}\n'

        for statement in node.body:
            self.output += self.indent_token
            self.visit(statement)

        self.output += '\n}'

    def visit_Import(self, node: Import):

        for alias in node.names:
            
            # Load .vol file with same name as import
            module_name = alias.name

            if module_name == 'volcano.shell':

                # Volcano shell is a virtual module used to indicate methods from
                # the shell, we don't need to import anything it's mainly there
                # to silence compiler errors - in the future tooling could be updated
                # to use this module to provide autocomplete for shell methods
                #
                continue

            module_spec = importlib.util.find_spec(module_name)
        
            print("Spec: ", module_spec)
            # if module_spec is not None and module_spec.origin.endswith('.vol'):
            #     with open(module_spec.origin, 'r') as f:
            #         module_code = f.read()
            #     module_tree = ast.parse(module_code)

            #     # Inject module contents into current script
            #     for module_node in module_tree.body:
            #         self.visit(module_node)

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

    def visit_Return(self, node: Return):
        self.output += 'echo '

        self.capture_call = True
        self.visit(node.value)
        self.capture_call = False