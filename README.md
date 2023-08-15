# Volcano

Volcano is a new programming language that is a subset of Python, designed to be compiled to shell script. It provides a simple and intuitive syntax that allows you to write shell scripts in Python, without having to worry about the complexities of shell scripting.

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

- **Portability**: Volcano scripts can be run on any system that has shell installed, without having to worry about the differences between different shell environments.

## Roadmap

- **Keyword arguments**: Currently, Volcano does not support keyword arguments.

- **Classes and objects**: Volcano does not currently support classes and objects, which are another fundamental building block of most programs. In the future, we plan to add support for classes and objects, which will allow you to write more complex and sophisticated programs in Volcano.

- **Control flow statements**: Volcano currently only supports `for` loops, but does not support other control flow statements like `if` statements, `while` loops, or `try`/`except` blocks. In the future, we plan to add support for these control flow statements, which will make it easier to write more complex programs in Volcano.

- **Python libraries**: Provide any replacement implementation for common python libraries like requests or os. This is a major limitation that we plan to address in the future.

- **Return statements**: Return statement support is still experimental.

- **List comprehension statements**: We have no support for list comprehension

- **Lambdas**: We have no support for lambdas

- **Primitive functions and comprison operartors**: Volcano currently does not support primitive functions like lower() for strings or comparisoon operators like > or <. This is a limitation that we plan to address in the future, which will make it easier to work with strings and other data types in Volcano.

- **Async code**: Volcano currently does not support writing asynchronous code using the async and await keywords. This is a limitation that we plan to address in the future, which will make it possible to write more efficient and responsive programs in Volcano.

- **Piping**: Volcano currently does not support piping from shell scripting. In the future, we plan to add support for piping, which will allow you to pipe commands together using a syntax like command.pipe(other_command)(args).

- **Optimizations**: We don't optimise the final shell code, So it may not be the best output since we don't reperesent it as an intenral IR yet.

- **Source maps**: We don't emit any comments in final code to be able to determine where the code was from

Overall, our roadmap for Volcano is focused on adding support for the features of Python that are most important for writing complex and sophisticated programs. We believe that by adding support for these features, we can make Volcano a more powerful and flexible tool for shell scripting.