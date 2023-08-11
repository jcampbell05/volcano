import argparse

def cli():
    parser = argparse.ArgumentParser(description='Process a file.')
    parser.add_argument('file', type=str, help='path to the file')
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        contents = f.read()

    print(contents)

if __name__ == '__main__':
    cli()