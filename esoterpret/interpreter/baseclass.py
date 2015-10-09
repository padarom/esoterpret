from abc import ABCMeta, abstractmethod

class AbstractInterpreter(metaclass=ABCMeta):
	InstructionPointer = 0
	Code = None

	def __init__(self, code, defaults = None):
		self.Code = code

	@abstractmethod
	def nextInstruction(self): pass

	@abstractmethod
	def hasExecutionFinished(self): pass