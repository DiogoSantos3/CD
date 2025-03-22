def maxnmin(v):
    max_value = v[0]
    min_value = v[0]
    for i in range(len(v)):
        if v[i] > max_value:
            max_value = v[i]

        elif v[i] < min_value:
            min_value = v[i]

    return max_value, min_value


print(maxnmin([10, 5, 8, 15, 2]))