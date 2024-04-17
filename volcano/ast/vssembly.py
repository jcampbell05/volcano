from typing import List, Union
import _ast

# TODO: How do we implement piping 
#

class Script(_ast.AST):
    def __init__(self, body: List['Body']):
        self.body = body

class Body(_ast.AST):
    def __init__(self, instructions: Union['Text', 'Instruction', 'Label']):
        self.instructions = instructions

class Variable(_ast.AST):
    def __init__(self, name: str):
        self.name = name

class Value(_ast.AST):
    def __init__(self, value: str):
        self.value = value

class LabelReference(_ast.AST):
    def __init__(self, function_name: str):
        self.function_name = function_name

class Label(_ast.AST):
    def __init__(self, name: str, body: List['Body']):
        self.name = name
        self.body = body

class Instruction(_ast.AST):
    def __init__(self, output: 'Variable', arg1: Union['Variable', 'Value', 'LabelReference'], arg2: Union['Variable', 'Value', 'LabelReference']):
        self.output = output
        self.arg1 = arg1
        self.arg2 = arg2

class Text(_ast.AST):
    def __init__(self, value: str):
        self.value = value

class AddInstruction(Instruction):
    """Performs addition of two operands."""
    pass

class SubInstruction(Instruction):
    """Performs subtraction of two operands."""
    pass

class AndInstruction(Instruction):
    """Performs bitwise AND operation on two operands."""
    pass

class OrInstruction(Instruction):
    """Performs bitwise OR operation on two operands."""
    pass

class NotInstruction(Instruction):
    """Performs bitwise NOT operation on an operand."""
    pass

class BneInstruction(Instruction):
    """Branches to an instruction if two operands are not equal."""
    pass

class BeqInstruction(Instruction):
    """Branches to an instruction if two operands are equal."""
    pass

class CallInstruction(Instruction):
    """Calls instruction."""
    pass

class JumpInstruction(Instruction):
    """Unconditionally jumps to an instruction."""
    pass

class PipeInstruction(Instruction):
    """Handles executing pipe instruction"""
    pass

class LwInstruction(Instruction):
    """Loads a word from memory into a register."""
    pass

class SwInstruction(Instruction):
    """Stores a word from a register into memory."""
    pass

class SllInstruction(Instruction):
    """Performs a logical left shift on an operand."""
    pass

class SrlInstruction(Instruction):
    """Performs a logical right shift on an operand."""
    pass

class SltInstruction(Instruction):
    """Sets the destination register to 1 if the first operand is less than the second, 0 otherwise."""
    pass

