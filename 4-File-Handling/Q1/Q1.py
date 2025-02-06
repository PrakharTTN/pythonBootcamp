with open("number.txt","r") as numbers:
    f=numbers.readlines()

with open("even.txt",'w+') as evenNumbers:
    for i in f:
        if ('.' not in i) and int(i)%2==0:
            evenNumbers.write(i)
    evenNumbers.seek(0)
    print("Numbers in evenNumbers.txt\n"+evenNumbers.read())

with open("odd.txt",'w+') as oddNumbers:
    for i in f:
        if ('.' not in i) and int(i)%2!=0:
            oddNumbers.write(i)
    oddNumbers.seek(0)
    print("Numbers in oddNumbers.txt\n"+oddNumbers.read())

with open("float.txt",'w+') as floatNumbers:
    for i in f:
        if '.' in i:
            floatNumbers.write(i)
    floatNumbers.seek(0)
    print("Numbers in floatNumbers.txt\n"+floatNumbers.read())

