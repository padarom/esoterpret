"""

Python interpreter for the esoteric language Mornington Crescent

More information: http://esolangs.org/wiki/Mornington_Crescent

"""

import re
from operator import and_,  inv

from esoterpret.interpreter.baseclass import AbstractInterpreter
from modules.morningtoncrescent.stations import stations, lines

def cannon_street(a, b):
    if type(a) == int and type(b) == int:
        if a == 0:
            return ""
        return b // a
    raise TypeError
def preston_road(a, b):
    if type(a) == int and type(b) == int:
        if a == 0:
            return ""
        return b % a
    return NotImplemented
def paddington(a, b):
    if type(a) != str:
        return NotImplemented
    return b + a
def gunnersbury(a, b):
    if isinstance(a, int):
        a, b = b, a
    if b < 0:
        raise RuntimeError("Cannot be negative")
    return a[:b]
def mile_end(a, b):
    if isinstance(a, int):
        a, b = b, a
    if b < 0:
        raise RuntimeError("Cannot be negative")
    return a[-b:]
BINARY_STATIONS = {
    "Upminster":int.__add__,
    "Chalfont & Latimer":int.__mul__,
    "Cannon Street": cannon_street,
    "Preston Road": preston_road,
    "Bounds Green": max,
    "Manor House": lambda a, b : ~(a | b),
    "Holland Park": and_,
    "Turnham Green": int.__rrshift__,
    "Stepney Green": int.__rlshift__,
    "Paddington": paddington,
    "Gunnersbury": gunnersbury,
    "Mile End": mile_end
}
def charing_cross(accum):
    if isinstance(accum, str):
        if accum:
            return ord(accum[0])
        else:
            return 0
    else:
        return chr(accum)
UNARY_STATIONS = {
    "Russell Square": lambda a:a**2,
    "Notting Hill Gate": inv,
    "Seven Sisters": lambda a:7,
    "Charing Cross": charing_cross,
    "Upney": str.upper,
    "Hounslow Central": str.lower,
    "Turnpike Lane": lambda s:s[::-1],
}

class MorningtonCrescentInterpreter(AbstractInterpreter):
    """
    Mornington Crescent Interpreter
    """

    def __init__(self, code, stdin, verbose = False):
        """
        Initialize a new interpreter.

        Arguments:
            code -- the code to execute as a string
            stdin -- file-like object to read initial accumulator from
            verbose -- whether to print out each step as it is executed
        """
        newcode = []
        for line in iter(code.splitlines()):
            pattern = re.compile("^Take (.*) Line to ([^#]*?)[\t ]*(#.*)?$")

            # Add only valid Lines to the code list, ignoring the rest.
            if pattern.match(line):
                newcode.append(line)
        super().__init__(newcode, stdin)

        self._verbose = verbose
        self.accumulator = self.input()

        self.station_values = {}
        # Initialize Station Values to their names
        for station in stations:
            self.station_values[station] = station
        self.location = "Mornington Crescent"
        self.jumpstack = []

    def has_execution_finished(self):
        if self.location == "Mornington Crescent" and self.instruction_pointer > 0:
            return True
        elif self.instruction_pointer >= len(self.code):
            raise RuntimeError("You have to end at Mornington Crescent.")

    @property
    def current_value(self):
        return self.station_values[self.location]
    @current_value.setter
    def current_value(self, value):
        self.station_values[self.location] = value
 
    def next_instruction(self):
        """Execute the next instruction as specified by InstructionPointer"""

        code    = self.code[self.instruction_pointer]
        pattern = re.compile("^Take (.*) Line to ([^#]*?)[\t ]*(#.*)?$")

        match       = pattern.match(code)
        line        = match.group(1)
        destination = match.group(2)

        self.validate_trip(destination, line)

        # Debug
        if self._verbose:
            print("[" + str(self.instruction_pointer) + "] " + code)
            print("Before: %r (%r)" % (self.accumulator, self.station_values[destination])))

        self.execute_station(destination)

        # Debug
        if self._verbose:
            print("After:  %r (%r)" % (self.accumulator, self.current_value))
            print()

        self.instruction_pointer += 1

    def validate_trip(self, destination, line):
        """
        Test if travel to a given station using a given line is allowed

        Arguments:
            destination -- the destination station
            line - the line to use
        """

        if line not in lines:
            raise RuntimeError("Line " + line + " doesn't exist.")
        elif destination not in stations:
            raise RuntimeError("Station " + destination + " doesn't exist.")
        elif line not in stations[self.location]:
            raise RuntimeError("Station " + self.location + " doesn't have access to " + line + " Line.")
        elif line not in stations[destination]:
            raise RuntimeError("Station " + destination + " doesn't have access to " + line + " Line.")
    def execute_station(self, station):
        """
        Executes the destination station's instruction

        Arguments:
            station -- The destination station
        """
        self.location = station

        # Check special stations that aren't implemented above
        # parse string to integer
        if station == "Parsons Green" and isinstance(self.accumulator, str):
            match = re.search("-?\d+", self.accumulator)
            new_value = 0 if not(match) else self.accumulator[match.end():]
            self.accumulator = 0 if not(match) else int(match.group())
            self.current_value = "" if not(match) else new_value
            return
        # store
        elif station == "Bank":
            # Set Hammersmith to the same value
            self.station_values["Hammersmith"] = self.accumulator

        # retain
        elif station == "Hammersmith":
            self.accumulator = self.current_value
            return

        # continuation
        elif station == "Temple":
            self.jumpstack.append(self.instruction_pointer)
            return

        # if
        elif station == "Angel":
            if self.accumulator != 0:
                self.location = "Temple"
                self.instruction_pointer = self.jumpstack[-1]
            return

        # pop
        elif station == "Marble Arch":
            del self.jumpstack[-1]
            return

        # output/exit
        elif station == "Mornington Crescent":
            self.output(self.accumulator)

        if station in UNARY_STATIONS:
            try:
                value = UNARY_STATIONS[station](self.current_value)
                if value != NotImplemented:
                    self.current_value = value
            except TypeError:
                pass
        elif station in BINARY_STATIONS:
            try:
                func = BINARY_STATIONS[station]
                value = func(self.accumulator, self.current_value)
                if value != NotImplemented:
                    self.current_value = value
            except TypeError:
                pass
        self.accumulator, self.current_value = self.current_value, self.accumulator
