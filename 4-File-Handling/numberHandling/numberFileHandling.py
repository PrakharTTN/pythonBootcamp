"""Q1. You have a number.txt, with each line a real number. Write a code to split this file into 3 files as follows:

even.txt  -- contain all even numbers
odd.txt -- all odd number
float.txt -- all floating point number

Use with() clause for file handling
"""

with open("number.txt","r") as numbers, open("even.txt",'w+') as evenNumbers, open("odd.txt",'w+') as oddNumbers, open("float.txt",'w+') as floatNumbers:
    for i in numbers.readlines():
            if ('.' not in i):
                if int(i)%2==0:
                    evenNumbers.write(i)
                else:
                    oddNumbers.write(i)
            else:
                floatNumbers.write(i)
                
    oddNumbers.seek(0)
    evenNumbers.seek(0)
    floatNumbers.seek(0)

    print("Numbers in evenNumbers.txt\n"+evenNumbers.read())
    print("Numbers in oddNumbers.txt\n"+oddNumbers.read())
    print("Numbers in floatNumbers.txt\n"+floatNumbers.read())