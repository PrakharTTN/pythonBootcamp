class InvalidAgeException (Exception):
    errorMessage="Exception Occured. Age is less than 18."
    pass

try:
    age=int(input("Enter the Age: "))
    if age<18:
        raise InvalidAgeException
    print("You can vote")
except InvalidAgeException as e:
    print(e.errorMessage)
