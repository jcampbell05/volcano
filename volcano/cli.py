import argparse
import ast
import os
import shutil
import subprocess
import sys
import tempfile

from .compiler import *

def process_file(filename):

    contents = ''

    if filename == '-':
        contents = sys.stdin.read()
    else:
        with open(filename, 'r') as f:
            contents = f.read()

    tree = ast.parse(contents)
    transformer = IRTransformer()
    transformer.visit(tree)
    
    return Script(
        transformer.root_statement
    )

def run():
    parser = argparse.ArgumentParser(description='Process a file.')
    parser.add_argument('command', type=str, nargs='?', choices=['build', 'run'], default='run', help='the action to perform')
    parser.add_argument('file', type=str, help='path to the file')

    parser.add_argument('--main', '-m', type=str, default='main', help='name of main function to execute by default if present')
    parser.add_argument('--output', '-o', type=str, default=None, help='path to the output file')
    parser.add_argument('--verbose', '-v', action='store_true', help='enable verbose output')
    parser.add_argument('--stdout', action='store_true', help='log compiled shell script to stdout')

    args = parser.parse_args()

    # If no output file is specified, use the input filename with ".sh" appended
    if args.output is None:
        base_name, _ = os.path.splitext(args.file)
        args.output = f'{base_name}.sh'

    module_name = os.path.splitext(os.path.basename(args.output))[0]

    if args.file == '-':
        module_name = ''
    
    tree = process_file(args.file)
    
    visitor = Compiler(module_name, main=args.main) 
    visitor.visit(tree)

    output_file = tempfile.NamedTemporaryFile(mode='w', delete=False)

    if args.stdout:
        print(visitor.output)

    with output_file as f:
        f.write(visitor.output)

    os.chmod(output_file.name, 0o755)

    if args.command == 'build' and not args.stdout:
        shutil.copy(output_file.name, args.output)
    else:
        subprocess.run([output_file.name], check=True)