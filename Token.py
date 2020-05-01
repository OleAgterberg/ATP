

class Token(object):
    def __init__(self, name : str, value : str) -> None:
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return "Token('%s', '%s')" % (self.name, self.value)
