# analysis/base_module.py

class BaseModule:

    name = "base"

    def analyze(self, context):
        raise NotImplementedError
