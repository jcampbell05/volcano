from typing import List, Union
import _ast

class Script(_ast.AST):
    def __init__(self, statement: 'Statement'):
        self.statement = statement

class Statement(_ast.AST):

    def __init__(self, instructions: Union['Comment', 'Shebang'] = []):
        self.instructions = instructions

class Comment(_ast.AST):
    def __init__(self, comment_text: str):
        self.comment_text = comment_text

class Shebang(_ast.AST):
    def __init__(self, shebang_text: str):
        self.shebang_text = shebang_text