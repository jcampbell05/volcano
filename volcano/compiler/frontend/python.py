from _ast import *
from _ast import Assign, Expr, ListComp, Try
import ast
from syntax import *
from typing import Any

class IRTransformer(ast.NodeTransformer):
    """
    The IRTransformaer transforms the code before it reaches the shell script generator
    into an intermediate representation that is easier to work with. Since some high level
    features of Volcano cannot be easily translated into shell script.
    """

    list_comp_count = 0
    tree = Script()

    def __init__(self) -> None:
        self.scope = None

    def create_import_module_node(self, path):

        # Add import io statement to beginning of module body
        #
        new_body = [ast.parse(f'import {path}').body[0]]
        return new_body
    
    def create_function_call(self, func: FunctionDef):
        return ast.Call(
            func=ast.Name(id=func.name),
            args=[],
            kwargs=[],
        )
    
    def unwrap_list_comp_node(self, list_comp: ListComp):

        flat_body = []

        for generator in list_comp.generators:

                for_def = ast.For(
                    target=generator.target,
                    iter=generator.iter
                )

                flat_body.append(for_def)

                ifs = [ast.If(
                    test=generator_if
                )  for generator_if in generator.ifs]

                flat_body.extend(ifs)

        for parent_index, child_node in enumerate(flat_body[1:]):

            parent_node = flat_body[parent_index]
            parent_node.body = [child_node]
                
        flat_body[-1].body = [
            ast.Assign(
                targets=[ast.Name(id='RESULT')],
                value=list_comp.elt
            ),
            ast.parse('array_append(ACCUMULATED, RESULT)').body[0],
            ast.parse('ACCUMULATED = RESULT').body[0],
        ]

        self.list_comp_count += 1

        func_def = ast.FunctionDef(
            name = f'list_comp_{self.list_comp_count}',
            args=ast.arguments(
                args=[],
                kwarg=None,
                defaults=[],
                kw_defaults=[],
            ),
            body=[
                ast.parse('ACCUMULATED=()').body[0],
                flat_body[0],
                ast.parse('return ACCUMULATED').body[0]
            ],
            decorator_list=[],
            returns=None
        )
        
        return func_def
        
    def visit_Module(self, node: Module):

        default_imports = [
            'volcano.vssembly',
            'volcano.runtime'
        ]
        default_imports.reverse()
        
        self.scope = node
        
        self.generic_visit(node)

        for module in default_imports:
            node.body = self.create_import_module_node(module) + node.body

        return node
    
    def visit_Assign(self, node: Assign):

        if isinstance(node.value, ast.ListComp):
            unwrapped_node = self.unwrap_list_comp_node(node.value)
            node.value = self.create_function_call(unwrapped_node)

            return [unwrapped_node, node]

        self.generic_visit(node)
        return node
    
    def visit_Expr(self, node: Expr):

        if isinstance(node.value, ast.ListComp):
            unwrapped_node = self.unwrap_list_comp_node(node.value)
            node.value = self.create_function_call(unwrapped_node)

            return [unwrapped_node, node]

        self.generic_visit(node)
        return node
    
    def visit_Try(self, node: Try) -> Any:

        except_def = ast.FunctionDef(
            name = 'except',
            args=ast.arguments(
                args=[
                    ast.arg(arg='error', annotation=None)
                ],
                kwarg=None,
                defaults=[],
                kw_defaults=[],
            ),

            body= node.handlers[0].body
        )

        try_def = ast.FunctionDef(
            name = 'try',
            args=ast.arguments(
                args=[],
                kwarg=None,
                defaults=[],
                kw_defaults=[],
            ),
            body=node.body + node.orelse
        )

        # body: list[stmt]
        # handlers: list[ExceptHandler]

        #trap 'handle_error "$?"' ERR

        return [
            # Set trap
            except_def,
            try_def,
            ast.Call(
                ast.Name(id='trap'),
                args=[
                    ast.Constant(value='except "$?"'),
                    ast.Constant(value='ERR'),
                ],
                kwargs=[]
            ),
            ast.Call(
                ast.Name(id='try'),
                args=[],
                kwargs=[]
            ),
            ast.Call(
                ast.Name(id='trap'),
                args=[
                    ast.Constant(value='-'),
                    ast.Constant(value='ERR'),
                ],
                kwargs=[]
            ),
        ] + node.finalbody