def decorator(fun):
    if callable(fun):

        def wrapper(*args, **kwargs):
            result = fun(*args, **kwargs)
            return result**2

        return wrapper
    else:
        return fun**2


def nadd(a, b):
    return a + b


@decorator
def add(a, b):
    return a + b


result = add(3, 4)
newresult = decorator(nadd(3, 4))

print(result)
print(newresult)
