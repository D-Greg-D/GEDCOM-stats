class Tree:
    def __init__(self):
        self.records = {}
        print("The tree is created")
    
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
            self.families = []
    
    class Family:
        def __init__(self, link):
            self.link = link
            self.children = []
            self.divorced = False
            self.even = False