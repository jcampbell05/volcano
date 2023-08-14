from _ast import *
from _ast import Constant, For, FormattedValue, JoinedStr, Name
import argparse
import ast
import os
import tempfile
from typing import Any

# TODO: Extract into seperate files
#
class VolcanoTransformer(ast.NodeTransformer):
    pass

class VolcanoVisitor(ast.NodeVisitor):

    def __init__(self, shell_executable):
        self.output = ''
        self.generate_shabang(shell_executable)

    def generate_shabang(self, shell_executable):
        self.output += f'#!{shell_executable}\n'

    def visit_Call(self, node: Call):
            self.output += node.func.id

            for index, arg in enumerate(node.args):
                self.output += ' ' if index == 0 else ', '
                self.visit(arg)

    def visit_Constant(self, node: Constant) -> Any:
        self.output +=  node.value

    def visit_FunctionDef(self, node: FunctionDef):
        self.output += f'{node.name} () {{\n'

        for index, arg in enumerate(node.args.args):
            self.output += f'{arg.arg}=${index + 1}\n'

        for statement in node.body:
            self.visit(statement)

        self.output += '\n}\n'

    def visit_Name(self, node: Name) -> Any:
        self.output += f'${node.id}'

    def visit_JoinedStr(self, node: JoinedStr) -> Any:
        self.output += '"' 

        for value in node.values:
            self.visit(value)

        self.output += '"'

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

    os.system(f'{args.shell} {output_file.name}')

if __name__ == '__main__':
    cli()