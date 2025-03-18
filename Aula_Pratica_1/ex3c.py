def progressao_geometrica(N, u, r):
    termos = []  # Lista para armazenar os termos
    for n in range(N):
        termo = u * r ** n  # Fórmula do n-ésimo termo
        termos.append(termo)
    return termos

# Exemplo de uso da função
N = 5  # Número de termos
u = 2  # Primeiro termo
r = 3  # Razão

resultado = progressao_geometrica(N, u, r)
print("Os primeiros", N, "termos da PG são:", resultado)


