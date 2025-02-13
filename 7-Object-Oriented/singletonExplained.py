import gc

class Database:
    has_obj = None
    
    def __new__(cls):
        if cls.has_obj is None:
            cls.has_obj = super().__new__(cls)
        return cls.has_obj
    
    @classmethod
    def refdel(cls):
        cls.has_obj=None

# Create instances of Database
db1 = Database()
db2 = Database()

print(f"id(db1): {id(db1)}")  # id(db1) and id(db2) should be the same
print(f"id(db2): {id(db2)}")  # because they refer to the same object

# Delete the instances
del db1
del db2

# Explicitly clear the singleton reference
Database.refdel()  # Manually clear the singleton instance reference

# Call garbage collector to cleanup
gc.collect()
# Create a new instance, which will be a fresh instance
db3 = Database()
print(f"id(db3): {id(db3)}")  # id(db3) should be a new, different instance
