#!/usr/local/bin/python

"""

Python interpreter for the esoteric language Mornington Crescent
Usage: ./mornington-crescent.py --help

More information: http://esolangs.org/wiki/Mornington_Crescent

"""

import sys, re

# TUBE LINE & STATION DATA
# Taken from https://gist.github.com/paulcuth/1111303
LINES = {
	'B': 'Bakerloo', 'C': 'Central', 'D': 'District', 'H': 'Hammersmith', 'I': 'Circle', 'J': 'Jubilee', 
	'M': 'Metropolitan', 'N': 'Northern', 'P': 'Piccadilly', 'V': 'Victoria', 'W': 'Waterloo & City'
}

STATIONS = {
	"BST": "Baker Street",
	"CHX": "Charing Cross",
	"ERB": "Edgware Road (Bakerloo)",
	"ELE": "Elephant and Castle",
	"EMB": "Embankment",
	"HSD": "Harlesden",
	"HAW": "Harrow and Wealdstone",
	"KGN": "Kensal Green",
	"KNT": "Kenton",
	"KPK": "Kilburn Park",
	"LAM": "Lambeth North",
	"MDV": "Maida Vale",
	"MYB": "Marylebone",
	"NWM": "North Wembley",
	"OXC": "Oxford Circus",
	"PAD": "Paddington",
	"PIC": "Piccadilly Circus",
	"QPK": "Queen's Park",
	"RPK": "Regent's Park",
	"SKT": "South Kenton",
	"SPK": "Stonebridge Park",
	"WAR": "Warwick Avenue",
	"WLO": "Waterloo",
	"WEM": "Wembley Central",
	"WJN": "Willesden Junction",
	"BNK": "Bank",
	"BDE": "Barkingside",
	"BNG": "Bethnal Green",
	"BDS": "Bond Street",
	"BHL": "Buckhurst Hill",
	"CYL": "Chancery Lane",
	"CHG": "Chigwell",
	"DEB": "Debden",
	"EBY": "Ealing Broadway",
	"EAC": "East Acton",
	"EPP": "Epping",
	"FLP": "Fairlop",
	"GHL": "Gants Hill",
	"GRH": "Grange Hill",
	"GFD": "Greenford",
	"HAI": "Hainault",
	"HLN": "Hanger Lane",
	"HOL": "Holborn",
	"HPK": "Holland Park",
	"LAN": "Lancaster Gate",
	"LEY": "Leyton",
	"LYS": "Leytonstone",
	"LST": "Liverpool Street",
	"LTN": "Loughton",
	"MAR": "Marble Arch",
	"MLE": "Mile End",
	"NEP": "Newbury Park",
	"NAC": "North Acton",
	"NHT": "Northolt",
	"NHG": "Notting Hill Gate",
	"PER": "Perivale",
	"QWY": "Queensway",
	"RED": "Redbridge",
	"ROD": "Roding Valley",
	"RUG": "Ruislip Gardens",
	"SBC": "Shepherd's Bush",
	"SNB": "Snaresbrook",
	"SRP": "South Ruislip",
	"SWF": "South Woodford",
	"STP": "St Paul's",
	"SFD": "Stratford",
	"THB": "Theydon Bois",
	"TCR": "Tottenham Court Road",
	"WAN": "Wanstead",
	"WAC": "West Acton",
	"WRP": "West Ruislip",
	"WCT": "White City",
	"WFD": "Woodford",
	"ACT": "Acton Town",
	"ALE": "Aldgate East",
	"BKG": "Barking",
	"BCT": "Barons Court",
	"BEC": "Becontree",
	"BLF": "Blackfriars",
	"BWR": "Bow Road",
	"BBB": "Bromley-by-Bow",
	"CST": "Cannon Street",
	"CHP": "Chiswick Park",
	"DGE": "Dagenham East",
	"DGH": "Dagenham Heathway",
	"ECM": "Ealing Common",
	"ECT": "Earl's Court",
	"EHM": "East Ham",
	"EPY": "East Putney",
	"ERD": "Edgware Road (H & C)",
	"EPK": "Elm Park",
	"FBY": "Fulham Broadway",
	"GRD": "Gloucester Road",
	"GUN": "Gunnersbury",
	"HMD": "Hammersmith (District and Picc)",
	"HST": "High Street Kensington",
	"HCH": "Hornchurch",
	"OLY": "Kensington (Olympia)",
	"KEW": "Kew Gardens",
	"MAN": "Mansion House",
	"MON": "Monument",
	"PGR": "Parsons Green",
	"PLW": "Plaistow",
	"PUT": "Putney Bridge",
	"RCP": "Ravenscourt Park",
	"RMD": "Richmond",
	"SSQ": "Sloane Square",
	"SKN": "South Kensington",
	"SFS": "Southfields",
	"SJP": "St. James's Park",
	"STB": "Stamford Brook",
	"STG": "Stepney Green",
	"TEM": "Temple",
	"THL": "Tower Hill",
	"TGR": "Turnham Green",
	"UPM": "Upminster",
	"UPB": "Upminster Bridge",
	"UPY": "Upney",
	"UPK": "Upton Park",
	"VIC": "Victoria",
	"WBT": "West Brompton",
	"WHM": "West Ham",
	"WKN": "West Kensington",
	"WMS": "Westminster",
	"WCL": "Whitechapel",
	"WDN": "Wimbledon",
	"WMP": "Wimbledon Park",
	"ALD": "Aldgate",
	"BAR": "Barbican",
	"ESQ": "Euston Square",
	"FAR": "Farringdon",
	"GPS": "Great Portland Street",
	"HMS": "Hammersmith",
	"KXX": "King's Cross St Pancras",
	"MGT": "Moorgate",
	"BER": "Bermondsey",
	"CWR": "Canada Water",
	"CWF": "Canary Wharf",
	"CNT": "Canning Town",
	"CPK": "Canons Park",
	"DHL": "Dollis Hill",
	"FRD": "Finchley Road",
	"GPK": "Green Park",
	"KIL": "Kilburn",
	"KBY": "Kingsbury",
	"LON": "London Bridge",
	"NEA": "Neasden",
	"NGW": "North Greenwich",
	"QBY": "Queensbury",
	"SWK": "Southwark",
	"SJW": "St John's Wood",
	"STA": "Stanmore",
	"SWC": "Swiss Cottage",
	"WPK": "Wembley Park",
	"WHD": "West Hampstead",
	"WLG": "Willesden Green",
	"AME": "Amersham",
	"CLF": "Chalfont & Latimer",
	"CWD": "Chorleywood",
	"CLW": "Colliers Wood",
	"CRX": "Croxley",
	"ETE": "Eastcote",
	"HOH": "Harrow on the Hill",
	"HDN": "Hillingdon",
	"ICK": "Ickenham",
	"MPK": "Moor Park",
	"NHR": "North Harrow",
	"NWP": "Northwick Park",
	"NWD": "Northwood",
	"NWH": "Northwood Hills",
	"PIN": "Pinner",
	"RLN": "Rayners Lane",
	"RKY": "Rickmansworth",
	"RUI": "Ruislip",
	"RUM": "Ruislip Manor",
	"UXB": "Uxbridge",
	"WAT": "Watford",
	"WHR": "West Harrow",
	"ANG": "Angel",
	"ARC": "Archway",
	"BAL": "Balham",
	"BPK": "Belsize Park",
	"BOR": "Borough",
	"BTX": "Brent Cross",
	"BUR": "Burnt Oak",
	"CTN": "Camden Town",
	"CHF": "Chalk Farm",
	"CPC": "Clapham Common",
	"CPN": "Clapham North",
	"CPS": "Clapham South",
	"COL": "Colindale",
	"EFY": "East Finchley",
	"EDG": "Edgware",
	"EUS": "Euston",
	"FYC": "Finchley Central",
	"GGR": "Golders Green",
	"GST": "Goodge Street",
	"HMP": "Hampstead",
	"HND": "Hendon Central",
	"HBT": "High Barnet",
	"HIG": "Highgate",
	"KEN": "Kennington",
	"KTN": "Kentish Town",
	"LSQ": "Leicester Square",
	"MHE": "Mill Hill East",
	"MOR": "Morden",
	"MCR": "Mornington Crescent",
	"OLD": "Old Street",
	"OVL": "Oval",
	"SWM": "South Wimbledon",
	"STK": "Stockwell",
	"TBE": "Tooting Bec",
	"TBY": "Tooting Broadway",
	"TOT": "Totteridge and Whetstone",
	"TPK": "Tufnell Park",
	"WST": "Warren Street",
	"WFY": "West Finchley",
	"WSP": "Woodside Park",
	"ALP": "Alperton",
	"AGR": "Arnos Grove",
	"ARL": "Arsenal",
	"BOS": "Boston Manor",
	"BGR": "Bounds Green",
	"CRD": "Caledonian Road",
	"CFS": "Cockfosters",
	"COV": "Covent Garden",
	"FPK": "Finsbury Park",
	"HTX": "Hatton Cross",
	"HTF": "Heathrow Terminal 4",
	"HRV": "Heathrow Terminal 5",
	"HRC": "Heathrow Terminals 1, 2, 3",
	"HRD": "Holloway Road",
	"HNC": "Hounslow Central",
	"HNE": "Hounslow East",
	"HNW": "Hounslow West",
	"HPC": "Hyde Park Corner",
	"KNB": "Knightsbridge",
	"MNR": "Manor House",
	"NEL": "North Ealing",
	"NFD": "Northfields",
	"OAK": "Oakwood",
	"OST": "Osterley",
	"PRY": "Park Royal",
	"RSQ": "Russell Square",
	"SEL": "South Ealing",
	"SHR": "South Harrow",
	"SGT": "Southgate",
	"SHL": "Sudbury Hill",
	"STN": "Sudbury Town",
	"TPL": "Turnpike Lane",
	"WGN": "Wood Green",
	"BHR": "Blackhorse Road",
	"BRX": "Brixton",
	"HBY": "Highbury and Islington",
	"PIM": "Pimlico",
	"SVS": "Seven Sisters",
	"TTH": "Tottenham Hale",
	"VUX": "Vauxhall",
	"WAL": "Walthamstow Central",
	"WDL": "Wood Lane",
	"PRE": "Preston Road",
}

