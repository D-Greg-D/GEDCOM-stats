from src.tree import Tree
from datetime import date, datetime

class GEDCOM_Parser:
    def __init__(self, config):
        self.file = "input/" + config["file"]
        self.developer_mode = config.get("developer_mode", False)
        self.tree_debug_mode = config.get("tree_debug_mode", True)
        self.lines = []
        self.line = 0
        self.level = 0
        self.type = ""
        self.payload = None

    def print_debug_information(self, type):
        if self.tree_debug_mode:
            if type == "odd_date":
                print(f"Некорректная форма даты найдена в строке {self.line}: \"{self.payload}\"")
        if self.developer_mode:
            if type == "odd_struct":
                print(f"Unexpected structure \"{self.type}\" of level {self.level} is found in line {self.line}.")
            if type == "odd_payload":
                print(f"Unexpected payload \"{self.payload}\" in a structure \"{self.type}\" of level {self.level} is found in line {self.line}.")

    def line_parser(self):
        self.level = int(self.lines[self.line][0])
        self.type = self.lines[self.line][1]
        self.payload = None
        if len(self.lines[self.line]) > 2:
            self.payload = self.lines[self.line][2]
        self.line = self.line + 1
        if self.type == "rin" or self.type == "_uid" or self.type == "_upd":
            return self.line_parser()
        return True

    def empty_while(self):
        while self.line_parser():
            if self.level < 1:
                self.line = self.line - 1
                break

    def get_date(self, input):
        try:
            return datetime.strptime(input, "%d %b %Y")
        except ValueError:
            try:
                return datetime.strptime(input, "%b %Y")
            except ValueError:
                try:
                    return datetime.strptime(input, "%Y")
                except ValueError:
                    try:
                        return datetime.strptime(input, "abt %Y")
                    except ValueError:
                        try:
                            return datetime.strptime(input, "приблизительно в %Y")
                        except ValueError:
                            self.print_debug_information("odd_date")
                            return None

    def go(self):
        with open(self.file) as ged:
            self.lines = [gedline.rstrip().lower().split(maxsplit=2) for gedline in ged]
            self.lines[0][0] = "0"

        tree = Tree()

        while self.line_parser():
            if self.type == "head" or self.type == "_publish":
                self.empty_while()
            elif self.type == "trlr":
                break
            elif self.type[0] == "@" and self.type[-1] == "@":
                if self.payload == "indi":
                    person = tree.add_person(self.type)

                    while self.line_parser():
                        if self.level < 1:
                            self.line = self.line - 1
                            break
                        elif self.type == "name":
                            person.full_name = self.payload

                            while self.line_parser():
                                if self.level < 2:
                                    self.line = self.line - 1
                                    break
                                elif self.type == "givn":
                                    person.name = self.payload
                                elif self.type == "surn":
                                    person.surname = self.payload
                                elif self.type == "_marnm":
                                    person.husband_surname = self.payload
                                else:
                                    self.print_debug_information("odd_struct")
                        elif self.type == "sex":
                            person.gender = self.payload
                        elif self.type == "famc":
                            person.origin_family = self.payload
                        elif self.type == "fams":
                            person.families.append(self.payload)
                        elif self.type == "birt":
                            while self.line_parser():
                                if self.level < 2:
                                    self.line = self.line - 1
                                    break
                                elif self.type == "date":
                                    person.birth_date = self.get_date(self.payload)
                                elif self.type == "plac":
                                    person.birth_place = self.payload
                                else:
                                    self.print_debug_information("odd_struct")
                        elif self.type == "deat":
                            while self.line_parser():
                                if self.level < 2:
                                    self.line = self.line - 1
                                    break
                                elif self.type == "date":
                                    person.death_date = self.get_date(self.payload)
                                elif self.type == "plac":
                                    person.death_place = self.payload
                                elif self.type == "caus":
                                    person.death_reason = self.payload
                                else:
                                    self.print_debug_information("odd_struct")
                        elif self.type == "buri":
                            while self.line_parser():
                                if self.level < 2:
                                    self.line = self.line - 1
                                    break
                                elif self.type == "plac":
                                    person.burial_place = self.payload
                                else:
                                    self.print_debug_information("odd_struct")
                        else:
                            self.print_debug_information("odd_struct")
                elif self.payload == "fam":
                    family = tree.add_family(self.type)

                    while self.line_parser():
                        if self.level < 1:
                            self.line = self.line - 1
                            break
                        elif self.type == "husb":
                            family.husband = self.payload
                        elif self.type == "wife":
                            family.wife = self.payload
                        elif self.type == "chil":
                            family.children.append(self.payload)
                        elif self.type == "div":
                            family.divorced = True
                        elif self.type == "even":
                            family.even = True
                            while self.line_parser():
                                if self.level < 2:
                                    self.line = self.line - 1
                                    break
                                elif self.type == "type":
                                    family.even_reason = self.payload
                                else:
                                    self.print_debug_information("odd_struct")
                        elif self.type == "marr":
                            while self.line_parser():
                                if self.level < 2:
                                    self.line = self.line - 1
                                    break
                                elif self.type == "date":
                                    family.marriage_date = self.get_date(self.payload)
                                elif self.type == "plac":
                                    family.marriage_place = self.payload
                                else:
                                    self.print_debug_information("odd_struct")
                        else:
                            self.print_debug_information("odd_struct")
                elif self.payload == "obje" or self.payload == "repo" or self.payload == "snote" or self.payload == "sour" or self.payload == "subm":
                    self.empty_while()
                else:
                    self.print_debug_information("odd_payload")
            else:
                self.print_debug_information("odd_struct")

        return tree
