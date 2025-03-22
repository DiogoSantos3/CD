def mdc(a, b):
    # máximo divisor comum
    if b == 0:
        return a

    else:
        return mdc(b, a % b)


if __name__ == "__main__":
    # mdc(10,5)
    print(mdc(48, 18))
