from typing import List, Union
import _ast

class Script(_ast.AST):
    def __init__(self, statement: 'Statement'):
        self.statement = statement

class Statement(_ast.AST):

    def __init__(self, instructions: Union['Comment', 'Shebang'] = []):
        self.instructions = instructions

class Shebang(_ast.AST):

    def __init__(self, commands: 'Command'):
        self.commands = commands

class Command(_ast.AST):
    def __init__(self, comment_text: str):
        self.comment_text = comment_text

class Comment(_ast.AST):
    def __init__(self, comment_text: str):
        self.comment_text = comment_text