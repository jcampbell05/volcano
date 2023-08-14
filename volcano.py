import argparse
import ast
import os

class VolcanoTransformer(ast.NodeTransformer):

    def visit_FunctionDef(self, node):
        # Modify the function name
        node.name = 'new_' + node.name

        # Add a new argument to the function
        arg = ast.arg(arg='new_arg', annotation=None)
        node.args.args.append(arg)

        # Return the modified node
        return node
    
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
    
    root_node = process_file(args.file)

    with open(args.output, 'w') as f:
        print("sss")
        f.write(ast.unparse(root_node)) # TODO: Replace with custom to_str code

if __name__ == '__main__':
    cli()