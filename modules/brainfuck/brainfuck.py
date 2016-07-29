"""

Python interpreter for the esoteric language Brainfuck

More information: http://esolangs.org/wiki/Brainfuck

"""


from esoterpret.interpreter.baseclass import AbstractInterpreter
from collections import defaultdict
import sys, re

class BrainfuckInterpreter(AbstractInterpreter):
	def nextInstruction(self):
		print("N")
