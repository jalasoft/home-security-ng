import sys

class Parameters:

    @staticmethod
    def parse():
        arguments = sys.argv[1:]
        pairs = { ParameterPair(i.split("=")[0], i.split("=")[1]) for i in arguments }
        return Parameters(pairs)

    def __init__(self, params):
        self.params = params

    def has_param(self, key):
        matched = { i for i in self.params if i.name == key }
        return len(matched) > 0

    def param(self, key):
        matched = [ i for i in self.params if i.name == key ]
        if len(matched) == 0:
            raise Error("No parameter '" + key + "'.")

        if len(matched) > 1:
            raise Error("Too many parameters '" + key + "': " + len(matched) + ".")

        return matched[0]

    def __iter__(self):
        return iter(self.params)


class ParameterPair:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return "Parameter[" + self.name + "=" + self.value + "]"


if __name__ == "__main__":
    params = Parameters.parse();
    
    for p in params:
        print(p)
