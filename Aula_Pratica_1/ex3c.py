def progressao_geometrica(N, u, r):
    termos = []  
    for n in range(N):
        termo = u * r ** n  
        termos.append(termo)
    return termos


N = 5  
u = 2  
r = 3  

resultado = progressao_geometrica(N, u, r)
print(resultado)


