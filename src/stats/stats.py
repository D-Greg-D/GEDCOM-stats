from datetime import date, datetime

class Stats:
    def __init__(self, config, tree):
        self.config = config
        self.tree = tree

    def go(self):
        self.general()
        self.death_reason_test()
        self.life_expectancy()

    def general(self):
        people_number = 0
        people_birth_dates_number = 0
        families_number = 0
        for record in self.tree.records.values():
            if record.type == "person":
                people_number += 1
                if record.birth_date == None:
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
                        if stat["groups"] == "gender":
                            if record.gender == "male":
                                result["m"].append(record.death_reason != None)
                            elif record.gender == "female":
                                result["f"].append(record.death_reason != None)

            for (group, value) in result.items():
                new_value = 0
                for b in value:
                    if b:
                        new_value += 1
                result[group] = new_value

            print("Количество людей по гендерам с указанной причиной смерти:", result)

    def life_expectancy(self):
        people = self.tree.get_corresponding_people([["gender", "male"], ["birth_date", datetime.strptime("1917", "%Y"), datetime.now()], ["not alive"]])
        print(len(people))
        avg_life = 0
        all_lives = []
        for person in people:
            all_lives.append((person.death_date - person.birth_date).days)
            avg_life += (person.death_date - person.birth_date).days
        avg_life /= len(people)
        median_life = (all_lives[(len(all_lives) - 1) // 2] + all_lives[len(all_lives) // 2]) / 2
        print("Средняя продолжительность жизни:", avg_life / 365.24)
        print("Медианная продолжительность жизни:", median_life / 365.24)
