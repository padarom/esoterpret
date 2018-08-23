import sys
from abc import ABCMeta, abstractmethod

class AbstractInterpreter(metaclass=ABCMeta):
    InstructionPointer = 0
    Code = None

    def __init__(self, code, stdin):
        self.Code = code
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
    def nextInstruction(self): pass

    @abstractmethod
    def hasExecutionFinished(self): pass

