def is_prime(num):
    for i in range(2,(num//2)+1):
        if num%i==0:
            return False
    else:
        return True


num=int(input("Enter the number: "))
print(is_prime(num))

