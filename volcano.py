import argparse
import ast
import os

class VolcanoTransformer(ast.NodeTransformer):
    pass

class VolcanoVisitor(ast.NodeVisitor):
    def __init__(self):
        self.output = ''

    def generic_visit(self, node):
        self.output += f'{type(node).__name__}('
        for field, value in ast.iter_fields(node):
            self.output += f'{field}='
            if isinstance(value, ast.AST):
                self.visit(value)
            elif isinstance(value, list):
                self.output += '['
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)
                    else:
                        self.output += repr(item)
                    self.output += ', '
                self.output = self.output[:-2] + ']'
            else:
                self.output += repr(value)
            self.output += ', '
        self.output = self.output[:-2] + ')'

    def visit(self, node):
        if isinstance(node, ast.AST):
            self.generic_visit(node)
        else:
            self.output += repr(node)
    
def process_file(filename):

    with open(filename, 'r') as f:
        contents = f.read()

    tree = ast.parse(contents)

    transformer = VolcanoTransformer()
    tree = transformer.visit(tree)

    return tree

def cli():
    parser = argparse.ArgumentParser(description='Process a file.')
    parser.add_argument('file', type=str, help='path to the file')
    parser.add_argument('--output', '-o', type=str, default=None, help='path to the output file')

    args = parser.parse_args()

    # If no output file is specified, use the input filename with ".sh" appended
    if args.output is None:
        base_name, _ = os.path.splitext(args.file)
        args.output = f'{base_name}.sh'
    
    tree = process_file(args.file)
    
    visitor = VolcanoVisitor()
    visitor.visit(tree)

    with open(args.output, 'w') as f:
        f.write(visitor.output)

if __name__ == '__main__':
    cli()