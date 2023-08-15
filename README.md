# Volcano

Volcano is a new programming language that is a subset of Python (Similar to MicroPython), designed to be compiled to shell script. It provides a simple and intuitive syntax that allows you to write shell scripts in Python, without having to worry about the complexities of shell scripting.

## Installation

To install Volcano, clone this repo and use pip from the directory:

```
pip install .
```

## Usage

To build your Volcano shell script, you can create a `.vol` file with your Volcano code, and then run the `volcano build` command with the path to your file. You should ned up with a shell script in the same directory as your code.

```
volcano build myscript.vol
```

To run it directly just use `run` instead.

```
volcano run myscript.vol
```

You can also use the `--help` option to see the available command-line options:

```
volcano --help
```

## Why use Volcano?

Volcano provides a number of benefits over traditional shell scripting:

- **Simplicity**: Volcano provides a simple and intuitive syntax that is easy to learn and use, even for beginners.

- **Pythonic**: Volcano is based on Python, so if you already know Python, you can easily write shell scripts in Volcano.

- **Portability**: Volcano scripts can be run on any system that has shell installed, without having to worry about the differences between different shell environments as long as implementations of `echo`, `bc`, `mktemp` and `tail` are avaliable.

## Roadmap

- **Keyword arguments**: Currently, Volcano does not support keyword arguments.
- **Classes and objects**: Volcano does not currently support classes and objects.
- **Lambdas**: We have no support for lambdas
- **List comprehension statements**: We have no support for list comprehension
- **Control flow statements**: Volcano currently only supports `for` loops and `if` statements.
- **Cmprison operartors**: Volcano currently does not support all comparisoon operators.
- **Async code**: Volcano currently does not support writing asynchronous code using the async and await keywords.
- **Piping**: Volcano currently does not support piping from shell scripting.
- **Generator**: Volcano currently does not support generators.
- **Standard library**: Volcano currently doesn't have an extensive standard library beyond `print`

Overall, our roadmap for Volcano is focused on adding support for the features of Python that are most important for writing complex and sophisticated programs. We believe that by adding support for these features, we can make Volcano a more powerful and flexible tool for shell scripting.