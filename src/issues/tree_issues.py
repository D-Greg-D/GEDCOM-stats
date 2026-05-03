class Tree_issues:
    def __init__(self, tree):
        self.tree = tree
    
    def separate_trees(self):
        for person in self.tree.records.values():
            if not person.looked:
                self.dfs(person.link)
                print("Subtree found")

    def dfs(self, person):
        if person == None:
            return
        person = self.tree.get(person)
        if person.looked:
            return
        person.looked = True
        if person.origin_family != None:
            self.dfs(self.tree.get(person.origin_family).husband)
            self.dfs(self.tree.get(person.origin_family).wife)
        for family in person.families:
            self.dfs(self.tree.get(family).husband)
            self.dfs(self.tree.get(family).wife)
            for child in self.tree.get(family).children:
                self.dfs(child)
