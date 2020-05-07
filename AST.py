from typing import Callable, Union, Dict, Tuple

class Node(object):
    pass

class AST(Node):
    def __init__(self,
                 value: Union[str, int, None] = None,
                 name: Union[str, None] = None,
                 left: Union[Node, None] = None,
                 right: Union[Node, None] = None,
                 f: Callable[
                                [
                                    Union[Node, None],
                                    Union[Node, None],
                                    Dict[str, int]
                                ],
                                Tuple[
                                    Union[Node,None],
                                    Dict[str, int]
                                ]
                            ] = None
                 ) -> None:
        self.value = value
        self.name = name
        self.left = left
        self.right = right
        self.f = f

    # getValue :: Dict[str, int] -> (str_int_None -> Dict[str, int])
    def getValue(self, program: Dict[str, int]) -> Tuple[Union[str, int, None], Dict[str, int]]:
        value = (None, program)
        if self.f:
            value = self.f(self.left, self.right, program)
        elif self.value:
            value = (self.value, program)
        elif program[self.name]:
            value (program[self.name], program)
        return value # == value, program

    def __str__(self) -> str:
        string = 'AST : %s = %s \n' % (self.name, self.value)
        string += 'left -> %s ' % self.left.__str__() if self.left.__str__() != 'None' else ''
        string += 'right -> %s' % self.right.__str__() if self.right.__str__() != 'None' else ''
        return string


def add (   left: Union[Node, None],
            right: Union[Node, None],
            program: Dict[str, int]
            ) -> Tuple[Union[str, int, None], Dict[str, int]]:
    try:
        # just add the value of right to name in the program state of left.
        lValue, program = left.getValue(program)
        rValue, program = right.getValue(program)
        new_value = int(lValue) + int(rValue)
        program[left.right.name] = new_value
        return (new_value, program)
    except Exception as e:
        return (None, program)

def min (   left: Union[Node, None],
            right: Union[Node, None],
            program: Dict[str, int]
            ) -> Tuple[Union[str, int, None], Dict[str, int]]:
    try:
        # lValue, program
        lValue, program = left.getValue(program)
        rValue, program = right.getValue(program)
        new_value = int(lValue) - int(rValue)
        program[left.right.name] = new_value
        return (new_value, program)
    except Exception as e:
        return (None, program)


def assign (    left: Union[Node, None],
                right: Union[Node, None],
                program: Dict[str, int]
            ) -> Tuple[Union[str, int, None], Dict[str, int]]:
    try:
        rValue, program = right.getValue(program)
        name = left.name
        program[name] = rValue
        return (rValue, program)
    except Exception as e:
        return (None, program)


def my_print (  left: Union[Node, None],
                right: Union[Node, None],
                program: Dict[str, int]
            ) -> Tuple[Union[str, int, None], Dict[str, int]]:
    try:
        rValue, program = right.getValue(program)
        value = str(rValue)
        program['print'] = value
        return (right, program)
    except Exception as e:
        return (None, program)

def my_print_ln (   left: Union[Node, None],
                    right: Union[Node, None],
                    program: Dict[str, int]
            ) -> Tuple[Union[str, int, None], Dict[str, int]]:
    try:
        rValue, program = right.getValue(program)
        value = str(rValue)
        program['print'] = value + '\n'
        return (right, program)
    except Exception as e:
        return (None, program)

def not_equal ( left: Union[Node, None],
                right: Union[Node, None],
                program: Dict[str, int]
            ) -> Tuple[Union[str, int, None], Dict[str, int]]:
    try:
        lValue, program = left.getValue(program)
        rValue, program = right.getValue(program)
        if str(lValue) != str(rValue):
            program['if'] = 1 #yes
        return ('equal', program)
    except Exception as e:
        return (None, program)


def modus (     left: Union[Node, None],
                right: Union[Node, None],
                program: Dict[str, int]
            ) -> Tuple[Union[str, int, None], Dict[str, int]]:
    try:
        lValue, program = left.getValue(program)
        rValue, program = right.getValue(program)
        if int(lValue) % int(rValue) != 0:
            program['if'] = 1 #yes
        return ('modus', program)
    except Exception as e:
        return (None, program)


def my_input (     left: Union[Node, None],
                right: Union[Node, None],
                program: Dict[str, int]
            ) -> Tuple[Union[str, int, None], Dict[str, int]]:
    try:
        i = input()
        return (i, program)
    except Exception as e:
        return (None, program)


def call (      left: Union[Node, None],
                right: Union[Node, None],
                program: Dict[str, int]
            ) -> Tuple[Union[str, int, None], Dict[str, int]]:
    try:
        name = right.name
        value = program[name]
        return (value, program)
    except Exception as e:
        return (None, program)

def run_once (  left: Union[Node, None],
                right: Union[Node, None],
                program: Dict[str, int]
            ) -> Tuple[Union[str, int, None], Dict[str, int]]:
    try:
        program['run_once'] = 1
        return right.getValue(program)
    except Exception as e:
        return (None, program)


def end (  left: Union[Node, None],
                right: Union[Node, None],
                program: Dict[str, int]
            ) -> Tuple[Union[str, int, None], Dict[str, int]]:
    try:
        program['end'] = 1
        return ('end', program)
    except Exception as e:
        return (None, program)


def line_down (  left: Union[Node, None],
                right: Union[Node, None],
                program: Dict[str, int]
            ) -> Tuple[Union[str, int, None], Dict[str, int]]:
    try:
        program['line_down'] = 1
        return ('line_down', program)
    except Exception as e:
        return (None, program)
