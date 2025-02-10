"""Write a code to print binary, octal or hexa-decimal presentation of a number. 
Do not use any third party library.
"""

def toBinary(n):
    output = ""
    while (n>0):
        output = str(n%2)+output
        n = n//2
    return int(output)

def toOctal(n):
    output = ""
    while (n>0):
        output = str(n%8)+output
        n = n//8
    return int(output)

def toHexadecimal(n):
    hexList= [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F']
    output = ""
    while (n>0):
        output = str(hexList[n % 16])+output
        n = n//16
    return output

n = int(input("Enter a Number: "))

print("In Binary: ", toBinary(n))
print("In Octal: ", toOctal(n))
print("In Hexadecimal: ", toHexadecimal(n))