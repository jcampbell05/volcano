from _ast import *
from _ast import Constant, For, JoinedStr, Name
import argparse
import ast
import os
import tempfile
from typing import Any

# TODO:
# - Extract into seperate files
# - Setup Repo
# - Roadmap
# - Allow pretty mdoe with Indentation for outout
#
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

    def visit_Assign(self, node: ast.Assign) -> Any:

        for target in node.targets:

            if isinstance(target, ast.Name):
                self.output += f'{target.id}='
                self.visit(node.value)

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

    def visit_Constant(self, node: Constant) -> Any:
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

    def visit_Name(self, node: Name) -> Any:

        if self.if_target:
            self.output += node.id
        else:
            self.output += f'${node.id}'

    def visit_JoinedStr(self, node: JoinedStr) -> Any:

        self.capture_call = True
        self.output += '"' 

        for value in node.values:
            self.visit(value)

        self.output += '"'
        self.capture_call = False

    def visit_Return(self, node: ast.Return) -> Any:
        self.output += 'echo '

        self.capture_call = True
        self.visit(node.value)
        self.capture_call = False

def process_file(filename):

    with open(filename, 'r') as f:
        contents = f.read()

    tree = ast.parse(contents)
    transformer = VolcanoTransformer()
    tree = transformer.visit(tree)

    return tree

def cli():
    parser = argparse.ArgumentParser(description='Process a file.')
    parser.add_argument('command', type=str, choices=['build', 'run'], help='the action to perform')
    parser.add_argument('file', type=str, help='path to the file')

    parser.add_argument('--shell', '-s', type=str, default='/bin/sh', help='path to the shell executable')
    parser.add_argument('--output', '-o', type=str, default=None, help='path to the output file')
    parser.add_argument('--verbose', '-v', action='store_true', help='enable verbose output')

    args = parser.parse_args()

    # If no output file is specified, use the input filename with ".sh" appended
    if args.output is None:
        base_name, _ = os.path.splitext(args.file)
        args.output = f'{base_name}.sh'
    
    tree = process_file(args.file)
    
    # TODO: Pick best visitor based on shell bacause some shells like fish have different syntax and anre't posix compliant
    #
    visitor = VolcanoVisitor(args.shell) 
    visitor.visit(tree)

    if args.verbose:
        print(visitor.output)

    output_file = None

    if args.command == 'run':
        output_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    else:
        output_file = open(args.output, 'w')

    with output_file as f:
        f.write(visitor.output)

    os.chmod(output_file.name, 0o755)
    os.system(f'{output_file.name}')

if __name__ == '__main__':
    cli()