'''Q1. Write an object oriented code to implement Prime number class.

Implement a Prime class which should have following funcnatinality:

- Ability to test if a number is prime or not 
- Generate prime numbers
- Generate prime numbers greater than a number N
- Generate prime numbers  less than a number N
- Generate all prime numbers between N, to M
- implement __len__() to tell number of primes between N and M where N < M

-  overload +, += operators to nerate number prime number with respect to current prime  nuber  e.g.

>> p = Prime(3)
>> p + 1
5
>> p + 2
7
>> p += 3
>> p
Prime(11)

implement `__repr__()`  and `__str__() methods'''
class Prime:
    def __init__(self, initial, final):
        self.initial = initial
        self.final= final
    
    def is_prime(self, num):
        '''To check if the num provided is prime'''
        if num <= 1:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    def greater_than(self,steps):
        '''Used steps to find the primes after the self.initial'''        
        primes = []
        temp=self.initial
        while steps > 0:
            if self.is_prime(temp):
                primes.append(temp)
                steps -= 1
            temp += 1
        return primes

    def less_than(self,steps=None):
        '''To generate primes which are less than self.final 
        If steps given: generate n primes before self.final
        lest generate till smallest prime'''
        primes = []
        for i in range(2, self.final):
            if self.is_prime(i):
                primes.append(i)
        return primes

    def between_num(self):
        '''To generate primes betweeen self.inital and self.final'''
        primes = []
        for i in range(self.initial + 1, self.final):
            if self.is_prime(i):
                primes.append(i)
        return primes
    
    def __len__(self):
        '''To return the number of prime number between self.initial and self.fianl'''
        return len(self.between_num())

    def __add__(self, num):
        '''To overload the self.inital using + operator to generate next prime
        eg: p=Prime(3)+1
            p+1 -> 5
            ...'''
        temp = self.initial
        while num > 0:
            temp += 1
            if self.is_prime(temp):
                num -= 1
        return temp
    
    def __iadd__(self, num):
        '''Continuation of add overloading, here overloading '+=' assigning the value to self.inital'''
        self.initial = self.__add__(num)
        return self
    
    def __repr__(self):
        '''implemented __repr__'''
        return f"Prime({self.initial})"

    def __str__(self):
        '''implemented __str__'''
        return f"Prime Number: {self.initial}"


test = Prime(3,101)
print(test + 1)  
print(test + 2)  
test += 3 
print(test)  
print(test.is_prime(4))  
print(test.greater_than(10))
print(test.less_than())  
print(test.between_num()) 
print(len(test))