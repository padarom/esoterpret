#!/usr/local/bin/python

"""

Esoterpret main program
Usage: ./esoterpret.py --help

Repository: https://github.com/Padarom/Esoterpret

"""

class Interpreter:
	test = ""

# Initialize Curses
import argparse
import esoterpret.interactive as interactive

cli = interactive.InteractiveCLI()
cli.menu()

cli.unset()