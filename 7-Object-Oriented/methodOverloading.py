'''Q4. Python does not support method overloading directly. Implement a class MathOperations with a method add() that can handle both two and three arguments.'''

class MathOperation:
    #Problem with overloading is that it uses the latest defined one
    #Using args to provide multiple arguments
    def add(self, *args):
        return sum(args) 

obj1=MathOperation()
print(obj1.add(1,2))
print(obj1.add(1,2,3))
print(obj1.add(1,2,3,4))