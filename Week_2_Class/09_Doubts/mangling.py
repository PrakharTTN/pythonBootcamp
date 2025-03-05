class person:
    def __init__(self):
        self.__name = "Jain AI"
        self.age = 21

    def get_name(self):
        print(self.__name)


p1 = person()
p1.get_name()

print(p1.age)
print(p1._person__name)


"""USE GETTER/SETTER TO ACCESS PRIVATE METHODS WITHIN THE CLASS"""


class MyClass:
    # Define the slots to restrict instance attributes
    __slots__ = ["_private_variable"]

    def __init__(self, value):
        # Directly setting values to slots
        self._private_variable = value

    # Getter method
    def get_private_variable(self):
        return self._private_variable

    # Setter method
    def set_private_variable(self, value):
        self._private_variable = value


# Create an object of MyClass
obj = MyClass(42)

# Accessing the private variable through getter and setter
print(obj.get_private_variable())  # Output: 42

obj.set_private_variable(100)
print(obj.get_private_variable())  # Output: 100
print(obj.__slots__)