LINES_AT_STATION = {	
	"BST": ["B", "H", "J", "M"],
	"CHX": ["B", "N"],
	"ERB": ["B"],
	"ELE": ["B", "N"],
	"EMB": ["B", "D", "H", "N", "I"],
	"HSD": ["B"],
	"HAW": ["B"],
	"KGN": ["B"],
	"KNT": ["B"],
	"KPK": ["B"],
	"LAM": ["B"],
	"MDV": ["B"],
	"MYB": ["B"],
	"NWM": ["B"],
	"OXC": ["B", "C", "V"],
	"PAD": ["B", "H", "D", "I"],
	"PIC": ["B", "P"],
	"QPK": ["B"],
	"RPK": ["B"],
	"SKT": ["B"],
	"SPK": ["B"],
	"WAR": ["B"],
	"WLO": ["B", "J", "N", "W"],
	"WEM": ["B"],
	"WJN": ["B"],
	"BNK": ["C", "N", "W", "D", "I"],
	"BDE": ["C"],
	"BNG": ["C"],
	"BDS": ["C", "J"],
	"BHL": ["C"],
	"CYL": ["C"],
	"CHG": ["C"],
	"DEB": ["C"],
	"EBY": ["C", "D"],
	"EAC": ["C"],
	"EPP": ["C"],
	"FLP": ["C"],
	"GHL": ["C"],
	"GRH": ["C"],
	"GFD": ["C"],
	"HAI": ["C"],
	"HLN": ["C"],
	"HOL": ["C", "P"],
	"HPK": ["C"],
	"LAN": ["C"],
	"LEY": ["C"],
	"LYS": ["C"],
	"LST": ["C", "H", "M"],
	"LTN": ["C"],
	"MAR": ["C"],
	"MLE": ["C", "D", "H"],
	"NEP": ["C"],
	"NAC": ["C"],
	"NHT": ["C"],
	"NHG": ["C", "D", "I"],
	"PER": ["C"],
	"QWY": ["C"],
	"RED": ["C"],
	"ROD": ["C"],
	"RUG": ["C"],
	"SBC": ["C"],
	"SNB": ["C"],
	"SRP": ["C"],
	"SWF": ["C"],
	"STP": ["C"],
	"SFD": ["C", "J"],
	"THB": ["C"],
	"TCR": ["C", "N"],
	"WAN": ["C"],
	"WAC": ["C"],
	"WRP": ["C"],
	"WCT": ["C"],
	"WFD": ["C"],
	"ACT": ["D", "P"],
	"ALE": ["D", "H"],
	"BKG": ["D", "H"],
	"BCT": ["D", "P"],
	"BEC": ["D"],
	"BLF": ["D", "H"],
	"BWR": ["D", "H"],
	"BBB": ["D", "H"],
	"CST": ["D", "H", "I"],
	"CHP": ["D"],
	"DGE": ["D"],
	"DGH": ["D"],
	"ECM": ["D", "P"],
	"ECT": ["D", "P"],
	"EHM": ["D", "H"],
	"EPY": ["D"],
	"ERD": ["D", "H"],
	"EPK": ["D"],
	"FBY": ["D"],
	"GRD": ["D", "H", "P"],
	"GUN": ["D"],
	"HMD": ["D", "P"],
	"HST": ["D", "H"],
	"HCH": ["D"],
	"OLY": ["D"],
	"KEW": ["D"],
	"MAN": ["D", "H"],
	"MON": ["D", "H"],
	"PGR": ["D"],
	"PLW": ["D", "H"],
	"PUT": ["D"],
	"RCP": ["D"],
	"RMD": ["D"],
	"SSQ": ["D", "H"],
	"SKN": ["D", "H", "P"],
	"SFS": ["D"],
	"SJP": ["D", "H"],
	"STB": ["D"],
	"STG": ["D", "H"],
	"TEM": ["D", "H", "I"],
	"THL": ["D", "H"],
	"TGR": ["D", "P"],
	"UPM": ["D"],
	"UPB": ["D"],
	"UPY": ["D"],
	"UPK": ["D", "H"],
	"VIC": ["D", "H", "V", "I"],
	"WBT": ["D"],
	"WHM": ["D", "H", "J"],
	"WKN": ["D"],
	"WMS": ["D", "H", "J"],
	"WCL": ["D", "H"],
	"WDN": ["D"],
	"WMP": ["D"],
	"ALD": ["H", "M", "I"],
	"BAR": ["H", "M"],
	"ESQ": ["H", "M"],
	"FAR": ["H", "M"],
	"GPS": ["H", "M"],
	"HMS": ["H", "D", "I", "P"],
	"KXX": ["H", "M", "N", "P", "V"],
	"MGT": ["H", "M", "N", "I"],
	"BER": ["J"],
	"CWR": ["J"],
	"CWF": ["J"],
	"CNT": ["J"],
	"CPK": ["J"],
	"DHL": ["J"],
	"FRD": ["J", "M"],
	"GPK": ["J", "P", "V"],
	"KIL": ["J"],
	"KBY": ["J"],
	"LON": ["J", "N"],
	"NEA": ["J"],
	"NGW": ["J"],
	"QBY": ["J"],
	"SWK": ["J"],
	"SJW": ["J"],
	"STA": ["J"],
	"SWC": ["J"],
	"WPK": ["J", "M"],
	"WHD": ["J"],
	"WLG": ["J"],
	"AME": ["M"],
	"CLF": ["M"],
	"CWD": ["M"],
	"CLW": ["M", "N"],
	"CRX": ["M"],
	"ETE": ["M", "P"],
	"HOH": ["M"],
	"HDN": ["M", "P"],
	"ICK": ["M", "P"],
	"MPK": ["M"],
	"NHR": ["M"],
	"NWP": ["M"],
	"NWD": ["M"],
	"NWH": ["M"],
	"PIN": ["M"],
	"RLN": ["M", "P"],
	"RKY": ["M"],
	"RUI": ["M", "P"],
	"RUM": ["M", "P"],
	"UXB": ["M", "P"],
	"WAT": ["M"],
	"WHR": ["M"],
	"ANG": ["N"],
	"ARC": ["N"],
	"BAL": ["N"],
	"BPK": ["N"],
	"BOR": ["N"],
	"BTX": ["N"],
	"BUR": ["N"],
	"CTN": ["N"],
	"CHF": ["N"],
	"CPC": ["N"],
	"CPN": ["N"],
	"CPS": ["N"],
	"COL": ["N"],
	"EFY": ["N"],
	"EDG": ["N"],
	"EUS": ["N", "V"],
	"FYC": ["N"],
	"GGR": ["N"],
	"GST": ["N"],
	"HMP": ["N"],
	"HND": ["N"],
	"HBT": ["N"],
	"HIG": ["N"],
	"KEN": ["N"],
	"KTN": ["N"],
	"LSQ": ["N", "P"],
	"MHE": ["N"],
	"MOR": ["N"],
	"MCR": ["N"],
	"OLD": ["N"],
	"OVL": ["N"],
	"SWM": ["N"],
	"STK": ["N", "V"],
	"TBE": ["N"],
	"TBY": ["N"],
	"TOT": ["N"],
	"TPK": ["N"],
	"WST": ["N", "V"],
	"WFY": ["N"],
	"WSP": ["N"],
	"ALP": ["P"],
	"AGR": ["P"],
	"ARL": ["P"],
	"BOS": ["P"],
	"BGR": ["P"],
	"CRD": ["P"],
	"CFS": ["P"],
	"COV": ["P"],
	"FPK": ["P", "V"],
	"HTX": ["P"],
	"HTF": ["P"],
	"HRV": ["P"],
	"HRC": ["P"],
	"HRD": ["P"],
	"HNC": ["P"],
	"HNE": ["P"],
	"HNW": ["P"],
	"HPC": ["P"],
	"KNB": ["P"],
	"MNR": ["P"],
	"NEL": ["P"],
	"NFD": ["P"],
	"OAK": ["P"],
	"OST": ["P"],
	"PRY": ["P"],
	"RSQ": ["P"],
	"SEL": ["P"],
	"SHR": ["P"],
	"SGT": ["P"],
	"SHL": ["P"],
	"STN": ["P"],
	"TPL": ["P"],
	"WGN": ["P"],
	"BHR": ["V"],
	"BRX": ["V"],
	"HBY": ["V"],
	"PIM": ["V"],
	"SVS": ["V"],
	"TTH": ["V"],
	"VUX": ["V"],
	"WAL": ["V"],
	"WDL": ["I", "H", "D"],
	"PRE": ["M"],
}

