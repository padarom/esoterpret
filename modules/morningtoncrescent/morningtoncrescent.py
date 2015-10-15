"""

Python interpreter for the esoteric language Mornington Crescent

More information: http://esolangs.org/wiki/Mornington_Crescent

"""

from esoterpret.interpreter.baseclass import AbstractInterpreter
import re

from modules.morningtoncrescent.defaults import Stations, Lines
from math import floor

class MorningtonCrescentInterpreter(AbstractInterpreter):
	"""
	Mornington Crescent Interpreter
	"""

	# Environment
	Accumulator = ""
	DataPointer = "Mornington Crescent";
	Jumpstack   = []
	StationValues = {}

	Code = []
	_verbose = False

	def __init__(self, code, acc, verbose = False):
		"""
		Initialize a new interpreter.

		Arguments:
			code -- the code to execute as a string
			acc -- initialization value for accumulator
		"""
		for line in iter(code.splitlines()):
			pattern = re.compile("^Take (.*) Line to (.*)$")

			# Add only valid Lines to the code list, ignoring the rest.
			if pattern.match(line):
				self.Code.append(line)

		self._verbose = verbose
		self.Accumulator = acc

		# Initialize Station Values to their names
		for station in Stations.keys():
			self.StationValues[station] = station

	def hasExecutionFinished(self):
		if self.InstructionPointer == len(self.Code) and self.DataPointer != "Mornington Crescent":
			raise RuntimeError("You have to end at Mornington Crescent.")

		return self.InstructionPointer > len(self.Code) or (self.InstructionPointer > 0 and self.DataPointer == "Mornington Crescent")

	def nextInstruction(self):
		"""Execute the next instruction as specified by InstructionPointer"""

		code    = self.Code[self.InstructionPointer]
		pattern = re.compile("^Take (.*) Line to (.*)$")

		match       = pattern.match(code)
		line        = match.group(1)
		destination = match.group(2)

		if self.areStationsConnected(self.DataPointer, destination, line):
			if destination not in Stations.keys():
				raise RuntimeError("Station " + destination + " doesn't exist.")

			# Debug
			if self._verbose:
				pa = "\"%s\"" % self.Accumulator if isinstance(self.Accumulator, str) else str(self.Accumulator)
				ps = "\"%s\"" % self.StationValues[destination] if isinstance(self.StationValues[destination], str) else str(self.StationValues[destination])
				print ("[" + str(self.InstructionPointer) + "] " + code)
				print ("Before: %s (%s)" % (pa, ps))

			self.executeStation(destination)

			# Debug
			if self._verbose:
				pa = "\"%s\"" % self.Accumulator if isinstance(self.Accumulator, str) else str(self.Accumulator)
				ps = "\"%s\"" % self.StationValues[destination] if isinstance(self.StationValues[destination], str) else str(self.StationValues[destination])
				print ("After:  %s (%s)" % (pa, ps))
				print ("")

		else:
			raise RuntimeError("Stations " + self.DataPointer + " and " + destination + " are not connected through " + line + " Line.")

		self.InstructionPointer += 1

	def areStationsConnected(self, origin, destination, line):
		"""
		Test if two Stations are connected to one another

		Arguments:
			origin -- the origin station
			destination -- the destination station
			line - the line to use
		"""

		if line not in Lines:
			raise RuntimeError("Line " + line + " doesn't exist.")

		if line not in Stations[origin]:
			raise RuntimeError("Station " + origin + " doesn't have access to " + line + " Line.")

		if line not in Stations[destination]:
			raise RuntimeError("Station " + destination + " doesn't have access to " + line + " Line.")

		return True

	def executeStation(self, station):
		"""
		Executes the destination station's instruction

		Arguments:
			station -- The destination station
		"""
		before = self.DataPointer
		self.DataPointer = station

		action = None
		performDefault = False

		# add
		if station == "Upminster":
			action = lambda a, b : a + b

		# multiplier
		elif station == "Chalfont & Latimer":
			action = lambda a, b : a * b
		
		# integer division
		elif station == "Cannon Street":
			action = lambda a, b : "" if b == 0 else int(floor(b / a))

		# remainder
		elif station == "Preston Road":
			action = lambda a, b : "" if b == 0 else b % a
		
		# max
		elif station == "Bounds Green":
			action = lambda a, b : max(a, b)
		
		# bitwise NOR
		elif station == "Manor House":
			action = lambda a, b : ~(a | b)

		# bitwise AND
		elif station == "Holland Park":
			action = lambda a, b : a & b

		# bitwise Shift-Right
		elif station == "Holland Park":
			action = lambda a, b : b if a == 0 else b >> a

		# bitwise Shift-Left
		elif station == "Stepney Green":
			action = lambda a, b : b if a == 0 else b << a

		# square
		elif station == "Russell Square":
			action = lambda a, b : b * b

		# bitwise NOT
		elif station == "Notting Hill Gate":
			if isinstance(self.StationValues[station], int):
				(self.Accumulator, self.StationValues[station]) = (~self.StationValues[station], self.Accumulator)
			else:
				performDefault = True

		# parse string to integer
		elif station == "Parsons Green":
			if isinstance(self.Accumulator, str):
				match = re.search("-?\d+", self.Accumulator)
				newStationValue = 0 if not(match) else self.Accumulator[match.end():]
				self.Accumulator = 0 if not(match) else int(match.group())
				self.StationValues[station] = "" if not(match) else newStationValue
			else:
				performDefault = True

		# 7
		elif station == "Seven Sisters":
			self.Accumulator = 7

		# character <> codepoint
		elif station == "Charing Cross":
			acc = self.Accumulator
			if isinstance(self.StationValues[station], str):
				self.Accumulator = ord(self.StationValues[station][0]) if len(self.StationValues[station]) > 0 else 0
			else:
				self.Accumulator = chr(self.StationValues[station]) 

			self.StationValues[station] = acc

		# string concatenation
		elif station == "Paddington":
			acc = self.Accumulator
			if isinstance(self.StationValues[station], str) and isinstance(self.Accumulator, str):
				self.Accumulator = self.StationValues[station] + self.Accumulator					
				self.StationValues[station] = acc
				self.StationValues[station] = acc
			else:
				self.swapValues(station)

		# left substring
		elif station == "Gunnersbury":
			acc = self.Accumulator
			if (isinstance(self.StationValues[station], str) and isinstance(self.Accumulator, str)) or (isinstance(self.StationValues[station], int) and isinstance(self.Accumulator, int)):
				self.swapValues(station)

			elif isinstance(self.StationValues[station], str) and isinstance(self.Accumulator, int):
				if self.Accumulator < 0:
					raise RuntimeError("Cannot be negative.")
				
				self.Accumulator = self.StationValues[station][:self.Accumulator]
				self.StationValues[station] = acc

			elif isinstance(self.StationValues[station], int) and isinstance(self.Accumulator, str):
				if self.StationValues[station] < 0:
					raise RuntimeError("Cannot be negative.")

				self.Accumulator = self.Accumulator[:self.StationValues[station]]
				self.StationValues[station] = acc

		# right substring
		elif station == "Mile End":
			acc = self.Accumulator
			if (isinstance(self.StationValues[station], str) and isinstance(self.Accumulator, str)) or (isinstance(self.StationValues[station], int) and isinstance(self.Accumulator, int)):
				performDefault = True

			elif isinstance(self.StationValues[station], str) and isinstance(self.Accumulator, int):
				if self.Accumulator < 0:
					raise RuntimeError("Cannot be negative.")
				self.Accumulator = self.StationValues[station][-self.Accumulator:]
				self.StationValues[station] = acc

			elif isinstance(self.StationValues[station], int) and isinstance(self.Accumulator, str):
				if self.StationValues[station] < 0:
					raise RuntimeError("Cannot be negative.")

				self.Accumulator = self.Accumulator[-self.StationValues[station]:]
				self.StationValues[station] = acc

		# upper-case
		elif station == "Upney":
			acc = self.Accumulator
			if isinstance(self.StationValues[station], str):
				self.Accumulator = self.StationValues[station].upper()
				self.StationValues[station] = acc
			else:
				performDefault = True

		# lower-case
		elif station == "Hounslow Central":
			acc = self.Accumulator
			if isinstance(self.StationValues[station], str):
				self.Accumulator = self.StationValues[station][::-1]
			else:
				performDefault = True

		# store
		elif station == "Bank":
			self.swapValues(station)
			# Set Hammersmith to the same value
			self.StationValues["Hammersmith"] = self.StationValues[station]

		# retain
		elif station == "Hammersmith":
			self.Accumulator = self.StationValues[station]

		# continuation
		elif station == "Temple":
			self.Jumpstack.append(self.InstructionPointer)

		# if
		elif station == "Angel":
			if not(isinstance(self.Accumulator, int) and self.Accumulator == 0):
				self.DataPointer = "Temple"
				last = self.Jumpstack.pop() # We don't want to pop it.
				self.Jumpstack.append(last) # So we store it again.
				self.InstructionPointer = last

		# pop
		elif station == "Marble Arch":
			last = self.Jumpstack.pop()

		# output/exit
		elif station == "Mornington Crescent":
			self.output(self.Accumulator)

		else:
			performDefault = True

		if action is not None:
			try:
				acc = self.Accumulator
				self.Accumulator = int(self.Accumulator)
				self.StationValues[station] = int(self.StationValues[station])

				self.Accumulator = action(self.Accumulator, self.StationValues[station])
				self.StationValues[station] = acc
			except (ValueError, TypeError):
				performDefault = True

		if performDefault:
			self.swapValues(station)

	def swapValues(self, station):
		"""Swaps the values of the Accumulator and the specified station"""
		self.Accumulator, self.StationValues[station] = self.StationValues[station], self.Accumulator
