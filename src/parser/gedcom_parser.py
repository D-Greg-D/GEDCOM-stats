from src.tree import Tree

class GEDCOM_Parser:
    def __init__(self, file):
        self.file = file
        self.lines = []
        self.line = 0
        self.level = 0
        self.type = ""
        self.payload = None
    
    def go(self):
        self.read()
        return self.create_tree()

    def print_odd_struct(self):
        print(f"Unexpected structure {self.type} of level {self.level} is found in line {self.line}.")

    def print_odd_payload(self):
        print(f"Unexpected payload {self.payload} in a structure {self.type} of level {self.level} is found in line {self.line}.")

    def line_parser(self):
        self.level = int(self.lines[self.line][0])
        self.type = self.lines[self.line][1]
        self.payback = None
        if len(self.lines[self.line]) > 2:
            self.payback = self.lines[self.line][2]
        self.line = self.line + 1
        if self.type == "rin" or self.type == "_uid" or self.type == "_upd":
            return self.line_parser()
        return True
    
    def empty_while(self):
        while self.line_parser():
            if self.level < 1:
                self.line = self.line - 1
                break

    def read(self):
        with open(self.file) as ged:
            self.lines = [gedline.rstrip().lower().split(maxsplit=2) for gedline in ged]
            self.lines[0][0] = "0"

    def create_tree(self):
        tree = Tree()

        while self.line_parser():
            if self.type == "head" or self.type == "_publish":
                self.empty_while()
            elif self.type == "trlr":
                break
            elif self.type[0] == "@" and self.type[-1] == "@":
                if self.payback == "indi":
                    person = tree.add_person(self.type)

                    while self.line_parser():
                        if self.level < 1:
                            self.line = self.line - 1
                            break
                        elif self.type == "name":
                            person.full_name = self.payback

                            while self.line_parser():
                                if self.level < 2:
                                    self.line = self.line - 1
                                    break
                                elif self.type == "givn":
                                    person.name = self.payback
                                elif self.type == "surn":
                                    person.surname = self.payback
                                elif self.type == "_marnm":
                                    person.husband_surname = self.payback
                                else:
                                    self.print_odd_struct()
                        elif self.type == "sex":
                            person.gender = self.payback
                        elif self.type == "famc":
                            person.origin_family = self.payback
                        elif self.type == "fams":
                            person.families.append(self.payback)
                        elif self.type == "birt":
                            while self.line_parser():
                                if self.level < 2:
                                    self.line = self.line - 1
                                    break
                                elif self.type == "date":
                                    person.birth_date = self.payback
                                elif self.type == "plac":
                                    person.birth_place = self.payback
                                else:
                                    self.print_odd_struct()
                        elif self.type == "deat":
                            while self.line_parser():
                                if self.level < 2:
                                    self.line = self.line - 1
                                    break
                                elif self.type == "date":
                                    person.death_date = self.payback
                                elif self.type == "plac":
                                    person.death_place = self.payback
                                elif self.type == "caus":
                                    person.death_reason = self.payback
                                else:
                                    self.print_odd_struct()
                        elif self.type == "buri":
                            while self.line_parser():
                                if self.level < 2:
                                    self.line = self.line - 1
                                    break
                                elif self.type == "plac":
                                    person.burial_place = self.payback
                                else:
                                    self.print_odd_struct()
                        else:
                            self.print_odd_struct()
                elif self.payback == "fam":
                    family = tree.add_family(self.type)

                    while self.line_parser():
                        if self.level < 1:
                            self.line = self.line - 1
                            break
                        elif self.type == "husb":
                            family.husband = self.payback
                        elif self.type == "wife":
                            family.wife = self.payback
                        elif self.type == "chil":
                            family.children.append(self.payback)
                        elif self.type == "div":
                            family.divorced = True
                        elif self.type == "even":
                            family.even = True
                            while self.line_parser():
                                if self.level < 2:
                                    self.line = self.line - 1
                                    break
                                elif self.type == "type":
                                    family.even_reason = self.payback
                                else:
                                    self.print_odd_struct()
                        elif self.type == "marr":
                            while self.line_parser():
                                if self.level < 2:
                                    self.line = self.line - 1
                                    break
                                elif self.type == "date":
                                    family.marriage_date = self.payback
                                elif self.type == "plac":
                                    family.marriage_place = self.payback
                                else:
                                    self.print_odd_struct()
                        else:
                            self.print_odd_struct()
                elif self.payback == "obje" or self.payback == "repo" or self.payback == "snote" or self.payback == "sour" or self.payback == "subm":
                    self.empty_while()
                else:
                    self.print_odd_payload()
            else:
                self.print_odd_struct()
        
        return tree
