import json, sys, os, imp

path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class Language:
    _module = None

    Class = None
    Config = None

    def __init__(self, name):
        # Load config
        content = None
        with open(path + "/modules/" + name + "/config.json", "r") as config:
            content = config.read()

        config = json.loads(content)
        self.Config = config

        # Import the module
        modulePath = "%s/modules/%s/%s" % (path, name, config["basefile"])
        sys.path.insert(0, modulePath)
        self._module = imp.load_source(name, modulePath)
        self.Class = getattr(self._module, config["baseclass"])
