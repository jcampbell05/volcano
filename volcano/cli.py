import argparse
import ast
import os
import tempfile

from .compiler import *

# TODO:
# - Implement reserved keywords
# - Implement print
# - Allow pretty mdoe with Indentation for outout
# - Intermediate IR to be able to more advanced reasoning of the code and result with better shell code
# - Use python's logger
# - Comments for source maps
#
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