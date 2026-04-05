class Tree:
    def __init__(self):
        self.records = {}

    def get(self, link):
        return records.get(link)

    class Record:
        def __init__(self, type, link):
            self.type = type
            self.link = link

    def add_person(self, link):
        self.records[link] = self.Record("person", self.Person(link))
        return self.records[link].link

    def add_family(self, link):
        self.records[link] = self.Record("family", self.Family(link))
        return self.records[link].link

    class Person:
        def __init__(self, link):
            self.link = link

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

    class Family:
        def __init__(self, link):
            self.link = link

            self.husband = None
            self.wife = None
            self.children = []

            self.marriage_date = None
            self.marriage_place = None

            self.divorced = False
            self.even = False
            self.even_reason = None
