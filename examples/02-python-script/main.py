import volcano

@volcano.volcano
def list_files():
    from volcano.shell import ls
    
    print('The files in the current directory are:\n')

    files = ls()
    count = 0

    for file in files:
        print(f"- {file}")
        count += 1

    print(f"\nTotal: {count} files")

if __name__ == '__main__':
    list_files()