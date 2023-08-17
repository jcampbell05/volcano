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
behabviout using `set -o posix`.

The last thing we do before execution is enable error mode. Typically shellscripts will keep trying
to execute as much of the script as possible even if earlier commands have failed. Python on the
other hand will abort straight away so we use `set -e` to ensure the shell will do the same thing.

### The Runtime

### Imports

### Assignment

### Arithmtic

### Joined Strings

### Control Flows

### Functions

### List Comprehension

## Future Features

### Try/Except

### Async

### Generator