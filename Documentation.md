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

Volcano supports two types of files when importing and compiling code, Volcano files `.vol` and `.vsh` Volcano-compatiable shell scripts. Imports will look for a file with either of those extensions in the
Volcano python package or in the local file-system.

- For `.vol` files we pass it to the python parser and traverse the AST to emit shell code 
- For `.vsh` we inject the contents of the file into the compiled shell code, similar to how a traditional
  compiler would with object `.o` files

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

The compiler is able to intelligently determine if it needs to prevent shell's globbing behaivour by
wrapping the value to be assigned in quites and if a value needs to be read from a function then
it will capture it using the $() syntax automatically.

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

### Control Flows

### Functions

### List Comprehension

## Future Features

### Try/Except

### Async

### Generator