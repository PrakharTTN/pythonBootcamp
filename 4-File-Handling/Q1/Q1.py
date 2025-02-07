with open("number.txt","r") as numbers, open("even.txt",'w+') as evenNumbers, open("odd.txt",'w+') as oddNumbers, open("float.txt",'w+') as floatNumbers:
    for i in numbers.readlines():
            if ('.' not in i) and int(i)%2==0:
                evenNumbers.write(i)
            if ('.' not in i) and int(i)%2!=0:
                oddNumbers.write(i)
            if '.' in i:
                floatNumbers.write(i)
    oddNumbers.seek(0)
    evenNumbers.seek(0)
    floatNumbers.seek(0)

    print("Numbers in evenNumbers.txt\n"+evenNumbers.read())
    print("Numbers in oddNumbers.txt\n"+oddNumbers.read())
    print("Numbers in floatNumbers.txt\n"+floatNumbers.read())