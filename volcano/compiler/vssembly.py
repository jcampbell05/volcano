from _ast import *
from _ast import Assign, Constant, For, JoinedStr, Name
import ast
import pkg_resources
from volcano.ast.shell import *
import os
from volcano.ast.shell import *
from typing import Any

class Vssembly(ast.NodeVisitor):

    symbol_tables = {}
    scope_stack = []

    declare_variable = False
    capture_call = False
    function_def_has_return = False
    in_joined_str = False

    indent_lavel = 0
    indent_token = '    '

    def __init__(self, module_name, main=None):

        self.module_name = module_name
        self.main = main
        self.output = ''

        self.push_scope(module_name.replace('-', '_'))

    @property
    def current_scope(self):
        return self.scope_stack[-1]

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

        

    # def load_shell_module(self, package_name, resource_name):
    #     sh_module_code = pkg_resources.resource_string(package_name, resource_name + '.vsh')
    #     self.write(sh_module_code.decode('utf-8'))

    # def register_symbol(self, name: str):
    #     scope = self.current_scope
    #     alias = f'{scope}_{name}'

    #     self.symbol_tables[scope][name] = alias
    #     return alias

    # def resolve_name(self, name: str, return_if_not_found=True):
        
    #     for scope in reversed(self.scope_stack):
    #         table = self.symbol_tables[scope]

    #         if name in table:
    #             return table[name]

    #     return name if return_if_not_found else None
    
    def write(self, token, indent=False):
    
        if indent:
            self.output += self.indent_token * self.indent_lavel

        self.output += token + '\n'

    # def visit_Assign(self, node: Assign):

    #     for target in node.targets:

    #         self.declare_variable = True
    #         self.visit(target)
    #         self.declare_variable = False
            
    #         self.write(f'=')

    #         self.capture_call = True
    #         self.visit(node.value)
    #         self.capture_call = False

    # def visit_AugAssign(self, node: AugAssign):

    #     self.declare_variable = True
    #     self.visit(node.target)
    #     self.declare_variable = False

    #     self.write(f'=')
    #     self.write('$( ' )

    #     self.in_joined_str = True

    #     # TODO: Handle in own function
    #     #
    #     if isinstance(node.op, ast.Add):
    #         self.write('add')
    #     elif isinstance(node.op, ast.Sub):
    #         self.write('sub')
    #     else:
    #         raise NotImplementedError(f"Unsupported operator {node.op}")

    #     self.capture_call = True
    #     self.write(' ')
    #     self.visit(node.target)
    #     self.write(' ')
    #     self.visit(node.value)
    #     self.capture_call = False

    #     self.in_joined_str = False
    #     self.write(' )' )

    # def visit_BoolOp(self, node: BoolOp):

    #     if isinstance(node.op, ast.Not):
    #             self.write('!')  

    #     for index, value in enumerate(node.values):

    #         if index > 0 and not isinstance(node.op, ast.Not):
    #             if isinstance(node.op, ast.Or):
    #                 self.write(' ] || [ ')
    #             elif isinstance(node.op, ast.And):
    #                 self.write(' ] && [ ')
    #             else:
    #                 raise NotImplementedError(f"Unsupported operator {node.op}")
            
    #         self.visit(value)

    # def visit_BinOp(self, node: BinOp):

    #     self.write('$( ' )

    #     self.in_joined_str = True
    #     self.visit(node.left)

    #     if isinstance(node.op, Add):
    #         self.write('add')
    #     elif isinstance(node.op, Sub):
    #         self.write('div')
    #     elif isinstance(node.op, Mult):
    #         self.write('mul')
    #     elif isinstance(node.op, Div):
    #         self.write('div')

    #     self.visit(node.right)
    #     self.in_joined_str = False

    # def visit_Call(self, node: Call):
            
    #         is_captured_call = self.capture_call
            
    #         if is_captured_call and not self.in_joined_str:
    #             self.write('"$( ')
    #         elif is_captured_call:
    #             self.write('$( ')

    #         self.write(
    #             self.resolve_name(node.func.id)
    #         )

    #         self.capture_call = True

    #         for arg in node.args:
    #             self.write(' ')
    #             self.visit(arg)

    #         self.capture_call = False

    #         if is_captured_call and not self.in_joined_str:
    #             self.write(' )"')
    #         elif is_captured_call:
    #             self.write(' )')

    # def visit_Compare(self, node: Compare):

    #     self.visit(node.left)

    #     for i, op in enumerate(node.ops):
    #         right = node.comparators[i]

    #         if isinstance(op, ast.Eq):
    #             self.write(' = ')
    #             self.visit(right)
    #         elif isinstance(op, ast.Is):
    #             self.write(' = ')
    #             self.visit(right)
    #         elif isinstance(op, ast.NotEq):
    #             self.write(' != ')
    #             self.visit(right)
    #         elif isinstance(op, ast.Gt):
    #             self.write(' -gt ')
    #             self.visit(right)
    #         elif isinstance(op, ast.GtE):
    #             self.write(' -ge ')
    #             self.visit(right)
    #         elif isinstance(op, ast.Lt):
    #             self.write(' -lt ')
    #             self.visit(right)
    #         elif isinstance(op, ast.LtE):
    #             self.write(' -le ')
    #             self.visit(right)
    #         else:
    #             raise NotImplementedError(f"Unsupported operator {op}")

    # def visit_Constant(self, node: Constant):
    #     if isinstance(node.value, str) and not self.in_joined_str:
    #         self.write(f'"{node.value}"')
    #     else:
    #         self.write(str(node.value))

    # def visit_For(self, node: For):

    #     self.write('for ')

    #     self.declare_variable = True
    #     self.visit(node.target)
    #     self.declare_variable = False

    #     self.write(' in ')
    #     self.visit(node.iter)

    #     self.write(';\n')
    #     self.write('', indent=True)
    #     self.write('do\n')

    #     self.indent_lavel += 1
        
    #     for statement in node.body:
    #         self.write('', indent=True)
    #         self.visit(statement)
    #         self.write('\n')

    #     self.indent_lavel -= 1

    #     self.write('', indent=True)
    #     self.write('done')

    # def visit_FunctionDef(self, node: FunctionDef):

    #     function_name = self.register_symbol(node.name)

    #     self.write(f'{function_name} () {{\n')

    #     args: arguments = reversed(node.args.args)
    #     defaults = reversed(node.args.defaults)

    #     self.indent_lavel += 1

    #     self.write('RESULT=\n', indent=True)

    #     for index, arg in enumerate(args):

    #         default = next(defaults, None)
    #         default = default.value if default is not None else ''

    #         self.write('', indent=True)
    #         self.write(f'local {arg.arg}=${{{index + 1}:-{default}}}')
    #         self.write('\n')

    #     self.push_scope(function_name)

    #     for statement in node.body:
    #         self.write('', indent=True)
    #         self.visit(statement)
    #         self.write('\n')

    #     self.pop_scope()

    #     self.indent_lavel -= 1
        
    #     self.write(' }\n', indent=True)

    # def visit_If(self, node: If):

    #     self.write('if [ ')

    #     self.capture_call = True
    #     self.visit(node.test)
    #     self.capture_call = False

    #     self.write(' ]\n')
    #     self.write('', indent=True)
    #     self.write('then\n')

    #     self.indent_lavel += 1

    #     for statement in node.body:
    #         self.write('', indent=True)
    #         self.visit(statement)
    #         self.write(' \n')

    #     self.indent_lavel -= 1

    #     if len(node.orelse) > 0:

    #         self.write('', indent=True)
    #         self.write('else\n')

    #         self.indent_lavel += 1

    #         for statement in node.orelse:
    #             self.write('', indent=True)
    #             self.visit(statement)
    #             self.write(' \n')

    #         self.indent_lavel -= 1

    #     self.write('', indent=True)
    #     self.write('fi\n')

    # def visit_Import(self, node: Import):

    #     for alias in node.names:
            
    #         # Load .vol file with same name as import
    #         import_path = alias.name

    #         if import_path == 'volcano.shell':

    #             # Volcano shell is a virtual module used to indicate methods from
    #             # the shell, we don't need to import anything it's mainly there
    #             # to silence compiler errors - in the future tooling could be updated
    #             # to use this module to provide autocomplete for shell methods
    #             #
    #             continue

    #         package_name = import_path.split('.')[0]
    #         resource_name = os.path.join(*import_path.split('.')[1:]) 

    #         try:
    #             self.load_volcano_module(package_name, resource_name)
    #             return
    #         except FileNotFoundError:
    #             pass

    #         try:
    #             self.load_shell_module(package_name, resource_name)  
    #             return          
    #         except FileNotFoundError:
    #             pass

    #         raise ImportError(f"No module named '{import_path}'")


    # def visit_Module(self, node):

    #     for statement in node.body:
    #         self.visit(statement)
    #         self.write('\n')

    #     main_func_name = self.resolve_name(self.main, return_if_not_found=False)

    #     if main_func_name:

    #         self.visit(ast.Call(
    #             func=ast.Name(id=main_func_name),
    #                 args=[],
    #                 keywords=[]
    #             )
    #         )

    # def visit_List(self, node):

    #     self.write('"')

    #     self.capture_call = True
        
    #     for index, item in enumerate(node.elts):
    #         self.write('' if index == 0 else '\ ')

    #         self.in_joined_str = True
    #         self.visit(item)
    #         self.in_joined_str = False

    #     self.capture_call = False

    #     self.write('"')

    # def visit_Name(self, node: Name):

    #     name = self.resolve_name(node.id)

    #     if self.declare_variable:
    #         self.write(name)
    #     elif self.capture_call and not self.in_joined_str:
    #         self.write(f'"${name}"')
    #     else:
    #         self.write(f'${name}')

    # def visit_JoinedStr(self, node: JoinedStr):

    #     self.capture_call = True
    #     self.write('"' )

    #     self.in_joined_str = True

    #     for value in node.values:
    #         self.visit(value)

    #     self.in_joined_str = False

    #     self.write('"')
    #     self.capture_call = False

    # def visit_Return(self, node: Return):
    #     self.write('RESULT=')

    #     self.capture_call = True

    #     if node.value is not None:
    #         self.visit(node.value)
        
    #     self.write('\n')
    #     self.write('echo "$RESULT"\n', indent=True)
    #     self.write('return', indent=True)

    #     self.capture_call = False

    # def visit_UnaryOp(self, node: UnaryOp):

    #     if isinstance(node.op, ast.Not):
    #         self.write(' ! ')
    #         self.visit(node.operand)
    #     else:
    #         raise NotImplementedError(f"Unsupported operator {node.op}")

    # def visit_While(self, node: While):
        
    #     self.write('while [ ')

    #     self.capture_call = True
    #     self.visit(node.test)
    #     self.capture_call = False

    #     self.write(' ]\n')
    #     self.write('', indent=True)
    #     self.write('do\n')

    #     self.indent_lavel += 1

    #     for statement in node.body:
    #         self.write('', indent=True)
    #         self.visit(statement)
    #         self.write(' \n')

    #     self.indent_lavel -= 1

    #     self.write('', indent=True)
    #     self.write('done\n')

    #     if len(node.orelse) > 0:

    #         for statement in node.orelse:
    #             self.write('', indent=True)
    #             self.visit(statement)
    #             self.write(' \n')

    def visit_AddInstruction(self, node):
        target_name = node.output.name
        self.write(f'{target_name}=$(expr {self.visit(node.args[0])} + {self.visit(node.args[1])})')

    def visit_SetInstruction(self, node):
        target_name = node.output.name
        self.write(f'{target_name}="{"".join([self.visit(arg) for arg in node.args])}"')

    def visit_Script(self, node):
        self.write(f'#!/usr/bin/env /bin/sh')
        self.write(f'# Generated by Volcano from {self.module_name}.vol')
        self.write(f'set -o posix')
        self.write(f'set -e')
        self.write(f'set -x') # TODO: Debug mode
        self.visit(node.statement)

    def visit_Value(self, node):
        return node.value

    def visit_Variable(self, node):
        return f'{{{node.value}}}'
    
    def visit_Script(self, node):
        statements = self.visit(node.statements)
        return Script(statements)

    def __call__(self, root) -> Any:
        output = self.visit(root)
        return output