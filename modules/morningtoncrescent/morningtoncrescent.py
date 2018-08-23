"""

Python interpreter for the esoteric language Mornington Crescent

More information: http://esolangs.org/wiki/Mornington_Crescent

"""

import re
from esoterpret.interpreter.baseclass import AbstractInterpreter
from modules.morningtoncrescent.stations import stations, lines

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
            print ("[" + str(self.instruction_pointer) + "] " + code)
            print ("Before: %s (%s)" % (repr(self.accumulator), repr(self.station_values[destination])))

        self.execute_station(destination)

        # Debug
        if self._verbose:
            print ("After:  %s (%s)" % (repr(self.accumulator), repr(self.station_values[self.location])))
            print ("")

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
            action = lambda a, b : "" if a == 0 else b // a

        # remainder
        elif station == "Preston Road":
            action = lambda a, b : "" if a == 0 else b % a
        
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
        elif station == "Turnham Green":
            action = lambda a, b : b if a == 0 else b >> a

        # bitwise Shift-Left
        elif station == "Stepney Green":
            action = lambda a, b : b if a == 0 else b << a

        # square
        elif station == "Russell Square":
            if isinstance(self.station_values[station], int):
                self.accumulator, self.station_values[station] = self.station_values[station] ** 2, self.accumulator
            else:
                performDefault = True

        # bitwise NOT
        elif station == "Notting Hill Gate":
            if isinstance(self.station_values[station], int):
                self.accumulator, self.station_values[station] = ~self.station_values[station], self.accumulator
            else:
                performDefault = True

        # parse string to integer
        elif station == "Parsons Green":
            if isinstance(self.accumulator, str):
                match = re.search("-?\d+", self.accumulator)
                new_value = 0 if not(match) else self.accumulator[match.end():]
                self.accumulator = 0 if not(match) else int(match.group())
                self.station_values[station] = "" if not(match) else new_value
            else:
                performDefault = True

        # 7
        elif station == "Seven Sisters":
            self.accumulator = 7

        # character <> codepoint
        elif station == "Charing Cross":
            acc = self.accumulator
            if isinstance(self.station_values[station], str):
                self.accumulator = ord(self.station_values[station][0]) if self.station_values[station] else 0
            else:
                self.accumulator = chr(self.station_values[station])

            self.station_values[station] = acc

        # string concatenation
        elif station == "Paddington":
            acc = self.accumulator
            if isinstance(self.station_values[station], str) and isinstance(self.accumulator, str):
                self.accumulator = self.station_values[station] + self.accumulator
                self.station_values[station] = acc
            else:
                performDefault = True

        # left substring
        elif station == "Gunnersbury":
            acc = self.accumulator
            if type(self.station_values[station]) == type(self.accumulator):
                performDefault = True
            elif isinstance(self.station_values[station], str):
                if self.accumulator < 0:
                    raise RuntimeError("Cannot be negative.")
                
                self.accumulator = self.station_values[station][:self.accumulator]
                self.station_values[station] = acc

            else:
                if self.station_values[station] < 0:
                    raise RuntimeError("Cannot be negative.")

                self.accumulator = self.accumulator[:self.station_values[station]]
                self.station_values[station] = acc

        # right substring
        elif station == "Mile End":
            acc = self.accumulator
            if type(self.station_values[station]) == type(self.accumulator):
                performDefault = True
            elif isinstance(self.station_values[station], str):
                if self.accumulator < 0:
                    raise RuntimeError("Cannot be negative.")

                self.accumulator = self.station_values[station][-self.accumulator:]
                self.station_values[station] = acc

            else:
                if self.station_values[station] < 0:
                    raise RuntimeError("Cannot be negative.")

                self.accumulator = self.accumulator[-self.station_values[station]:]
                self.station_values[station] = acc

        # upper-case
        elif station == "Upney":
            acc = self.accumulator
            if isinstance(self.station_values[station], str):
                self.accumulator = self.station_values[station].upper()
                self.station_values[station] = acc
            else:
                performDefault = True

        # lower-case
        elif station == "Hounslow Central":
            acc = self.accumulator
            if isinstance(self.station_values[station], str):
                self.accumulator = self.station_values[station].lower()
                self.station_values[station] = acc
            else:
                performDefault = True

        # reverse string
        elif station == "Turnpike Lane":
            acc = self.accumulator
            if isinstance(self.station_values[station], str):
                self.accumulator = self.station_values[station][::-1]
            else:
                performDefault = True

        # store
        elif station == "Bank":
            # Set Hammersmith to the same value
            self.station_values["Hammersmith"] = self.accumulator
            performDefault = True

        # retain
        elif station == "Hammersmith":
            self.accumulator = self.station_values[station]

        # continuation
        elif station == "Temple":
            self.jumpstack.append(self.instruction_pointer)

        # if
        elif station == "Angel":
            if self.accumulator != 0:
                self.location = "Temple"
                self.instruction_pointer = self.jumpstack[-1]

        # pop
        elif station == "Marble Arch":
            del self.jumpstack[-1]

        # output/exit
        elif station == "Mornington Crescent":
            self.output(self.accumulator)

        else:
            performDefault = True

        if action is not None:
            if isinstance(self.accumulator, int) and isinstance(self.station_values[station], int):
                acc = self.accumulator
                self.accumulator = action(acc, self.station_values[station])
                self.station_values[station] = acc
            else:
                performDefault = True
        if performDefault:
            self.accumulator, self.station_values[station] = self.station_values[station], self.accumulator
