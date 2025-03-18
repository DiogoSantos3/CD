import math

def combinacoes(n, k):
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

# Exemplo de uso
n = 5
k = 2
resultado = combinacoes(n, k)
print(f"O número de combinações de {n} elementos tomados {k} a k é: {resultado}")
