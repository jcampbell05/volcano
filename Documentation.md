# Documentation

Volcano was made out of a frustration on the steep learning curve shell scripting can present,
to take one example "1=1" is not the same as "1 = 1" despite the fact that in modern programming
languages this would result in the same behaviour.

For many users they use shellscript primarily for it's portability, they are deploying in 
environments with limited space where they may not have access to any languages such as python.

Most attempts at solving this problem involve creating a new shell scripting syntax (Such as Cmake, 
Oil and Fish) which is removes the benefits of portability. Or a custom language which compiles
into shell but ends up abandoned since making a lanaguage from scratch is hard.

With Volcano we took a different approach. We took the robust foundation of python which has a battle tested syntax, built-in modules for parsing source code and is one of the most popular
programming languages so presents a low barrier to entry. 

Since python typically comes as standard on almost all unix like  operating systems we have been
able to build a compiler that can be run almost anywhere with zero additional dependencies.

## Implementation

This is a living document and will be updated as we update Volcano, this is a brief guide to how
we've implemented various language features in shellscript.

### Execution

Before we can generate any code we need to inform the shell how to run the file, for our scripts
we simply write a shabang header which indicates the code should be ran with the standard `sh
shell.

If for whatever reason this shell has been aliased to another shell which has non-standard POSIX
extensions such as bash, we also set that shell into POSIX mode to disable any non stanard 
behabviout using `set -o posix`. This also ensures during testing that our code is POSIX compiant.

The last thing we do before execution is enable error mode. Typically shellscripts will keep trying
to execute as much of the script as possible even if earlier commands have failed. Python on the
other hand will abort straight away so we use `set -e` to ensure the shell will do the same thing.

### Imports and Compiling

Volcano supports two types of files when importing and compiling code, Volcano python files `.vol` and `.vsh` Volcano-compatiable shell scripts written to follow volcano's calling converions. 

Imports will look for a file with either of those extensions in the Volcano python package or in the local file-system.

- For `.vol` files we pass it to the python parser and traverse the AST to emit shell code 
- For `.vsh` we inject the contents of the file into the compiled shell code, similar to how a traditional compiler 
would with object `.o` files

### The Runtime

Volcano automatically imports a runtime script which includes support funcrtions required to run the 
compiled shell script. This is located at `volcano/runtime.vsh`.

It includes implementations for the `print` and `input` methods for python.

### Shell Imports

Volcano currently assumes a reference to a symbol that wasn't defined in the script must come from
the shell envrionment. But Python tooling will higlight these as an error, so Volcano supports importing
these symbols from the module `volcano.shell` which will silence these errors. No additional code is
emitted into the shell script.

### Assignment

Assignments to variables are translated directly to shellscript:

`foo = "bar"` becomes `foo="bar"`

The compiler is able to intelligently determine if it needs to prevent shell's globbing behaivour by wrapping the value to be assigned in quites.

If a value needs to be read from a function then it will
capture it using the command subsitution (`$()`) automatically.

### Arithmtic

The compiler automatically handles passing any arithmtic
expressions to `awk` to be evaluated.

```
a = 1
b = 2
c = a + b
```

Will be translated to the following shellscript:

```
a=1
b=2
c=$( awk "BEGIN {print "$a"+"$b"}")
```

When using shorthand i.e `+=` or `-=`, the compiler knows
to add the original value of the variable to the `awk` 
expression so that `i += i` will become:

```
i=$( awk "BEGIN {print "$i"+1}")
```

### Joined Strings

When using joined strings in python, the compiler will 
automatically convert them to variable substitution.

Any placeholders which rely on the result of a function
will automatically be translated to use command substituion.

```
"Hello, {name}. today is {date()}"
```

Will become:

```
"Hello, $name. Today is $(date)"
```

### Control Flows

Control flows such as `if`, `while` and `for` are directly
trasnalted to their equivlenet syntax in shellscript.

The compiler automatically handles subsituting variables
and wraps them in quotes to avoid issues with the shell
globbing the content instead so that it behaves the same
as in Python.

```
if name > "Ken:
    pass
```

Becomes:

```
if [ "$name" = "Ken" ]
then
fi
```

We don't yet have support for `switch` or one-line `if` 
statments but these can easily be implemented by 
modifying our intermediate representation to convert them
into shell if statements.

`is` currently; does the same thing as `==` as we haven't
got an implemention of objests for the compiled code and
so there is no concept of unique copies of the same
value.

### Functions

The compiler automatically genertes the code needed to read
positional arguments off the stack - If the arguments have
a default then code is emitted to set them when a value
isn't provided.

All variables will be marked as local to simulate them
being locally scoped in python.

```
def hello(message="Hey"):
    print(message)
```

Will become:

```
hello () {
    RESULT=
    local message=${1:-Hey}
    print "$message"
}
```

At the start of this function we clear the RESULT environment
variable which is where we store the result of the function.

If modify that function to return the message instead of 
printing it, then we will get a statment at the end of the
function which returns the result to the calling function.

```
hello () {
    RESULT=
    local message=${1:-Hey}
    echo "$message"
}
```

User defined functions are expected to use the built-in 
`print` to log to the console since the standard `echo` call
will cause additional data to be returned to the calling 
function due to how shell works. 

The `print` file` handles writing the logs to a temporary file the
runtime automatically creates and spins a background job
to `tail` the content of the file so it shows in the consokle.

### List Comprehension

List comprehensions are automatically translated into their
equivlent for loop and if statement code at the intermediate
representation stage.

```
name = ["Beth", "Bob", "Gizmo"]
[print(f"Hello {name}") for name in names]
```

Will become:

```
list_comp() {
    name = ["Beth", "Bob", "Gizmo"]
    for name in $name:
        print(f"Hello {name}")
}
list_comp
```

The compiler wraps this genrated code as a function in
shellscript to allow for the reuslts to be returned
to other expressiosn `numbers=[i for 0 in range(10)]`

There is some additional runtime code emittedto allow us to 
collect the values generated by the iterator as an array, but
this is work in progressso so these details are skipped for
now.

### Try/Except

The compiler tries to use the `trap` functionality to
emit code that can handle exceptions. This feature is 
experimental and doesn't work. 

It isn't possible to capture specific errors as we don't
have a way of defining classes required for Exception
classes.

Try exceptions are re-structured in the intermediated 
representation stage before being emitted to shell script
by the compiler.

```
try:
    print("My code")
except:
    print("Exception)
else:
    print("Success")
finally:
    print("All done")
```

Will become

```
except () {
    print("Exception")
}

try () {
    print("My Code")
    print("Success")
}

trap "except "$?"" "ERR"
try
trap - ERR
print("All done")

```

Firstly we move all the code from the exception handler to
it's own function.

Then the code in the try block is moved to it's own function
including the code from the else block which should be
ran once it's completed succesfully.

Before calling the try function we tell shell to call the
except function in case of errors. Afterwards we tell shell
to stop calling the except function.

Finally we emit all the code from the finally block so that
it's executed in either case.

This feature is still experimental.

### Name Collision

Generated symbols will be namespaced to avoid collions
for example.

```
def hello():

    print("outer")

    def hello():
        print("inner")

    hello()

hello()
hello()
```

Will be transformed into the following code.

```
module_hello () { 

    print "outer"

    module_hello_hello () {
        print "inner"
    }

    module_hello_hello
}

module_hello
module_hello
```

Notcied how we prefix each function and it's call with
the name of the specific cope it is contained within.

This ensures all code behaves exactly as original python
code intended.