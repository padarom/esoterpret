#!/usr/local/bin/python
"""

Esoterpret main program
Usage: ./esoterpret.py --help

Repository: https://github.com/Padarom/Esoterpret

"""

import argparse, os, sys, inspect

from esoterpret.language import Language
from esoterpret.terminal import Color

# Add current path to sys.path, so we can import modules
path = os.path.dirname(os.path.realpath(__file__))

def listLanguages():
	for item in os.listdir(path + "/modules"):
		if os.path.isdir(path + "/modules/" + item) and item != "__pycache__":
			try:
				language = Language(item)
				print("- %s%s %s(%s)" % (Color.BOLD, language.Config["name"], Color.NORMAL, item))
			except:
				pass

def useLanguage(language, code, initialization, extra_args):
	try:
		lang = Language(language)
		extrakws, extrapos = parseExtra(extra_args, lang, language)
		interpreter = lang.Class(code, initialization,
					 *extrapos, **extrakws)
		while not(interpreter.hasExecutionFinished()):
			interpreter.nextInstruction()
	except ImportError:
		print("No Interpreter found for %s." % language)
	except FileNotFoundError:
		print("Config file for %s could not be loaded." % language)
def parseExtra(extra, langc, langname):
	sig = inspect.signature(langc.Class.__init__)
	Parameter = inspect.Parameter
	parser = argparse.ArgumentParser(description="""
	Esoterpret, interpreter and debugger for esoteric programming languages""" ,
	prog='esoterpret -l %s' %langname, add_help=False)
	skip_params = 3 # ignore the required arguments of "self", "code", "stdin"
	for param in sig.parameters.values():
		if skip_params and param.kind == Parameter.POSITIONAL_OR_KEYWORD:
			skip_params -= 1
		elif param.kind == Parameter.VAR_KEYWORD:
			# We don't know how to handle these
			continue
		elif param.kind == Parameter.VAR_POSITIONAL:
			parser.add_argument(param.name, nargs="*",dest="__VARARGS")
		else:
			default = param.default
			action = "store"
			required = False
			if default == Parameter.empty:
				required = True
			elif type(default) == bool:
				if default:
					action = "store_false"
				else:
					action = "store_true"
			parser.add_argument("--"+param.name,"-" + param.name[0],
					    action=action,default=default,
					    required=required)
	ns = parser.parse_args(extra)
	kwargs = ns.__dict__
	return kwargs, kwargs.pop("__VARARGS", [])

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="""
	Esoterpret, interpreter and debugger for esoteric programming languages""",
		formatter_class=argparse.RawDescriptionHelpFormatter)

	parser.add_argument("script",
	                    type=argparse.FileType("r"),
	                    nargs="?",
	                    help="script file to execute")
	parser.add_argument("--gui",
	                    help="open the gui [WIP]",
	                    action="store_true")

	parser.add_argument("--nogui",
	                    help="compatibility mode (deprecated)",
	                    action="store_true")

	parser.add_argument("-s", "--stdin",
	                    help="stdin values")

	parser.add_argument("-l", "--language",
	                    help="the language you want to execute")

	parser.add_argument("--list-languages",
	                    help="list available languages",
	                    action="store_true")

	arguments, extra = parser.parse_known_args()

	if arguments.list_languages:
		if extra:
			parser.error('unrecognized arguments: %s' % ' '.join(extra))
		listLanguages()

	elif arguments.language is not None and not arguments.gui:
		if arguments.script:
			code = arguments.script.read()
			initialization = ""
			if arguments.stdin:
				initialization = arguments.stdin
			arguments.script.close()
			useLanguage(arguments.language, code, initialization, extra)

	else:
		raise hell # unimplemented
