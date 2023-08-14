# Volcano

Volcano is a new programming language that is a subset of Python, designed to be compiled to shell script. It provides a simple and intuitive syntax that allows you to write shell scripts in Python, without having to worry about the complexities of shell scripting.

## Installation

To install Volcano, you can use pip:

```
pip install volcano
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