import volcano

@volcano.volcano
def my_script():
    from volcano.shell import ls
    
    print('The files in the current directory are:\n')

    files = ls()
    count = 0

    for file in files:
        print(f"- {file}")
        count += 1

    print(f"\nTotal: {count} files")

my_script()