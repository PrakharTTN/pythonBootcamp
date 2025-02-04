def is_prime(num):
    if num<=1:
        return False
    for i in range(2,int(num**(1/2))+1):
        if num % i == 0:
            return False
    else:
        return True

def first_n_primes(n):
    primes =[]
    num =2  
    while len(primes)<n:
        if is_prime(num):
            primes.append(num)
        num+=1
    return primes
n = 10
a = [2]  
x = 3  
while len(a) < n:
    for i in a:
        if x % i == 0:
            break  
    else:
        a.append(x) 
    x += 1

print(a)

n=int(input('Enter the number of prime numbers req: '))
print(first_n_primes(n))
