import importlib.util
import json
import os
import sys

path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class Language:

    def __init__(self, name):
        # Load config
        content = None
        directory = os.path.join(path, "modules", name)
        with open(os.path.join(directory, "config.json")) as config_file:
           config = json.loads(config_file.read())

        self.config = config

        # Import the module
        interpreter_file = os.path.join(directory, config["basefile"])
        spec = importlib.util.spec_from_file_location(name, interpreter_file)
        self._module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self._module)
        self.interpreter_class = getattr(self._module, config["baseclass"])
