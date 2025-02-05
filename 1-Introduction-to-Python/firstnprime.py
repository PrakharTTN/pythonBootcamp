def is_prime(num):
    if num<=1:
        return False
    for i in range(2,int(num**(1/2))+1):
        if num % i == 0:
            return False
    else:
        return True

# def first_n_primes(n):
#     primes =[]
#     num =2  
#     while len(primes)<n:
#         if is_prime(num):
#             primes.append(num)
#         num+=1
#     return primes
# n = 10
# a = [2]  
# x = 3  
# while len(a) < n:
#     for i in a:
#         if x % i == 0:
#             break  
#     else:
#         a.append(x) 
#     x += 1

# print(a)

# n=int(input('Enter the number of prime numbers req: '))
# print(first_n_primes(n))

def sieve(limit):
    list1=[True]*(limit+1)
    list1[0]=list1[1]=False

    for i in range(2,int(limit**(1/2))):
        if list1[i]:
            for j in range(i*i,limit+1,i):
                list1=[False]
    
    primes=[]
    for i,j in enumerate(list1):
        print(i,j)
        if is_prime(j):
            primes.append(i)
            
    return primes
print(sieve(10))
