from typing import Callable, Union
from Token import Token

class AST(object):
    def __init__(self, left):
        pass

    def run(self) -> Union[str, None]:
        return ''


class Variable(AST):
    def __init__(self, token : Token) -> None:
        self.identifier = token.name
        self.value = token.value

    def run(self) -> Union[str, None]:
        return self.value

    def __str__(self) -> str:
        return self.value


class Assign(AST):
    def __init__(self, left: Variable, right: Variable) -> None:
        self.left = left
        self.right = right

    def run(self) -> Union[str, None]:
        try:
            self.left.value = self.right.value
            return self.right.value
        except:
            return None

    def __str__(self) -> str:
        return "%s = %s" % (self.left.name, self.right)


class Add(AST):
    def __init__(self, left: Variable, right: Variable) -> None:
        self.left = left
        self.right = right

    def run(self) -> Union[str, None]:
        try:
            number = int(self.left.value) + int(self.right.value)
            return str(number)
        except:
            return None

    def __str__(self) -> str:
        return "%s + %s" % (self.left.name, self.right)


class Min(AST):
    def __init__(self, left: Variable, right: Variable) -> None:
        self.left = left
        self.right = right

    def run(self) -> Union[str, None]:
        try:
            number = int(self.left.value) + int(self.right.value)
            return str(number)
        except:
            return None

    def __str__(self) -> str:
        return "%s - %s" % (self.left.name, self.right)


class Print(AST):
    def __init__(self, variable: Variable) -> None:
        self.variable = variable

    def run(self) -> Union[str, None]:
        try:
            print(self.variable.value)
            return self.variable.value
        except:
            return None

    def __str__(self) -> str:
        return 'print %s' % self.variable


class Run_Once(AST):
    def __init__(self, instruction: AST) -> None:
        self.instruction = instruction

    def run(self) -> Union[str, None]:
        try:
            return self.instruction.run()
        except:
            return None

    def __str__(self) -> str:
        return str(instruction)

# , f: Callable[[Variable, Variable], Variable]
