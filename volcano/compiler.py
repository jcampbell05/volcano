from _ast import *
from _ast import Constant, For, JoinedStr, Name
import ast
import pkg_resources
import os
import uuid

class VolcanoTransformer(ast.NodeTransformer):
    
    def visit_Module(self, node):

        # Add import io statement to beginning of module body
        #
        new_body = [ast.parse('import volcano.io').body[0]] + node.body
        node.body = new_body
        
        # Add import stdlib statement to beginning of module body
        #
        new_body = [ast.parse('import volcano.stdlib').body[0]] + node.body
        node.body = new_body

        return node

class VolcanoVisitor(ast.NodeVisitor):

    control_flow_target = False
    capture_call = False
    function_def_has_return = False
    in_joined_str = False

    indent_lavel = 0
    indent_token = '    '

    def __init__(self, shell_executable):
        self.output = ''
        self.generate_shabang(shell_executable)

    def generate_shabang(self, shell_executable):
        self.write(f'#!{shell_executable}\n')

    def load_volcano_module(self, package_name, resource_name):

        module_code = pkg_resources.resource_string(package_name, resource_name + '.vol')
        module_tree = ast.parse(module_code)

        # Inject module contents into current script
        #
        for module_node in module_tree.body:
            self.visit(module_node)

    def load_shell_module(self, package_name, resource_name):
        sh_module_code = pkg_resources.resource_string(package_name, resource_name + '.sh')
        self.write(sh_module_code.decode('utf-8'))

    def visit_Assign(self, node: Assign):

        for target in node.targets:

            if isinstance(target, Name):
                self.write(f'{target.id}=')
                self.visit(node.value)

    def visit_BinOp(self, node: BinOp):

        self.write(f'$( echo "' )
        self.visit(node.left)

        if isinstance(node.op, Add):
            self.write('+')
        elif isinstance(node.op, Sub):
            self.write('-')
        elif isinstance(node.op, Mult):
            self.write('*')
        elif isinstance(node.op, Div):
            self.write('/')

        self.visit(node.right)

        self.write('" | bc -l )')

    def visit_Call(self, node: Call):
            
            is_captured_call = self.capture_call
            
            if is_captured_call:
                self.write('$( RESULT= && ')

            self.write(node.func.id)
            self.capture_call = True

            for index, arg in enumerate(node.args):
                self.write(' ' if index == 0 else ', ')
                self.visit(arg)

            self.capture_call = False

            if is_captured_call:
                self.write(' && echo $RESULT)')

    def visit_Compare(self, node: Compare):

        self.write('[ ')
        self.visit(node.left)

        for i, op in enumerate(node.ops):
            right = node.comparators[i]

            if isinstance(op, ast.Eq):
                self.write(' =  ')
                self.visit(right)

        self.write(' ]')

    def visit_Constant(self, node: Constant):
        if isinstance(node.value, str) and not self.in_joined_str:
            self.write(f'"{node.value}"')
        else:
            self.write(str(node.value))

    def visit_For(self, node: For):

        self.write('for ')

        self.control_flow_target = True
        self.visit(node.target)
        self.control_flow_target = False

        self.write(' in ')
        self.visit(node.iter)

        self.write(';\n')
        self.write('do\n')

        self.indent_lavel += 1
        
        for statement in node.body:
            self.write('', indent=True)
            self.visit(statement)

        self.indent_lavel -= 1

        self.write('\ndone')

    def visit_FunctionDef(self, node: FunctionDef):

        self.write(f'{node.name} () {{\n')

        args: arguments = reversed(node.args.args)
        defaults = reversed(node.args.defaults)

        self.indent_lavel += 1

        for index, arg in enumerate(args):

            default = next(defaults, None)
            default = default.value if default is not None else ''

            self.write('', indent=True)
            self.write(f'local {arg.arg}=${{{index + 1}:-{default}}}')
            self.write('\n')

        for statement in node.body:
            self.write('', indent=True)
            self.visit(statement)
            self.write('\n')

        self.indent_lavel -= 1
    
        self.write(' }\n', indent=True)

    def visit_If(self, node: If):

         # node.test
        self.write('if [')
        self.visit(node.test)
        self.write(']\n')
        self.write('', indent=True)
        self.write('then\n')

        self.indent_lavel += 1

        for statement in node.body:
            self.write('', indent=True)
            self.visit(statement)
            self.write(' \n')

        self.indent_lavel -= 1

        # # Visit else statement body, if present
        # if node.orelse:
        #     self.visit(node.orelse)

        self.write('', indent=True)
        self.write('fi\n')

    def visit_Import(self, node: Import):

        for alias in node.names:
            
            # Load .vol file with same name as import
            import_path = alias.name

            if import_path == 'volcano.shell':

                # Volcano shell is a virtual module used to indicate methods from
                # the shell, we don't need to import anything it's mainly there
                # to silence compiler errors - in the future tooling could be updated
                # to use this module to provide autocomplete for shell methods
                #
                continue

            package_name = import_path.split('.')[0]
            resource_name = os.path.join(*import_path.split('.')[1:]) 

            try:
                self.load_volcano_module(package_name, resource_name)
                return
            except FileNotFoundError:
                pass

            try:
                self.load_shell_module(package_name, resource_name)  
                return          
            except FileNotFoundError:
                pass

            raise ImportError(f"No module named '{import_path}'")


    def visit_Module(self, node):

        for statement in node.body:
            self.visit(statement)
            self.write('\n')

    def visit_List(self, node):

        self.write('"')

        self.capture_call = True
        
        for index, item in enumerate(node.elts):
            self.write('' if index == 0 else ' ')
            self.visit(item)

        self.capture_call = False

        self.write('"')

    def visit_Name(self, node: Name):

        if self.control_flow_target:
            self.write(node.id)
        else:
            self.write(f'${node.id}')

    def visit_JoinedStr(self, node: JoinedStr):

        self.capture_call = True
        self.write('"' )

        self.in_joined_str = True

        for value in node.values:
            self.visit(value)

        self.in_joined_str = False

        self.write('"')
        self.capture_call = False

    def visit_Return(self, node: Return):
        self.write('RESULT=')

        self.capture_call = True

        if node.value is not None:
            self.visit(node.value)
        
        self.write('\n')
        self.write('return', indent=True)

        self.capture_call = False

    def write(self, token, indent=False):
    
        if indent:
            self.output += self.indent_token * self.indent_lavel

        self.output += token