from typing import List, Union
import _ast

class stmt(_ast.AST):
    pass

class Script(_ast.AST):
    def __init__(self, statements: list[stmt] = []):
        self.statements = statements

class Shebang(stmt):

    def __init__(self, commands: 'Command'):
        self.commands = commands

class Command(_ast.AST):
    def __init__(self, comment_text: str):
        self.comment_text = comment_text

class Comment(_ast.AST):
    def __init__(self, name: str, args: list = []):
        self.name = name
        self.args = args