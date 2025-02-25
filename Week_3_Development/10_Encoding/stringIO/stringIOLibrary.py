from io import StringIO

#create a StringIO object and write data to it
my_string = StringIO()
my_string.write("Hello python bootcamp\n")
my_string.write("This is an example of stringIO.\n")

#move the cursor to the beginning
my_string.seek(0)

#read the data from the StringIO object 
content = my_string.read()
print(content)

#using readlines here
my_string.seek(0)
print(my_string.readline())  
print(my_string.readline())  
