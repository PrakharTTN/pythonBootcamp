from functools import reduce

a = list(filter(lambda x: x == x[::-1], ["abba", "baba", "madam"]))
print(a)

a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
b = a.transpose

b = []
for i in range(len(a)):
    b.append([j[i] for j in a])

print(b)


a = iter([1, 2, 3, 4, 5])
for _ in range(5):
    print(_, next(a))


def fib(number):
    a, b, counter = 0, 1, 0
    while True:
        if counter > number:
            return
        yield (a)
        a, b = b, a + b
        counter += 1


a = fib(5)
for _ in a:
    print(_)
