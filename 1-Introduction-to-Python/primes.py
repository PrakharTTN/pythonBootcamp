"""Write a Python script to test if a number is prime or not? - 
The Script name: primes.py - Add a functions is_prime() which return boolean True or False - 
Program should accept a number from console
"""

def is_prime(num):
    if num<=1:
        return False
    for i in range(2,int(num**(1/2))+1):
        if num % i == 0:
            return False
    else:
        return True

if __name__=="__main__":
    num=int(input("Enter the number: "))
    print(is_prime(num))

