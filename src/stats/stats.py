class Stats:
    def __init__(self, config, tree):
        self.config = config
        self.tree = tree

    def go(self):
        self.general()
        self.death_reason_test()

    def general(self):
        people_number = 0
        people_birth_dates_number = 0
        families_number = 0
        for record in self.tree.records.values():
            if record.type == "person":
                people_number += 1
                if record.link.birth_date == None:
                    people_birth_dates_number += 1
            elif record.type == "family":
                families_number += 1
        print(f"Людей в дереве: {people_number}\nУ {people_birth_dates_number} из них некорректно указана дата рождения\nСемей в дереве: {families_number}")
    
    def death_reason_test(self):
        for stat in self.config.get("stats", []):
            result = {"m": [], "f": []}

            if stat["objects"] == "people":
                for record in self.tree.records.values():
                    if record.type == "person":
                        person = record.link
                        if stat["groups"] == "gender":
                            if person.gender == "m":
                                result["m"].append(person.death_reason != None)
                            elif person.gender == "f":
                                result["f"].append(person.death_reason != None)

            for (group, value) in result.items():
                new_value = 0
                for b in value:
                    if b:
                        new_value += 1
                result[group] = new_value

            print("Количество людей по гендерам с указанной причиной смерти:", result)

    def life_expectancy(self):
        pass
