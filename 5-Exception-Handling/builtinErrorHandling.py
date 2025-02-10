try:
    x=int(input("Enter value:" )) #ValueError exception
    y=x+'ABC' #TypeError Exception
    a=20
    c=a/0#ZeroDivisionError or RuntimeError
      

except ValueError:
    print("Value Error: Enter an INTEGER")

except TypeError:
    print("TypeError: Can't concatenate the datatypes.")
    
except ZeroDivisionError:
    print("Runtime Error: Do check if you are dividing by zero.")







