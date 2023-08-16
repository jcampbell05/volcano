from _ast import *
from _ast import Constant, For, JoinedStr, Name
import ast
import pkg_resources
import os

class VolcanoTransformer(ast.NodeTransformer):
    """
    The VolcanoTransformaer transforms the code before it reaches the shell script generator
    into something that is easier to work with. Since some high level features of Volcano
    cannot be easily translated into shell script.
    """

    def import_module(self, node: Module, path):

        # Add import io statement to beginning of module body
        #
        new_body = [ast.parse(f'import {path}').body[0]] + node.body
        return new_body
    
    def visit_Module(self, node: Module):

        self.generic_visit(node)

        node.body = self.import_module(node, 'volcano.runtime')
        return node
    
    def visit_IfExp(self, node: ast.IfExp):

        # Define the function
        func_name = 'my_func'
        func_args = ast.arguments(args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[])
        func_body = [ast.Pass()]
        func_def = ast.FunctionDef(name=func_name, args=func_args, body=func_body, decorator_list=[])

        # Create an Insert node to inject the function before the current statement
        insert_node = ast.Insert(body=[func_def], before=node)

        # Replace the IfExp node with the Insert node
        return insert_node
    
    def visit_GeneratorExp(self, node: ListComp):
        
        # Define the function
        func_name = 'my_func'
        func_args = ast.arguments(args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[])
        func_body = [ast.Pass()]
        func_def = ast.FunctionDef(name=func_name, args=func_args, body=func_body, decorator_list=[])

        # Create an Insert node to inject the function before the current statement
        insert_node = ast.Insert(body=[func_def], before=node)

        # Replace the IfExp node with the Insert node
        return insert_node
    
    def visit_ListComp(self, node):
        # Extract the components of the list comprehension
        elt = node.elt
        generators = node.generators

        # Create a new for loop node with the same target and iter as the first generator
        first_gen = generators[0]
        target = first_gen.target
        iter = first_gen.iter
        for_loop = ast.For(target=target, iter=iter, body=[])
        if_stmt = None

        # Add the remaining generators as if statements inside the for loop
        for gen in generators[1:]:
            if gen.ifs:
                if_stmt = ast.If(test=gen.ifs[0], body=[], orelse=[])
                for_loop.body.append(if_stmt)
                for_loop = if_stmt.body[0]

            # Update the target and iter of the for loop to match the current generator
            target = gen.target
            iter = gen.iter
            for_loop.target = target
            for_loop.iter = iter

        # Add the final expression as the body of the innermost if statement or the for loop
        if if_stmt is not None:
            if_stmt.body.append(ast.Expr(value=elt))
        else:
            for_loop.body.append(ast.Expr(value=elt))

        # Return the new for loop node
        return for_loop

