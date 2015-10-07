#!/usr/local/bin/python

"""

Python interpreter for the esoteric language Mornington Crescent
Usage: ./mornington-crescent.py --help

More information: http://esolangs.org/wiki/Mornington_Crescent

"""

import sys, re
from collections import defaultdict

# TUBE LINE & STATION DATA
# Taken from https://gist.github.com/paulcuth/1111303
_StationString = """Acton Town [Piccadilly] [District]
Aldgate [Metropolitan] [Circle]
Aldgate East [Hammersmith & City] [District]
Alperton [Piccadilly]
Amersham [Metropolitan]
Angel [Northern]
Archway [Northern]
Arnos Grove [Piccadilly]
Arsenal [Piccadilly]
Baker Street [Hammersmith & City] [Circle] [Metropolitan] [Bakerloo] [Jubilee]
Balham [Northern]
Bank [Central] [Waterloo & City] [Northern] [District] [Circle]
Barbican [Hammersmith & City] [Circle] [Metropolitan]
Barking [Hammersmith & City] [District]
Barkingside [Central]
Barons Court [Piccadilly] [District]
Bayswater [Circle] [District]
Becontree [District]
Belsize Park [Northern]
Bermondsey [Jubilee]
Bethnal Green [Central]
Blackfriars [Circle] [District]
Blackhorse Road [Victoria]
Bond Street [Jubilee] [Central]
Borough [Northern]
Boston Manor [Piccadilly]
Bounds Green [Piccadilly]
Bow Road [Hammersmith & City] [District]
Brent Cross [Northern]
Brixton [Victoria]
Bromley-by-Bow [Hammersmith & City] [District]
Buckhurst Hill [Central]
Burnt Oak [Northern]
Caledonian Road [Piccadilly]
Camden Town [Northern]
Canada Water [Jubilee]
Canary Wharf [Jubilee]
Canning Town [Jubilee]
Cannon Street [Circle] [District]
Canons Park [Jubilee]
Chalfont & Latimer [Metropolitan]
Chalk Farm [Northern]
Chancery Lane [Central]
Charing Cross [Bakerloo] [Northern]
Chesham [Metropolitan]
Chigwell [Central]
Chiswick Park [District]
Chorleywood [Metropolitan]
Clapham Common [Northern]
Clapham North [Northern]
Clapham South [Northern]
Cockfosters [Piccadilly]
Colindale [Northern]
Colliers Wood [Northern]
Covent Garden [Piccadilly]
Croxley [Metropolitan]
Dagenham East [District]
Dagenham Heathway [District]
Debden [Central]
Dollis Hill [Jubilee]
Ealing Broadway [Central] [District]
Ealing Common [Piccadilly] [District]
Earl's Court [District] [Piccadilly]
East Acton [Central]
Eastcote [Metropolitan] [Piccadilly]
East Finchley [Northern]
East Ham [Hammersmith & City] [District]
East Putney [District]
Edgware [Northern]
Edgware Road [Hammersmith & City] [Circle] [District]
Edgware Road [Bakerloo]
Elephant & Castle [Bakerloo] [Northern]
Elm Park [District]
Embankment [Northern] [Bakerloo] [Circle] [District]
Epping [Central]
Euston [Northern] [Victoria]
Euston Square [Hammersmith & City] [Circle] [Metropolitan]
Fairlop [Central]
Farringdon [Hammersmith & City] [Circle] [Metropolitan]
Finchley Central [Northern]
Finchley Road [Metropolitan] [Jubilee]
Finsbury Park [Piccadilly] [Victoria]
Fulham Broadway [District]
Gants Hill [Central]
Gloucester Road [Piccadilly] [Circle] [District]
Golders Green [Northern]
Goldhawk Road [Hammersmith & City] [Circle]
Goodge Street [Northern]
Grange Hill [Central]
Great Portland Street [Hammersmith & City] [Circle] [Metropolitan]
Greenford [Central]
Green Park [Jubilee] [Victoria] [Piccadilly]
Gunnersbury [District]
Hainault [Central]
Hammersmith [Piccadilly] [District]
Hammersmith [Hammersmith & City] [Circle]
Hampstead [Northern]
Hanger Lane [Central]
Harlesden [Bakerloo]
Harrow & Wealdstone [Bakerloo]
Harrow-on-the-Hill [Metropolitan]
Hatton Cross [Piccadilly]
Heathrow Terminal 4 [Piccadilly]
Heathrow Terminal 5 [Piccadilly]
Heathrow Terminals 1, 2, 3 [Piccadilly]
Hendon Central [Northern]
High Barnet [Northern]
Highbury & Islington [Victoria]
Highgate [Northern]
High Street Kensington [Circle] [District]
Hillingdon [Metropolitan] [Piccadilly]
Holborn [Piccadilly] [Central]
Holland Park [Central]
Holloway Road [Piccadilly]
Hornchurch [District]
Hounslow Central [Piccadilly]
Hounslow East [Piccadilly]
Hounslow West [Piccadilly]
Hyde Park Corner [Piccadilly]
Ickenham [Metropolitan] [Piccadilly]
Kennington [Northern]
Kensal Green [Bakerloo]
Kensington [District]
Kentish Town [Northern]
Kenton [Bakerloo]
Kew Gardens [District]
Kilburn [Jubilee]
Kilburn Park [Bakerloo]
Kingsbury [Jubilee]
King's Cross St. Pancras [Victoria] [Piccadilly] [Northern] [Circle] [Hammersmith & City] [Metropolitan]
Knightsbridge [Piccadilly]
Ladbroke Grove [Hammersmith & City] [Circle]
Lambeth North [Bakerloo]
Lancaster Gate [Central]
Latimer Road [Hammersmith & City] [Circle]
Leicester Square [Northern] [Piccadilly]
Leyton [Central]
Leytonstone [Central]
Liverpool Street [Circle] [Hammersmith & City] [Metropolitan] [Central]
London Bridge [Northern] [Jubilee]
Loughton [Central]
Maida Vale [Bakerloo]
Manor House [Piccadilly]
Mansion House [Circle] [District]
Marble Arch [Central]
Marylebone [Bakerloo]
Mile End [Central] [Hammersmith & City] [District]
Mill Hill East [Northern]
Moorgate [Northern] [Hammersmith & City] [Circle] [Metropolitan]
Moor Park [Metropolitan]
Morden [Northern]
Mornington Crescent [Northern]
Neasden [Jubilee]
Newbury Park [Central]
North Acton [Central]
North Ealing [Piccadilly]
Northfields [Piccadilly]
North Greenwich [Jubilee]
North Harrow [Metropolitan]
Northolt [Central]
North Wembley [Bakerloo]
Northwick Park [Metropolitan]
Northwood [Metropolitan]
Northwood Hills [Metropolitan]
Notting Hill Gate [Circle] [District] [Central]
Oakwood [Piccadilly]
Old Street [Northern]
Osterley [Piccadilly]
Oval [Northern]
Oxford Circus [Bakerloo] [Victoria] [Central]
Paddington [Bakerloo] [Circle] [District]
Paddington [Circle] [Hammersmith & City]
Park Royal [Piccadilly]
Parsons Green [District]
Perivale [Central]
Piccadilly Circus [Bakerloo] [Piccadilly]
Pimlico [Victoria]
Pinner [Metropolitan]
Plaistow [Hammersmith & City] [District]
Preston Road [Metropolitan]
Putney Bridge [District]
Queensbury [Jubilee]
Queen's Park [Bakerloo]
Queensway [Central]
Ravenscourt Park [District]
Rayners Lane [Metropolitan] [Piccadilly]
Redbridge [Central]
Regent's Park [Bakerloo]
Richmond [District]
Rickmansworth [Metropolitan]
Roding Valley [Central]
Royal Oak [Circle] [Hammersmith & City]
Ruislip [Metropolitan] [Piccadilly]
Ruislip Gardens [Central]
Ruislip Manor [Metropolitan] [Piccadilly]
Russell Square [Piccadilly]
Seven Sisters [Victoria]
Shepherd's Bush [Central]
Shepherd's Bush Market [Circle] [Hammersmith & City]
Sloane Square [Circle] [District]
Snaresbrook [Central]
South Ealing [Piccadilly]
Southfields [District]
Southgate [Piccadilly]
South Harrow [Piccadilly]
South Kensington [Piccadilly] [Circle] [District]
South Kenton [Bakerloo]
South Ruislip [Central]
Southwark [Jubilee]
South Wimbledon [Northern]
South Woodford [Central]
Stamford Brook [District]
Stanmore [Jubilee]
Stepney Green [Hammersmith & City] [District]
St. James's Park [Circle] [District]
St. John's Wood [Jubilee]
Stockwell [Victoria] [Northern]
Stonebridge Park [Bakerloo]
St. Paul's [Central]
Stratford [Central]  [Jubilee]
Sudbury Hill [Piccadilly]
Sudbury Town [Piccadilly]
Swiss Cottage [Jubilee]
Temple [Circle] [District]
Theydon Bois [Central]
Tooting Bec [Northern]
Tooting Broadway [Northern]
Tottenham Court Road [Northern] [Central]
Tottenham Hale [Victoria]
Totteridge & Whetstone [Northern]
Tower Hill [Circle] [District]
Tufnell Park [Northern]
Turnham Green [District]
Turnpike Lane [Piccadilly]
Upminster [District]
Upminster Bridge [District]
Upney [District]
Upton Park [Hammersmith & City] [District]
Uxbridge [Metropolitan] [Piccadilly]
Vauxhall [Victoria]
Victoria [Victoria] [Circle] [District]
Walthamstow Central [Victoria]
Wanstead [Central]
Warren Street [Northern] [Victoria]
Warwick Avenue [Bakerloo]
Waterloo [Bakerloo] [Northern] [Waterloo & City] [Jubilee]
Watford [Metropolitan]
Wembley Central [Bakerloo]
Wembley Park [Metropolitan] [Jubilee]
West Acton [Central]
Westbourne Park [Circle] [Hammersmith & City]
West Brompton [District]
West Finchley [Northern]
West Ham [Jubilee] [Hammersmith & City] [District]
West Hampstead [Jubilee]
West Harrow [Metropolitan]
West Kensington [District]
Westminster [Circle] [District] [Jubilee]
West Ruislip [Central]
Whitechapel [Hammersmith & City] [District]
White City [Central]
Willesden Green [Jubilee]
Willesden Junction [Bakerloo]
Wimbledon [District]
Wimbledon Park [District]
Woodford [Central]
Wood Green [Piccadilly]
Wood Lane [Circle] [Hammersmith & City]
Woodside Park [Northern]"""
_lines = _StationString.split("\n")
_matches = map(lambda a: re.search("^([^\[\]]*?)\s*((\[[^\[\]]*\]\s*)*)$", a), _lines)