def getLineAbbreviation(line):
	"""Returns the abbreviation of a specified line, or None if it doesn't exist"""
	for abbreviation, name in LINES.items():
		if name == line:
			return abbreviation

	return None

def getStationAbbreviation(station):
	"""Returns the abbreviation of a specified station, or None if it doesn't exist"""
	for abbreviation, name in STATIONS.items():
		if name == station:
			return abbreviation

	return None

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
		for station in STATIONS:
			self.StationValues[station] = STATIONS[station]

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
			# Find the abbreviation of a station
			abbreviation = getStationAbbreviation(destination)

			if abbreviation is None:
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

		# Identify the line
		lineAbbreviation        = getLineAbbreviation(line)
		originAbbreviation      = getStationAbbreviation(origin)
		destinationAbbreviation = getStationAbbreviation(destination)

		if lineAbbreviation is None:
			raise RuntimeError("Line " + line + " doesn't exist.")

		if lineAbbreviation not in LINES_AT_STATION[originAbbreviation]:
			raise RuntimeError("Station " + origin + " doesn't have access to " + line + " Line.")

		if lineAbbreviation not in LINES_AT_STATION[destinationAbbreviation]:
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
		abbreviation = getStationAbbreviation(station)

		action = None
		performDefault = False

		# Debug
		if self._verbose:
			print ("Before: " + str(self.Accumulator) + " (" + str(self.StationValues[abbreviation]) + ")")

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
			if isinstance(self.StationValues[abbreviation], int):
				action = lambda a, b : ~b
			else:
				performDefault = True

		# parse string to integer
		elif station == "Parsons Green":
			match = re.search("-?\d+", self.Accumulator)
			station = self.Accumulator[match.end():]
			self.Accumulator = 0 if not(match) else match.group()
			self.StationValues[abbreviation] = "" if not(match) else station

		# 7
		elif station == "Seven Sisters":
			self.Accumulator = 7

		# character <> codepoint
		elif station == "Charing Cross":
			acc = self.Accumulator
			if isinstance(self.StationValues[abbreviation], str):
				self.Accumulator = ord(self.StationValues[abbreviation][0]) if len(self.StationValues[abbreviation]) > 0 else 0
			else:
				self.Accumulator = chr(self.StationValues[abbreviation]) 

			self.StationValues[abbreviation] = acc

		# string concatenation
		elif station == "Paddington":
			acc = self.Accumulator
			if isinstance(self.StationValues[abbreviation], str) and isinstance(self.Accumulator, str):
				self.Accumulator = self.StationValues[abbreviation] + self.Accumulator					
				self.StationValues[abbreviation] = acc
				self.StationValues[abbreviation] = acc
			else:
				self.swapValues(abbreviation)

		# left substring
		elif station == "Gunnersbury":
			acc = self.Accumulator
			if (isinstance(self.StationValues[abbreviation], str) and isinstance(self.Accumulator, str)) or (isinstance(self.StationValues[abbreviation], int) and isinstance(self.Accumulator, int)):
				self.swapValues(abbreviation)

			elif isinstance(self.StationValues[abbreviation], str) and isinstance(self.Accumulator, int):
				if self.Accumulator < 0:
					raise RuntimeError("Cannot be negative.")
				
				self.Accumulator = self.StationValues[abbreviation][:self.Accumulator]
				self.StationValues[abbreviation] = acc

			elif isinstance(self.StationValues[abbreviation], int) and isinstance(self.Accumulator, str):
				if self.StationValues[abbreviation] < 0:
					raise RuntimeError("Cannot be negative.")

				self.Accumulator = self.Accumulator[:self.StationValues[abbreviation]]
				self.StationValues[abbreviation] = acc

		# right substring
		elif station == "Mile End":
			acc = self.Accumulator
			if (isinstance(self.StationValues[abbreviation], str) and isinstance(self.Accumulator, str)) or (isinstance(self.StationValues[abbreviation], int) and isinstance(self.Accumulator, int)):
				performDefault = True

			elif isinstance(self.StationValues[abbreviation], str) and isinstance(self.Accumulator, int):
				if self.Accumulator < 0:
					raise RuntimeError("Cannot be negative.")
				self.Accumulator = self.StationValues[abbreviation][-self.Accumulator:]
				self.StationValues[abbreviation] = acc

			elif isinstance(self.StationValues[abbreviation], int) and isinstance(self.Accumulator, str):
				if self.StationValues[abbreviation] < 0:
					raise RuntimeError("Cannot be negative.")

				self.Accumulator = self.Accumulator[-self.StationValues[abbreviation]:]
				self.StationValues[abbreviation] = acc

		# upper-case
		elif station == "Upney":
			acc = self.Accumulator
			if isinstance(self.StationValues[abbreviation], str):
				self.Accumulator = self.StationValues[abbreviation].upper()
				self.StationValues[abbreviation] = acc
			else:
				performDefault = True

		# lower-case
		elif station == "Hounslow Central":
			acc = self.Accumulator
			if isinstance(self.StationValues[abbreviation], str):
				self.Accumulator = self.StationValues[abbreviation][::-1]
			else:
				performDefault = True

		# store
		elif station == "Bank":
			self.swapValues(abbreviation)
			# Set Hammersmith to the same value
			self.StationValues["HMS"] = self.StationValues[abbreviation]

		# retain
		elif station == "Hammersmith":
			self.Accumulator = self.StationValues[abbreviation]

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
				self.StationValues[abbreviation] = int(self.StationValues[abbreviation])

				self.Accumulator = action(self.Accumulator, self.StationValues[abbreviation])
				self.StationValues[abbreviation] = acc
			except (ValueError, TypeError):
				performDefault = True

		if performDefault:
			self.swapValues(abbreviation)

		# Debug
		if self._verbose:
			print ("After:  " + str(self.Accumulator) + " (" + str(self.StationValues[abbreviation]) + ")")
			print ("")

	def swapValues(self, abbreviation):
		"""Swaps the values of the Accumulator and the station with the specified abbreviation"""
		self.Accumulator, self.StationValues[abbreviation] = self.StationValues[abbreviation], self.Accumulator

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
