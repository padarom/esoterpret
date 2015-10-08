#!/usr/local/bin/python

"""

Esoterpret main program
Usage: ./esoterpret.py --help

Repository: https://github.com/Padarom/Esoterpret

"""

class Interpreter:
	test = ""

import argparse, os, sys, imp

# Add current path to sys.path, so we can import modules
path = os.path.dirname(os.path.realpath(__file__))
#if path not in sys.path:
#	sys.path.insert(0, path)

import esoterpret.interactive as interactive
from esoterpret.language import Language

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="""
	Esoterpret, interpreter and debugger for esoteric programming languages""", 
		formatter_class=argparse.RawDescriptionHelpFormatter)

	parser.add_argument("-i", "--interactive", 
	                    help="open the interactive CLI interpreter/debugger",
	                    action="store_true")

	parser.add_argument("-l", "--language", 
	                    help="the language you want to execute")

	parser.add_argument("--list-languages", 
	                    help="list available languages",
	                    action="store_true")

	arguments = parser.parse_args()

	if arguments.interactive:
		cli = interactive.InteractiveCLI()
		cli.menu()
		cli.unset()

	elif arguments.list_languages:
		for item in os.listdir(path + "/modules"):
			if os.path.isdir(path + "/modules/" + item) and item != "__pycache__":
				try:
					language = Language(item)
					print("- %s (%s)" % (language.Config["name"], item))
				except:
					pass

	elif arguments.language is not None:
		try:
			language = Language(arguments.language)
			interpreter = language.Class("", "")

		except (ImportError):
			print("No Interpreter for " + arguments.language + " found.")
		except FileNotFoundError:
			print("Config file could not be loaded.")
