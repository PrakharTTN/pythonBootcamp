class person:
    def __init__(self):
        self.__name="Jain AI"
        self.age=21
    def get_name(self):
        print(self.__name)

p1=person()
p1.get_name()

print(p1.age)
print(p1._person__name)
