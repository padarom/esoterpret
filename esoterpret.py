#!/usr/local/bin/python
"""

Esoterpret main program
Usage: ./esoterpret.py --help

Repository: https://github.com/Padarom/Esoterpret

"""

import argparse
import inspect
import io
import os
import sys

from esoterpret.language import Language
from esoterpret.terminal import Color

# Add current path to sys.path, so we can import modules
path = os.path.dirname(os.path.realpath(__file__))

def list_languages():
    modules_dir = os.path.join(path, "modules")
    for item in os.listdir(modules_dir):
        if os.path.isdir(os.path.join(modules_dir, item)) and item != "__pycache__":
            try:
                language = Language(item)
                print("- %s%s %s(%s)" % (Color.BOLD, language.config["name"], Color.NORMAL, item))
            except:
                pass

def use_language(language, code, stdin, extra_args):
    try:
        lang = Language(language)
        extrakws, extrapos = parse_extra_args(extra_args, lang, language)
        interpreter = lang.interpreter_class(code, stdin, *extrapos, **extrakws)
        while not(interpreter.has_execution_finished()):
            interpreter.next_instruction()
    except ImportError:
        print("No Interpreter found for %s." % language)
    except FileNotFoundError:
        print("Config file for %s could not be loaded." % language)
def parse_extra_args(extra, langc, langname):
    sig = inspect.signature(langc.interpreter_class.__init__)
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
            parser.add_argument("--" + param.name,
                        "-" + param.name[0],
                        action=action,
                        default=default,
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

    parser.add_argument("--nogui",
                        help=argparse.SUPPRESS,
                        action="store_true")

    parser.add_argument("-s", "--stdin",
                        help="stdin values",
                        type=io.StringIO,
                        default=sys.stdin)

    exclusive = parser.add_mutually_exclusive_group(required=True)

    exclusive.add_argument("--list-languages",
                        help="list available languages",
                        action="store_true")
    
    exclusive.add_argument("-l", "--language",
                        help="the language you want to execute")

    exclusive.add_argument("--gui",
                        help="open the gui [WIP]",
                        action="store_true")

    arguments, extra = parser.parse_known_args()
    
    if arguments.gui:
        parser.error("GUI not currently implemented")
    elif arguments.list_languages:
        if arguments.script or arguments.stdin != sys.stdin or extra:
            parser.error("extra arguments given with --list-languages")
        list_languages()
    else:
        if arguments.script:
            code = arguments.script.read()
            arguments.script.close()
            use_language(arguments.language, code,
                         arguments.stdin, extra)
        else:
            parser.error("no file to execute specified")
