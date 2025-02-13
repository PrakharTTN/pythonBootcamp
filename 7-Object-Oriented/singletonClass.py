'''Q3. Implement a singleton class `Database` that ensures 
only one instance of the class can be created.'''

class Database:
    has_obj=None
    def __new__(cls):
        if cls.has_obj==None:
            cls.has_obj=super().__new__(cls)
            print("The first instance has been creeated")
        else:
            print("The instance already exists.")
        return cls
    
obj1=Database() 
obj2=Database()
print("Unique ID of obj1: ",id(obj1))
print("Unique ID of obj2: ",id(obj2))
print("Checking if obj1=obj2: ", obj1==obj2)