import json

class Config_Parser:
    def __init__(self, file):
        self.file = file

    def go(self):
        with open(self.file) as file:
            config = json.load(file)
            if config.get("input") == None or config["input"].get("file") == None:
                raise ValueError("There is no input file specified in config.json")
            return config
