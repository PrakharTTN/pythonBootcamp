def is_prime(num):
    if num<=1:
        return False
    for i in range(2,int(num**(1/2))+1):
        if num % i == 0:
            return False
    else:
        return True

num=int(input("Enter the number: "))
print(is_prime(num))

