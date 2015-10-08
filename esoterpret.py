#!/usr/local/bin/python

"""

Esoterpret main program
Usage: ./esoterpret.py --help

Repository: https://github.com/Padarom/Esoterpret

"""

class Interpreter:
	test = ""

import argparse, os, sys, importlib, json
import esoterpret.interactive as interactive

# Add current path to sys.path, so we can import modules
path = os.path.abspath(".")
if path not in sys.path:
	sys.path.insert(0, path)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="""
	Esoterpret, interpreter and debugger for esoteric programming languages""", 
		formatter_class=argparse.RawDescriptionHelpFormatter)

	parser.add_argument("-i", "--interactive", 
	                    help="open the interactive CLI interpreter/debugger",
	                    action="store_true")

	parser.add_argument("-l", "--language", 
	                    help="the language you want to execute")

	arguments = parser.parse_args()

	if arguments.interactive:
		cli = interactive.InteractiveCLI()
		cli.menu()
		cli.unset()

	if arguments.language is not None:
		try:
			# Load config
			content = None
			with open("modules/" + arguments.language + ".json", "r") as config:
				content = config.read()

			config = json.loads(content)
			
			# Import the module
			mc = importlib.import_module('modules.' + arguments.language)
			# Get the class
			class_ = getattr(mc, config["baseclass"])
			# Initialize the class
			interpreter = class_("Take Northern Line to Bank", "")

		except (ImportError, FileNotFoundError):
			print("No Interpreter for " + arguments.language + " found.")
		except json.decoder.JSONDecodeError:
			print("The config file for " + arguments.language + " is not a valid JSON.")
