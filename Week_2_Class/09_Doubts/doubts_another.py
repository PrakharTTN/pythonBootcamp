class Animal:
    def speak(self):
        print("Animal speaking")


class Dog(Animal):
    def speak(self):
        super().speak()  # Call the parent class's speak method
        print("Dog barking")


dog = Dog()
super(Dog, dog).speak()
# Output:
# Animal speaking
# Dog barking

import datetime


datetime_obj = datetime.datetime.strptime(
    datetime.datetime.now().strftime("%d-%m-%Y-%H:%M:%S"), "%d-%m-%Y-%H:%M:%S"
)

print(datetime_obj)


class a:
    def __init__(self, num):
        self.number = num


class b(a):
    def __init__(self, name):
        a.__init__(self, name)


new_b = b(4)
a = super(a, new_b).__init__()


if a := False:
    pass
print(a)


def print_output(func):
    def wrapper(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        print("Output is: " + str(res))
        return res

    return wrapper


class myclass:
    def __init__(self, num):
        self.num = num

    @print_output
    def check(self):
        return self.num * 2


a = myclass(5)
a.check()


class MyClass:
    class_variable = "I am a class variable"
    new_class_variable = "Hello"

    def __init__(self, value):
        self.instance_variable = value

    @staticmethod
    def static_method(self, cls):
        # This will raise an error because it cannot access instance or class variables directly
        print(self.instance_variable)  # Error: 'self' is not defined here
        print(
            cls.class_variable
        )  # Error: cannot access class variables directly in static method

    @classmethod
    def class_method(cls):
        print(cls.class_variable)  # This is valid

    def instance_method(self):
        print(self.instance_variable)  # This is valid


class subClass(MyClass):

    @classmethod
    def class_method(cls):
        cls.class_variable = "isfbfbdj"
        print(cls.class_variable)


# Creating an object of MyClass
obj = MyClass("I am an instance variable")
obj.static_method(obj, MyClass)  # This will raise an error
ob2 = subClass(2)
ob2.class_method()

obj.class_method()  # This will print "I am a class variable"
# obj.instance_method()  # This will print "I am an instance variable"


class Parent:
    @staticmethod
    def static_method():
        print("This is the static method in the Parent class.")


class Child(Parent):
    @staticmethod
    def static_method():
        print("This is the overridden static method in the Child class.")


a = Child()
a.static_method()
super(Child, a).static_method()

a = [4, 5, 6, 7]
for _ in a:
    print(_)