STATIONS = defaultdict(list)
LINES = set()


for match in _matches:
	for line in re.compile("\[([^\[\]]*)\]").findall(match.group(2)):
		STATIONS[match.group(1)].append(line)
		LINES.add(line)

class Interpreter:
	"""
	Mornington Crescent Interpreter
	"""

	# Environment
	Accumulator = ""
	DataPointer = "Mornington Crescent";
	Jumpstack   = []
	StationValues = {}

	Code = []
	_InstructionPointer = 0
	_verbose = False

	def __init__(self, code, acc, verbose):
		"""
		Initialize a new interpreter.

		Arguments:
			code -- the code to execute as a string
			acc -- initialization value for accumulator
		"""
		for line in iter(code.splitlines()):
			pattern = re.compile("^Take (.*) Line to (.*)$")

			# Add only valid lines to the code list, ignoring the rest.
			if pattern.match(line):
				self.Code.append(line)

		self._verbose = verbose
		self.Accumulator = acc

		# Initialize Station Values to their names
		for station in STATIONS.keys():
			self.StationValues[station] = station

		while self._InstructionPointer < len(self.Code):
			self.move()

	def move(self):
		"""Execute the next instruction as specified by _InstructionPointer"""

		code    = self.Code[self._InstructionPointer]
		pattern = re.compile("^Take (.*) Line to (.*)$")

		match       = pattern.match(code)
		line        = match.group(1)
		destination = match.group(2)

		if self.areStationsConnected(self.DataPointer, destination, line):
			if destination not in STATIONS.keys():
				raise RuntimeError("Station " + destination + " doesn't exist.")

			if self._verbose:
				print ("[" + str(self._InstructionPointer) + "] " + code)

			self.executeStation(destination)

		else:
			raise RuntimeError("Stations " + self.DataPointer + " and " + destination + " are not connected through " + line + " Line.")

		self._InstructionPointer += 1

		# RuntimeError if the instruction pointer is bigger than the number of lines
		if self._InstructionPointer == len(self.Code):
			raise RuntimeError("You have to end at Mornington Crescent.")

	def areStationsConnected(self, origin, destination, line):
		"""
		Test if two stations are connected to one another

		Arguments:
			origin -- the origin station
			destination -- the destination station
			line - the line to use
		"""

		if line not in LINES:
			raise RuntimeError("Line " + line + " doesn't exist.")

		if origin not in STATIONS.keys():
			raise RuntimeError("Station " + origin + " doesn't have access to " + line + " Line.")

		if destination not in STATIONS.keys():
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

		# Debug
		if self._verbose:
			print ("Before: " + str(self.Accumulator) + " (" + str(self.StationValues[station]) + ")")

		# add
		if station == "Upminster":
			action = lambda a, b : a + b

		# multiplier
		elif station == "Chalfont & Latimer":
			action = lambda a, b : a * b
		
		# integer division
		elif station == "Cannon Street":
			action = lambda a, b : "" if b == 0 else int(round(b / a))

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
				action = lambda a, b : ~b
			else:
				performDefault = True

		# parse string to integer
		elif station == "Parsons Green":
			match = re.search("-?\d+", self.Accumulator)
			station = self.Accumulator[match.end():]
			self.Accumulator = 0 if not(match) else match.group()
			self.StationValues[station] = "" if not(match) else station

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
			self.Jumpstack.append(self._InstructionPointer)

		# if
		elif station == "Angel":
			if not(isinstance(self.Accumulator, int) and self.Accumulator == 0):
				self.DataPointer = "Temple"
				last = self.Jumpstack.pop() # We don't want to pop it.
				self.Jumpstack.append(last) # So we store it again.
				self._InstructionPointer = last

		# pop
		elif station == "Marble Arch":
			last = self.Jumpstack.pop()

		# output/exit
		elif station == "Mornington Crescent":
			print(self.Accumulator)
			sys.exit()

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

		# Debug
		if self._verbose:
			print ("After:  " + str(self.Accumulator) + " (" + str(self.StationValues[station]) + ")")
			print ("")

	def swapValues(self, station):
		"""Swaps the values of the Accumulator and the specified station"""
		self.Accumulator, self.StationValues[station] = self.StationValues[station], self.Accumulator

if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description="""
	Execute a Mornington Crescent script.

	Executing a script is as easy as:
		%(prog)s <script file>""",
	formatter_class=argparse.RawDescriptionHelpFormatter)
	
	parser.add_argument("script",
	                    type=argparse.FileType("r"),
	                    nargs="?",
	                    help=".mcresc file to execute")

	# Still not ideal, according to the specification it requires the accumulator to come from stdin.
	# But it'll do for now.
	parser.add_argument("-a", "--accumulator", 
	                   	help="the value to initialize the accumulator to",
	                   	default="")

	parser.add_argument("-v", "--verbose", 
	                    help="increase output verbosity",
	                    action="store_true")

	arguments = parser.parse_args()

	if arguments.script:
		code = arguments.script.read()
		arguments.script.close()
		interpreter = Interpreter(code, arguments.accumulator, arguments.verbose)
	else:
		print("You need to provide a path to your program!")
