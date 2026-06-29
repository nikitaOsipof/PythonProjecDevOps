class Person:
    lev = "1 уровень"  # атрибут класса

    def __init__(self, level):
        self.level = level

    def display_info(self):
        print("Level: ", self.level, Person.lev)

#print(Person.display_info())

p1 = Person(12)

p2 = Person(101)
print(p1.level)
print(p2.level)
print(p1.display_info())