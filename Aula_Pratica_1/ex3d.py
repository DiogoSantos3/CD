def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)


def comb(n, k):
    return int(factorial(n) / (factorial(k) * factorial(n - k)))


print(comb(7,3))