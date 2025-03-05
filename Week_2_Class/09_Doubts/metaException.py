def t1(a):
    try:
        return a / 0
    except:
        raise Exception


def t2(a):
    try:
        t1(a)
    except:
        raise Exception


def main():
    try:
        t2(2)
    except Exception as e:
        print("exception occurent")


main()
