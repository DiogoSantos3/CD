def num_func(left, right):
    # multiplos de 4 no intervalo de left-right
    for i in range(left, right + 1):
        if i % 4 == 0:
            print(i)

    print("=====================================")


if __name__ == "__main__":
    num_func(1, 10)
    num_func(10, 20)
    num_func(20, 30)
    num_func(30, 40)
