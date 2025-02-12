'''Q3. Implement a singleton class `Database` that ensures 
only one instance of the class can be created.'''

class Database:
    def __new__(cls):
        if not hasattr(cls,'instance'):
            cls.instance=super(Database,cls).__new__(cls)
            print("Creating one and only database instance")
        else:
            print("Instance already exists, returning the created one.")
        return cls.instance


obj1=Database()
obj2=Database()
print("Unique ID of obj1: ",id(obj1))
print("Unique ID of obj2: ",id(obj2))
print("Checking if obj1=obj2: ", obj1==obj2)