class VolcanoVisitor(ast.NodeVisitor):

    symbol_tables = {}
    scope_stack = []

    declare_variable = False
    capture_call = False
    function_def_has_return = False
    in_joined_str = False

    indent_lavel = 0
    indent_token = '    '

    def __init__(self, module_name, shell_executable):

        self.module_name = module_name
        self.output = ''

        self.generate_header(shell_executable)
        self.push_scope(module_name.replace('-', '_'))

    @property
    def current_scope(self):
        return self.scope_stack[-1]

    def generate_header(self, shell_executable):
        self.write(f'#!{shell_executable}\n')
        self.write(f'# Generated by Volcano from {self.module_name}.vol\n')
        self.write(f'\n')
        self.write(f'set -o posix\n')
        self.write(f'\n')

    def pop_scope(self):
        old_scope = self.scope_stack.pop()
        del self.symbol_tables[old_scope]

    def push_scope(self, name: str):
        self.scope_stack.append(name)
        self.symbol_tables[name] = {}

    def load_volcano_module(self, package_name, resource_name):

        module_code = pkg_resources.resource_string(package_name, resource_name + '.vol')
        module_tree = ast.parse(module_code)

        # Inject module contents into current script
        #
        for module_node in module_tree.body:
            self.visit(module_node)

    def load_shell_module(self, package_name, resource_name):
        sh_module_code = pkg_resources.resource_string(package_name, resource_name + '.vsh')
        self.write(sh_module_code.decode('utf-8'))

    def register_symbol(self, name: str):
        scope = self.current_scope
        alias = f'{scope}_{name}'

        self.symbol_tables[scope][name] = alias
        return alias

    def resolve_name(self, name: str):
        
        for scope in reversed(self.scope_stack):
            table = self.symbol_tables[scope]

            if name in table:
                return table[name]

        return name
    
    def write(self, token, indent=False):
    
        if indent:
            self.output += self.indent_token * self.indent_lavel

        self.output += token

    def visit_Assign(self, node: Assign):

        for target in node.targets:

            self.declare_variable = True
            self.visit(target)
            self.declare_variable = False
            

            self.write(f'=')

            self.capture_call = True
            self.visit(node.value)
            self.capture_call = False

    def visit_AugAssign(self, node: AugAssign):

        self.declare_variable = True
        self.visit(node.target)
        self.declare_variable = False

        self.write(f'=')
        self.write('$( awk "BEGIN {print ' )

        self.visit(node.target)

        if isinstance(node.op, ast.Add):
            self.write('+')
        elif isinstance(node.op, ast.Sub):
            self.write('-')
        else:
            raise NotImplementedError(f"Unsupported operator {node.op}")

        self.capture_call = True
        self.visit(node.value)
        self.capture_call = False

        self.write('}")')

    def visit_BoolOp(self, node: BoolOp):

        if isinstance(node.op, ast.Not):
                self.write('!')  

        for index, value in enumerate(node.values):

            if index > 0 and not isinstance(node.op, ast.Not):
                if isinstance(node.op, ast.Or):
                    self.write(' ] || [ ')
                elif isinstance(node.op, ast.And):
                    self.write(' ] && [ ')
                else:
                    raise NotImplementedError(f"Unsupported operator {node.op}")
            
            self.visit(value)

    def visit_BinOp(self, node: BinOp):

        self.write('$( awk "BEGIN {print ' )
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

        self.write('}")')

    def visit_Call(self, node: Call):
            
            is_captured_call = self.capture_call
            
            if is_captured_call:
                self.write('$( RESULT= && ')

            self.write(
                self.resolve_name(node.func.id)
            )
            self.capture_call = True

            for index, arg in enumerate(node.args):
                self.write(' ' if index == 0 else ', ')
                self.visit(arg)

            self.capture_call = False

            if is_captured_call:
                self.write(' && echo $RESULT)')

    # TODO: Implement not
    #
    def visit_Compare(self, node: Compare):

        self.visit(node.left)

        for i, op in enumerate(node.ops):
            right = node.comparators[i]

            if isinstance(op, ast.Eq):
                self.write(' = ')
                self.visit(right)
            elif isinstance(op, ast.Is):
                self.write(' = ')
                self.visit(right)
            elif isinstance(op, ast.NotEq):
                self.write(' != ')
                self.visit(right)
            elif isinstance(op, ast.Gt):
                self.write(' -gt ')
                self.visit(right)
            elif isinstance(op, ast.GtE):
                self.write(' -ge ')
                self.visit(right)
            elif isinstance(op, ast.Lt):
                self.write(' -lt ')
                self.visit(right)
            elif isinstance(op, ast.LtE):
                self.write(' -le ')
                self.visit(right)
            else:
                raise NotImplementedError(f"Unsupported operator {op}")

    def visit_Constant(self, node: Constant):
        if isinstance(node.value, str) and not self.in_joined_str:
            self.write(f'"{node.value}"')
        else:
            self.write(str(node.value))

    def visit_For(self, node: For):

        self.write('for ')

        self.declare_variable = True
        self.visit(node.target)
        self.declare_variable = False

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

        function_name = self.register_symbol(node.name)

        self.write(f'{function_name} () {{\n')

        args: arguments = reversed(node.args.args)
        defaults = reversed(node.args.defaults)

        self.indent_lavel += 1

        for index, arg in enumerate(args):

            default = next(defaults, None)
            default = default.value if default is not None else ''

            self.write('', indent=True)
            self.write(f'local {arg.arg}=${{{index + 1}:-{default}}}')
            self.write('\n')

        self.push_scope(function_name)

        for statement in node.body:
            self.write('', indent=True)
            self.visit(statement)
            self.write('\n')

        self.pop_scope()

        self.indent_lavel -= 1
        self.write(' }\n', indent=True)

    def visit_If(self, node: If):

        self.write('if [ ')
        self.visit(node.test)
        self.write(' ]\n')
        self.write('', indent=True)
        self.write('then\n')

        self.indent_lavel += 1

        for statement in node.body:
            self.write('', indent=True)
            self.visit(statement)
            self.write(' \n')

        self.indent_lavel -= 1

        if len(node.orelse) > 0:

            self.write('', indent=True)
            self.write('else\n')

            self.indent_lavel += 1

            for statement in node.orelse:
                self.write('', indent=True)
                self.visit(statement)
                self.write(' \n')

            self.indent_lavel -= 1

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

        name = self.resolve_name(node.id)

        if self.declare_variable:
            self.write(name)
        else:
            self.write(f'${name}')

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

    def visit_UnaryOp(self, node: UnaryOp):

        if isinstance(node.op, ast.Not):
            self.write(' ! ')
            self.visit(node.operand)
        else:
            raise NotImplementedError(f"Unsupported operator {node.op}")

    def visit_While(self, node: While):
        
        self.write('while [ ')
        self.visit(node.test)
        self.write(' ]\n')
        self.write('', indent=True)
        self.write('do\n')

        self.indent_lavel += 1

        for statement in node.body:
            self.write('', indent=True)
            self.visit(statement)
            self.write(' \n')

        self.indent_lavel -= 1

        self.write('', indent=True)
        self.write('done\n')

        if len(node.orelse) > 0:

            for statement in node.orelse:
                self.write('', indent=True)
                self.visit(statement)
                self.write(' \n')

