#=============== i ===============
import random
import string

def gerar_palavra_passe():
    tamanho = random.randint(10, 14)
    alfabeto = string.ascii_letters + string.digits + "!@#$%&*?"
    return ''.join(random.choice(alfabeto) for _ in range(tamanho))

# Gerar 10 exemplos
for i in range(10):
    print(f"PW{i+1}: {gerar_palavra_passe()}")


#=============== ii ===============


#=============== iii ===============


#=============== iv ===============


