from abc import ABCMeta, abstractmethod
from sys import stdin

class AbstractInterpreter(metaclass=ABCMeta):
	InstructionPointer = 0
	Code = None

	def __init__(self, code, defaults = None):
		self.Code = code

	def output(self, text, newline = True):
		if newline:
			print("%s" % text)
		else:
			print("%s" % text, end="")

	def input(self, character = False):
		if character:
			return stdin.read(1)
		else:
			return stdin.readline()

	@abstractmethod
	def nextInstruction(self): pass

	@abstractmethod
	def hasExecutionFinished(self): pass