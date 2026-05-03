from datetime import date, datetime

class Tree:
    def __init__(self):
        self.records = {}

    def get(self, link):
        return self.records.get(link)

    def add(self, record):
        self.records[record.link] = record
        return self.records[record.link]

    def get_corresponding_people(self, conditions):
        corresponding_people = []
        for record in self.records.values():
            if record.type == "person" and record.corresponds(conditions):
                corresponding_people.append(record)
        return corresponding_people

class Person:
    def __init__(self, link):
        self.link = link
        self.type = "person"
        self.looked = False

        self.full_name = None
        self.name = None
        self.surname = None
        self.husband_surname = None

        self.gender = None

        self.origin_family = None
        self.families = []

        self.birth_date = None
        self.birth_place = None

        self.death_date = None
        self.death_place = None
        self.death_reason = None
        self.burial_place = None

    def corresponds(self, conditions):
        print(self.gender, self.name)
        ret = True
        for condition in conditions:
            if condition[0] == "gender":
                ret = (ret and self.gender == condition[1])
            elif condition[0] == "birth_date":
                ret = (ret and self.birth_date != None and self.birth_date >= condition[1] and self.birth_date < condition[2])
            elif condition[0] == "alive":
                ret = (ret and self.death_date == None)
            elif condition[0] == "not alive":
                ret = (ret and self.death_date != None)
        return ret

class Family:
    def __init__(self, link):
        self.link = link
        self.type = "family"

        self.husband = None
        self.wife = None
        self.children = []

        self.marriage_date = None
        self.marriage_place = None

        self.divorced = False
        self.even = False
        self.even_reason = None
