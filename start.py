import sys
sys.dont_write_bytecode = True
# from src.tree import Tree
from src.parser.gedcom_parser import GEDCOM_Parser

tree = GEDCOM_Parser("input/VenusMirror27.03.2025-21063.ged").go()
people_number = 0
families_number = 0
for record in tree.records.values():
    if record.type == "person":
        people_number += 1
    elif record.type == "family":
        families_number += 1
print(f"Людей в дереве: {people_number}\nСемей в дереве: {families_number}")