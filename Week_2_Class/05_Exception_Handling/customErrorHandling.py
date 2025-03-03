class InvalidAgeException(Exception):
    errorMessage = "Exception Occured. Age is less than 18."
    pass


try:
    age = int(input("Enter the Age: "))
    if age < 18:
        raise InvalidAgeException
    print("You can vote")
except InvalidAgeException as e:
    print(e.errorMessage)


# Step 1: Define a custom exception
class AgeTooLowError(Exception):
    """Raised when the provided age is too low."""

    def __init__(self, age, message="Age is too low, must be 18 or older."):
        self.age = age
        self.message = message
        super().__init__(self.message)


# Step 2: Function to check age and raise the custom exception if needed
def check_age(age):
    if age < 18:
        raise AgeTooLowError(age)
    else:
        print(f"Age {age} is valid.")


# Step 3: Test the custom exception
try:
    age = int(input("Enter your age: "))
    check_age(age)
except AgeTooLowError as e:
    print(f"Error: {e.message} (Provided age: {e.age})")
except ValueError:
    print("Invalid input! Please enter a valid number for age.")
