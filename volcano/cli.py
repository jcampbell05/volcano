import argparse
import ast
import os
import shutil
import subprocess
import tempfile

from .compiler import *

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

    parser.add_argument('--run', '-r', action='store_true', help='run the shell executable')
    parser.add_argument('--shell', '-s', type=str, default='/bin/sh', help='path to the shell executable')
    parser.add_argument('--output', '-o', type=str, default=None, help='path to the output file')
    parser.add_argument('--verbose', '-v', action='store_true', help='enable verbose output')
    parser.add_argument('--stdout', action='store_true', help='log compiled shell script to srdout')

    args = parser.parse_args()

    # If no output file is specified, use the input filename with ".sh" appended
    if args.output is None:
        base_name, _ = os.path.splitext(args.file)
        args.output = f'{base_name}.sh'

    module_name = os.path.splitext(os.path.basename(args.output))[0]
    tree = process_file(args.file)
    
    visitor = VolcanoVisitor(module_name, args.shell) 
    visitor.visit(tree)

    output_file = tempfile.NamedTemporaryFile(mode='w', delete=False)

    if args.stdout:
        print(visitor.output)

    with output_file as f:
        f.write(visitor.output)

    os.chmod(output_file.name, 0o755)

    if not args.stdout:
        shutil.copy(output_file.name, args.output)

    if args.run:
        subprocess.run([output_file.name], check=True)

if __name__ == '__main__':
    cli()