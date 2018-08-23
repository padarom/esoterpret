import sys
from abc import ABCMeta, abstractmethod

class AbstractInterpreter(metaclass=ABCMeta):
    instruction_pointer = 0

    def __init__(self, code, stdin):
        self.code = code
        self.stdin = stdin or sys.stdin

    def output(self, text, newline = True):
        if newline:
            print("%s" % text)
        else:
            print("%s" % text, end="")

    def input(self, character = False):
        if character:
            return self.stdin.read(1)
        else:
            return self.stdin.readline()

    @abstractmethod
    def next_instruction(self): pass

    @abstractmethod
    def has_execution_finished(self): pass

