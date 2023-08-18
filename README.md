# Volcano 🌋

Volcano is a new programming language that is a subset of Python (Similar to MicroPython), designed to be compiled to shell script. It provides a simple and intuitive syntax that allows you to write shell scripts in Python, without having to worry about the complexities of shell syntax.

## Why use Volcano?

Volcano provides a number of benefits over traditional shell scripting:

- **Pythonic**: Volcano is based on Python, so if you already know Python, you can easily write shell scripts in Volcano.
- **Portability**: Volcano scripts can be run on any system that has shell installed, without having to worry about the differences between different shell environments as long as it's POSIX compiant.

Write using the syntax you know and love.

```
def lets_go():
    print("Lets get this party started")

lets_go()
```

But get shell code you know can work where
you need.

```
lets_go () {
    print "Lets get this party started"
}

lets_go
```

## Installation

To install Volcano, clone this repo and use pip from the directory:

```
python setup.py install
```

## Usage

To build your Volcano shell script, you can create a `.vol` file with your Volcano code, and then run the `volcano build` command with the path to your file. You should end up with a shell script in the same directory as your code.

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

## Roadmap

- **Async code**: Volcano currently does not support writing asynchronous code using the async and await keywords.
- **Generator**: Volcano currently does not support generators
- **Type methods**: Volcano currently does not support any of the low level methods such as tolower for string
- **Classes and objects**: Volcano does not currently support classes and objects.
- **Keyword arguments and star args**: Currently, Volcano does not support keyword arguments or references to *args or **kwargs.
- **Context Manager**: Volcano currently does not support context managers
- **Lambdas**: We have no support for lambdas
- **Piping**: Volcano currently does not support piping from shell scripting.

Any PRs implementhing these are welcome, you can read more on how Volcano is implemented in Documentation.md

Overall, our roadmap for Volcano is focused on adding support for the features of Python that are most important for writing complex and sophisticated programs. We believe that by adding support for these features, we can make Volcano a more powerful and flexible tool for shell scripting.