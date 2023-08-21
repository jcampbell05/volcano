import volcano

@volcano.volcano
def my_script():
    from volcano.shell import ls
    print(ls())

my_script()