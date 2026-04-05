import sys
sys.dont_write_bytecode = True

# from src.tree import Tree
from src.parsers.config_parser import Config_Parser
from src.parsers.gedcom_parser import GEDCOM_Parser
from src.stats.stats import Stats

config = Config_Parser("config.json").go()
tree = GEDCOM_Parser(config["input"]).go()
Stats(config, tree).go()
