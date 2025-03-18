def min_max(vetor):
    minimo = min(vetor)
    maximo = max(vetor)
    return minimo, maximo


vetor = [3, 5, 1, 9, 2]
minimo, maximo = min_max(vetor)

print(f"mínimo: {minimo}")
print(f"máximo: {maximo}")
