import argparse
import ast
import os
import tempfile

class VolcanoTransformer(ast.NodeTransformer):
    pass

class VolcanoVisitor(ast.NodeVisitor):

    shell_executable = '/bin/bash'

    def __init__(self):
        self.output = ''
        self.generate_shabang()

    def generate_shabang(self):
        self.output += f'#!{self.shell_executable}\n'

    def visit_FunctionDef(self, node):
        self.output += f'''{node.name} () {{\n\
echo
}}\n'''

    def visit_Call(self, node):
            func_name = node.func.id
            args = '' #', '.join([self.visit(arg) for arg in node.args])
            self.output += f'{func_name}{args}'
    
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
    parser.add_argument('--output', '-o', type=str, default=None, help='path to the output file')
    parser.add_argument('--verbose', '-v', action='store_true', help='enable verbose output')

    args = parser.parse_args()

    # If no output file is specified, use the input filename with ".sh" appended
    if args.output is None:
        base_name, _ = os.path.splitext(args.file)
        args.output = f'{base_name}.sh'
    
    tree = process_file(args.file)
    
    visitor = VolcanoVisitor()
    visitor.visit(tree)

    if args.verbose:
        print(visitor.output)

    if args.command == 'build':

        with open(args.output, 'w') as f:
            f.write(visitor.output)

    elif args.command == 'run':
        os.system(f'bash -c "{visitor.output}"')

if __name__ == '__main__':
    cli()